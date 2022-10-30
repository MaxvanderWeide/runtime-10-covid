import json
import os

class StorageClient:
    def __init__(self):
        pass

    def get_entity(self, entity) -> dict:
        with open(f'{os.path.dirname(__file__)}/data/{entity}.json', 'r') as f:
            data = json.load(f)
        return data


__client = None


def get_client():
    global __client
    if not __client:
        __client = StorageClient()
    return __client
