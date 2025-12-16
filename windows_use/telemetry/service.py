from windows_use.telemetry.views import BaseTelemetryEvent
from tempfile import TemporaryDirectory
from uuid_extensions import uuid7str
from dotenv import load_dotenv
from posthog import Posthog
from pathlib import Path
import logging
import os

load_dotenv()

logger=logging.getLogger(__name__)

class ProductTelemetry:
    PROJECT_API_KEY = 'phc_uxdCItyVTjXNU0sMPr97dq3tcz39scQNt3qjTYw5vLV'
    HOST = 'https://us.i.posthog.com'
    TEMP_FOLDER=Path(TemporaryDirectory().name).parent
    USER_ID=None

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

    @property
    def user_id(self):
        if (self.TEMP_FOLDER/'.windows-use-user-id').exists():
            self.USER_ID = (self.TEMP_FOLDER/'.windows-use-user-id').read_text(encoding='utf-8')
        else:
            self.USER_ID = uuid7str()
            (self.TEMP_FOLDER/'.windows-use-user-id').write_text(self.USER_ID, encoding='utf-8')
        return self.USER_ID

    def capture(self, event:BaseTelemetryEvent):
        if not self.client:
            return 
        try:
            self.client.capture(
                distinct_id=self.user_id,
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
