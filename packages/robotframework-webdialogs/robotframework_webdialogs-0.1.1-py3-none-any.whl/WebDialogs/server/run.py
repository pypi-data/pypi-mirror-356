import threading

from .app import app


def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)


def start_flask_server():
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
