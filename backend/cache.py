from threading import Lock

class MemStorage:
    """
    This is a thread safe cache storage class for storing key-value pairs.
    """
    def __init__(self):
        self.storage = {}
        self.lock = Lock()

    def set_value(self, key, value):
        with self.lock:
            self.storage[key] = value

    def get_value(self, key):
        with self.lock:
            return self.storage.get(key)

    def get_all_values(self):
        with self.lock:
            return self.storage.copy()

    def delete_value(self, key):
        with self.lock:
            if key in self.storage:
                del self.storage[key]

g_global_kv = MemStorage()


def get_global_kv() -> MemStorage:
    return g_global_kv

