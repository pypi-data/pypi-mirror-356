from abc import ABC


class Dialog(ABC):
    template = None

    def __init__(self, message):
        self.message = message
        self.response = None

    def answer(self, response):
        self.response = response

    def get_response(self):
        return self.response


class CustomStepDialog(Dialog):
    template = None

    def __init__(self, message="", step=""):
        super().__init__(message)
        self.step = step
        self.template = f"custom/{step}.html"


class PauseExecutionDialog(Dialog):
    template = "dialog_pause_execution.html"


class ExecuteManualStepDialog(Dialog):
    template = "dialog_execute_manual_step.html"


class GetSelectionFromUserDialog(Dialog):
    template = "dialog_get_selection_from_user.html"

    def __init__(self, message, options):
        super().__init__(message)
        self.options = options


class GetSelectionsFromUserDialog(GetSelectionFromUserDialog):
    template = "dialog_get_selections_from_user.html"


class GetValueFromUserDialog(Dialog):
    template = "dialog_get_value_from_user.html"

    def __init__(self, message):
        super().__init__(message)
