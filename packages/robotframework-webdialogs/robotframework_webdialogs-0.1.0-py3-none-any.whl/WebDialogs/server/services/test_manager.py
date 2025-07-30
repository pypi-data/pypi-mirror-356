import enum


class test_status_enum(enum.Enum):
    PENDING = 0
    RUNNING = 1
    FINISHED = 2


class TestManager:
    def __init__(self):
        self.test_status = test_status_enum.PENDING

    def reset(self):
        self.test_status = test_status_enum.PENDING

    def get_status(self):
        return self.test_status.name

    def start(self):
        self.test_status = test_status_enum.RUNNING

    def stop(self):
        self.test_status = test_status_enum.FINISHED
