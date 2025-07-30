import time

from robot.api.deco import keyword

from .backend_controller import BackendController


class WebDialogs:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, timeout=3600, poll_interval=0.5, custom_templates="templates", custom_static="static"):
        self.client_backend = BackendController(timeout, poll_interval, custom_templates, custom_static)
        self.client_backend.run_backend()

        self.client_backend.send_signal("start")

    def close(self):
        self.client_backend.send_signal("stop")
        time.sleep(1)

    @keyword("Get Value From User")
    def get_value_from_user(self, message):
        self.client_backend.create_dialog("get_value_from_user", message)
        return self.client_backend.get_response()

    @keyword("Get Selection From User")
    def wait_for_user_selection(self, message, options):
        self.client_backend.create_dialog("get_selection_from_user", message, options=options)
        return self.client_backend.get_response()

    @keyword("Get Selections From User")
    def wait_for_user_selections(self, message, options):
        self.client_backend.create_dialog("get_selections_from_user", message, options=options)
        return self.client_backend.get_response()

    @keyword("Execute Manual Step")
    def execute_manual_step(self, message, default_error=""):
        self.client_backend.create_dialog("execute_manual_step", message)
        response = self.client_backend.get_response()
        if response == "FAIL":
            if default_error:
                msg = default_error
            else:
                msg = self.get_value_from_user("Error message")
            raise AssertionError(msg)
        return response

    @keyword("Pause Execution")
    def pause_execution(self, message):
        self.client_backend.create_dialog("pause_execution", message)
        return self.client_backend.get_response()

    @keyword("Execute Custom Step")
    def execute_custom_step(self, step):
        self.client_backend.create_dialog("execute_custom_step", "Custom Step", step=step)
        return self.client_backend.get_response()
