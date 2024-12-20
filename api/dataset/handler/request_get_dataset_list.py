from interface.abstract_handler import AbstractHandler


class RequestGetDatasetList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        pass