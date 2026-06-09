from __future__ import annotations

import asyncio
import time

import httpx

from operator_use.inference.api.video.base import BaseVideoAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedVideo, VideoContext, VideoFormat, VideoOptions, VideoStopReason

_BASE = "https://queue.fal.run"


class FalVideoAPI(BaseVideoAPI):
    """
    fal.ai queue-based video generation API.

    All jobs are asynchronous at the provider level: we submit, then poll
    until the status is COMPLETED or FAILED. The full submit→poll→download
    cycle is handled here so callers get a simple awaitable.
    """

    def __init__(self, options: VideoOptions) -> None:
        super().__init__(options)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Key {self.options.api_key}",
            "Content-Type": "application/json",
        }

    def _build_payload(self, context: VideoContext) -> dict:
        payload: dict = {"prompt": context.prompt}
        if context.duration is not None:
            payload["duration"] = context.duration
        if context.aspect_ratio is not None:
            payload["aspect_ratio"] = context.aspect_ratio
        if context.resolution is not None:
            payload["resolution"] = context.resolution
        if context.image is not None:
            import base64
            payload["image_url"] = f"data:image/jpeg;base64,{base64.b64encode(context.image).decode()}"
        return payload

    def _extract_video_url(self, result: dict) -> str | None:
        if "video" in result:
            v = result["video"]
            return v.get("url") if isinstance(v, dict) else v
        if "videos" in result:
            videos = result["videos"]
            if videos and isinstance(videos[0], dict):
                return videos[0].get("url")
        return None

    async def generate(self, model: Model, context: VideoContext) -> GeneratedVideo:
        timeout = self.options.timeout.total_seconds()
        deadline = time.monotonic() + timeout
        headers = self._headers()
        payload = self._build_payload(context)

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Submit job
            resp = await client.post(f"{_BASE}/{model.id}", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            request_id: str = data["request_id"]

            # Poll for completion
            status_url = f"{_BASE}/{model.id}/requests/{request_id}/status"
            result_url = f"{_BASE}/{model.id}/requests/{request_id}"

            while time.monotonic() < deadline:
                await asyncio.sleep(self.options.poll_interval)

                status_resp = await client.get(status_url, headers=headers)
                status_resp.raise_for_status()
                status_data = status_resp.json()
                status = status_data.get("status")

                if status == "COMPLETED":
                    result_resp = await client.get(result_url, headers=headers)
                    result_resp.raise_for_status()
                    result = result_resp.json()

                    video_url = self._extract_video_url(result)
                    video_bytes: bytes | None = None
                    if video_url:
                        dl = await client.get(video_url, follow_redirects=True, timeout=120.0)
                        dl.raise_for_status()
                        video_bytes = dl.content

                    duration = result.get("duration") or context.duration
                    return GeneratedVideo(
                        model_id=model.id,
                        provider="fal",
                        url=video_url,
                        video=video_bytes,
                        format=VideoFormat.MP4,
                        duration=duration,
                        stop_reason=VideoStopReason.Stop,
                    )

                if status == "FAILED":
                    error_info = status_data.get("error") or {}
                    msg = error_info.get("message", "Job failed") if isinstance(error_info, dict) else str(error_info)
                    return GeneratedVideo(
                        model_id=model.id,
                        provider="fal",
                        stop_reason=VideoStopReason.Error,
                        error=msg,
                    )

        return GeneratedVideo(
            model_id=model.id,
            provider="fal",
            stop_reason=VideoStopReason.Timeout,
            error=f"Video generation timed out after {timeout:.0f}s",
        )
