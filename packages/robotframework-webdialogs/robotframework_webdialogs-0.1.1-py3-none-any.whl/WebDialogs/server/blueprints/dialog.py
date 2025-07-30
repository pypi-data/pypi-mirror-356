from flask import Blueprint, redirect, render_template, request

from ..services import dialog_manager
from ..services.dialogs.base import CustomStepDialog
from ..services.utils import __get_all_values_from_form

dialog = Blueprint("dialog", __name__, url_prefix="/dialog")


@dialog.route("/")
def show_dialog():
    dialog = dialog_manager.get()

    if dialog is None:
        return redirect("/")

    return render_template(f"dialogs/{dialog.template}", **dialog.__dict__)


@dialog.post("/submit")
def submit_dialog():

    data = __get_all_values_from_form(request)

    dialog = dialog_manager.get()
    if isinstance(dialog, CustomStepDialog):
        value = data
    else:
        value = data["response"]

    dialog_manager.answer(value)
    return redirect("/")
