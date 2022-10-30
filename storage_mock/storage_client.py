class StorageClient:
    def __init__(self):
        pass


__client = None


def get_client():
    global __client
    if not __client:
        __client = StorageClient()
    return __client
