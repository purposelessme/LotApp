import dbm


class Db:

    @staticmethod
    def create_db(name):
        with dbm.open(f"databases/{name}", "c") as db:
            pass

    @staticmethod
    def add_entry(name, field):
        with dbm.open(f"databases/{name}", "w") as db:
            db[field] = ""

    @staticmethod
    def list_files(name):
        with dbm.open(f"databases/{name}", "w") as db:
            return list(db.keys())
