from windows_use.telemetry.views import BaseTelemetryEvent
from tempfile import TemporaryDirectory
from uuid_extensions import uuid7str
from dotenv import load_dotenv
from posthog import Posthog
from pathlib import Path
import logging
import os
import atexit

load_dotenv()

logger=logging.getLogger(__name__)

class ProductTelemetry:
    PROJECT_API_KEY = 'phc_uxdCItyVTjXNU0sMPr97dq3tcz39scQNt3qjTYw5vLV'
    HOST = 'https://us.i.posthog.com'

    def __init__(self):
        self._client = None
        self._user_id = None
        self._enabled = os.getenv("ANONYMIZED_TELEMETRY", "True").lower() == "true"

    @property
    def client(self):
        if self._enabled and self._client is None:
            try:
                self._client = Posthog(
                    project_api_key=self.PROJECT_API_KEY,
                    host=self.HOST,
                    disable_geoip=False,
                    enable_exception_autocapture=True,
                    flush_at=10,
                    flush_interval=5.0
                )
                # Unregister Posthog's atexit join handler to prevent hanging on exit
                try:
                    atexit.unregister(self._client.join)
                except Exception:
                    pass
            except Exception as e:
                logger.error(f"Failed to initialize Posthog client: {e}")
                self._enabled = False
        return self._client

    @property
    def user_id(self):
        if self._user_id is not None:
            return self._user_id
        
        temp_dir = Path(os.path.join(os.environ.get('TEMP', os.environ.get('TMP', '/tmp')), '.windows-use'))
        temp_dir.mkdir(parents=True, exist_ok=True)
        user_id_file = temp_dir / '.windows-use-user-id'
        
        if user_id_file.exists():
            try:
                self._user_id = user_id_file.read_text(encoding='utf-8').strip()
            except Exception:
                pass
                
        if not self._user_id:
            self._user_id = uuid7str()
            try:
                user_id_file.write_text(self._user_id, encoding='utf-8')
            except Exception:
                pass
                
        return self._user_id

    def capture(self, event:BaseTelemetryEvent):
        client = self.client
        if not client:
            return 
        try:
            client.capture(
                distinct_id=self.user_id,
                event=event.event_name,
                properties={**event.properties,'process_person_profile': True}
            )
        except Exception as e:
            logger.error(f"Failed to capture telemetry event {event.event_name}: {e}")

    def flush(self):
        client = self.client
        if client:
            try:
                client.flush()
            except Exception as e:
                logger.error(f"Failed to flush telemetry data: {e}")
        else:
            logger.debug("Telemetry client is not initialized; skipping flush.")
