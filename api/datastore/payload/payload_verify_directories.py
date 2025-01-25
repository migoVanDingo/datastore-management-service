class PayloadVerifyDirectories:
    @staticmethod
    def form_payload(data: dict) -> dict:
        return {
            "set_name": data.get("set_name"),
            "dataset_directory_path": data.get("dataset_directory_path"),
            "project_name": data.get("project_name"),
            "user_id": data.get("user_id")
        }