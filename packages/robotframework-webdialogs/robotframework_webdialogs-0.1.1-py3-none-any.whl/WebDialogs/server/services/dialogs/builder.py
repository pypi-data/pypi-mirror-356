from .base import (
    CustomStepDialog,
    ExecuteManualStepDialog,
    GetSelectionFromUserDialog,
    GetSelectionsFromUserDialog,
    GetValueFromUserDialog,
    PauseExecutionDialog,
)


class DialogBuilder:
    DIALOG_TYPES = {
        "execute_manual_step": ExecuteManualStepDialog,
        "get_selection_from_user": GetSelectionFromUserDialog,
        "get_selections_from_user": GetSelectionsFromUserDialog,
        "get_value_from_user": GetValueFromUserDialog,
        "pause_execution": PauseExecutionDialog,
        "execute_custom_step": CustomStepDialog,
    }

    @staticmethod
    def build(type, message, **kwargs):
        dialog_cls = DialogBuilder.DIALOG_TYPES.get(type)
        if not dialog_cls:
            raise ValueError(f"Unknown dialog type: {type}")
        return dialog_cls(message, **kwargs)
