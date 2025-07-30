import time
from pathlib import Path

import requests
from robot.api import logger

from ..server.run import start_flask_server


def float_range(start, stop, step):
    while start < stop:
        yield start
        start += step


WEBDIALOGS_BACKEND_URL = "http://localhost:5000"
WEBDIALOGS_PATH = Path(__file__).parent
WEBDIALOGS_SYMLINK_TEMPLATES = WEBDIALOGS_PATH.joinpath("..", "server", "templates", "dialogs", "custom")
WEBDIALOGS_SYMLINK_STATIC = WEBDIALOGS_PATH.joinpath("..", "server", "static", "custom")


class BackendController:
    def __init__(self, timeout=3600, poll_interval=0.5, custom_templates="templates", custom_static="static"):
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.custom_templates = custom_templates
        self.custom_static = custom_static

    def run_backend(self):
        self._prepare_enviroment()
        self._run_server()
        self._check_alive_backend()
        logger.console(f"WebDialogs initialized in {WEBDIALOGS_BACKEND_URL}")

    def _run_server(self):
        start_flask_server()

    def _prepare_enviroment(self):
        custom_templates_path = Path(self.custom_templates)
        if custom_templates_path.exists():
            if WEBDIALOGS_SYMLINK_TEMPLATES.exists():
                WEBDIALOGS_SYMLINK_TEMPLATES.unlink()
            WEBDIALOGS_SYMLINK_TEMPLATES.symlink_to(custom_templates_path.absolute())

        custom_static_path = Path(self.custom_static)
        if custom_static_path.exists():
            if WEBDIALOGS_SYMLINK_STATIC.exists():
                WEBDIALOGS_SYMLINK_STATIC.unlink()
            WEBDIALOGS_SYMLINK_STATIC.symlink_to(custom_static_path.absolute())

    def _check_alive_backend(self):
        for retry in range(0, 10):
            try:
                requests.get(f"{WEBDIALOGS_BACKEND_URL}/api/ping")
            except:  # noqa
                if retry == 9:
                    raise Exception("Timeout starting backend WebDialogs")
                logger.console("Waiting for WebDialogs to start...")
                time.sleep(1)

    def send_signal(self, signal):
        requests.post(f"{WEBDIALOGS_BACKEND_URL}/api/test/{signal}")

    def create_dialog(self, dialog_type, message, **kwargs):
        requests.post(f"{WEBDIALOGS_BACKEND_URL}/api/create/{dialog_type}", json={"message": message, **kwargs})

    def get_response(self):
        for _ in float_range(0, self.timeout, self.poll_interval):
            r = requests.get(f"{WEBDIALOGS_BACKEND_URL}/api/get_response")
            response = r.json().get("response")
            if response is not None:
                return response
            time.sleep(self.poll_interval)

        raise Exception("Timeout waiting for response")
