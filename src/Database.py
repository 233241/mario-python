import shelve

class Database(object):
    @staticmethod
    def save(path, key, data):
        try:
            db = shelve.open(path)
            if db.has_key(key):
                del db[key]
            db[key] = data
            db.sync()
        finally:
            db.close()
    @staticmethod
    def load(path, key):
        data = None
        try:
            db = shelve.open(path)
            data = db[key]
        finally:
            db.close()
            return data
