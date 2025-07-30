from flask import Blueprint, request

from ..services import dialog_manager, test_manager

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/create/<type>", methods=["POST"])
def api_create(type):
    data = request.get_json()
    print(data)
    dialog_manager.create(type, **data)
    return {}


@api.route("/get_response")
def api_get_response():
    value = dialog_manager.get_response()
    return {"response": value}


@api.route("/test/start", methods=["POST"])
def api_start_test():
    dialog_manager.reset()
    test_manager.start()
    return {"message": "Test started"}


@api.route("/response_awaiting")
def api_is_message_pending():
    return {"status": dialog_manager.is_message_pending()}


@api.route("/test/status")
def api_test_status():
    return {"status": test_manager.get_status()}


@api.route("/test/stop", methods=["POST"])
def api_stop_test():
    dialog_manager.reset()
    test_manager.stop()
    return {"message": "Test stopped"}


@api.route("/ping")
def api_ping():
    return {"message": "pong"}
