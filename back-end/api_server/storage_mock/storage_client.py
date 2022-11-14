import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('operation', help='Operation', type=str, default='get')
parser.add_argument('entity', help='Entity', type=str)


class StorageClient:
    def __init__(self):
        pass

    def get_entity(self, entity) -> dict:
        with open(f'{os.path.dirname(__file__)}/data/{entity}.json', 'r') as f:
            data = json.load(f)
        return data

    def append_entity(self, entity, entity_body):
        pre_data = self.get_entity(entity)

        for key in pre_data["data"]:
            for country in pre_data["data"][key]:
                pre_data["data"][key][country].append(entity_body["data"][key][country])
        
        with open(f'{os.path.dirname(__file__)}/data/{entity}.json', 'w') as f:
            f.write(pre_data)
        return self

__client = None


def get_client():
    global __client
    if not __client:
        __client = StorageClient()
    return __client


if __name__ == '__main__':
    args = parser.parse_args()
    if args.operation == 'get':
        print(get_client().get_entity(args.entity))
