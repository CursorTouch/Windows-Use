from windows_use.telemetry.views import BaseTelemetryEvent
from uuid_extensions import uuid7str
from dotenv import load_dotenv
from posthog import Posthog
import logging
import os

load_dotenv()

logger=logging.getLogger(__name__)

class ProductTelemetry:
    PROJECT_API_KEY = 'phc_uxdCItyVTjXNU0sMPr97dq3tcz39scQNt3qjTYw5vLV'
    HOST = 'https://us.i.posthog.com'

    def __init__(self):
        if os.getenv("ANONYMIZED_TELEMETRY", True):
            self.client = Posthog(
                project_api_key=self.PROJECT_API_KEY,
                host=self.HOST,
                disable_geoip=False,
                enable_exception_autocapture=True
            )
        else:
            self.client = None

    def capture(self, event:BaseTelemetryEvent):
        if not self.client:
            return 
        try:
            self.client.capture(
                distinct_id=uuid7str(),
                event=event.event_name,
                properties={**event.properties,'process_person_profile': True}
            )
        except Exception as e:
            logger.error(f"Failed to capture telemetry event {event.event_name}: {e}")

    def flush(self):
        if self.client:
            try:
                self.client.flush()
            except Exception as e:
                logger.error(f"Failed to flush telemetry data: {e}")
        else:
            logger.debug("Telemetry client is not initialized; skipping flush.")
