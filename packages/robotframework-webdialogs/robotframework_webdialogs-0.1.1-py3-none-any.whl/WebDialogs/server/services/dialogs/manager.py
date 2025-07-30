import threading

from .base import Dialog
from .builder import DialogBuilder


class DialogManager:
    def __init__(self):
        self.dialog: Dialog = None
        self.lock = threading.Lock()

    def reset(self):
        with self.lock:
            self.dialog = None

    def create(self, type, message, **kwargs):
        with self.lock:
            self.dialog = DialogBuilder.build(type, message, **kwargs)

    def get(self):
        return self.dialog

    def answer(self, response):
        with self.lock:
            self.dialog.answer(response)

    def get_response(self):
        if self.dialog is None:
            return None
        response = self.dialog.get_response()
        if response is not None:
            self.reset()
        return response

    def is_message_pending(self):
        return self.dialog is not None and self.dialog.response is None
