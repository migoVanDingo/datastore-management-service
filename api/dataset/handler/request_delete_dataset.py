from interface.abstract_handler import AbstractHandler


class RequestDeleteDataset(AbstractHandler):
    def __init__(self, request_id: str, dataset_id: str):
        self.request_id = request_id
        self.dataset_id = dataset_id

    def do_process(self):
        pass