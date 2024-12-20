class Constant:
    service = "datastore-management-service"

    datastore_root_dir = "/Users/bubz/Developer/master-project/tests/test-datastore-root"

    base_url = "http://localhost:"
    dao_port = "5010"

    dao = {
        "create": "/api/create",
        "read": "/api/read",
        "list": "/api/read_list",
        "update": "/api/update",
        "delete": "/api/delete"
    }

    table = {
        "DATASTORE": "datastore",
        "DATASET": "dataset"
    }

    delimeter = {
        "DATASTORE": "__",
        "DATASET": "__"
    }

    datastore = {
        "directories": [
            "raw_data/videos",
            "raw_data/images",
            "raw_data/audio",
            "raw_data/other",
            "datasets",
            "logs",
            "reports",
        ],
    }

    dataset = {
        "directories": [
            "ground_truth",
            "preprocessed_data/videos",
            "preprocessed_data/images",
            "preprocessed_data/audio",
            "models",
            "predictions",
            "annotations",
        ],

    }
    files = {
        "metadata": "-metadata.json"
    }
