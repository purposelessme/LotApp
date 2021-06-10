import json


class Db:

    @staticmethod
    def create_db(name):
        with open(f"databases/{name}.txt", "w") as db:
            db.write("{}")

    @staticmethod
    def add_entry(name, field):
        with open(f"databases/{name}.txt", "r") as db:
            j_dict = json.loads(db.read())
            dic = {"participants": {}, "shuffled": {}, "selected": {}, "result": {}, "condition": {"down": ""}}
            j_dict[field] = dic
            data = json.dumps(j_dict)
        with open(f"databases/{name}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def list_files(name):
        with open(f"databases/{name}.txt", "r") as db:
            return json.loads(db.read()).keys()

    @staticmethod
    def add_participant(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["participants"][name] = ""
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def remove_participant(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["participants"].pop(name)
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def get_participants(lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            return json.loads(db.read())[lot]["participants"].keys()

    @staticmethod
    def add_selected(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["selected"][name] = ""
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def remove_selected(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["selected"].pop(name)
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def get_selected(lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            return json.loads(db.read())[lot]["selected"].keys()

    @staticmethod
    def add_shuffled(name, lot, collection):
        dic = {}
        for i in name:
            dic[i] = ""
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["shuffled"] = dic
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def get_shuffled(lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            return json.loads(db.read())[lot]["shuffled"].keys()

    @staticmethod
    def add_result(name, lot, collection):
        dic = {}
        for i in name:
            dic[i] = ""
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["result"] = dic
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def remove_result(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["result"].pop(name)
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def get_result(lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            return json.loads(db.read())[lot]["result"].keys()

    @staticmethod
    def add_condition(name, lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            j_dict = json.loads(db.read())
            j_lot = j_dict[lot]
            j_lot["condition"]["state"] = name
            j_dict[lot] = j_lot
            data = json.dumps(j_dict)
        with open(f"databases/{collection}.txt", "w") as db:
            db.write(data)

    @staticmethod
    def get_condition(lot, collection):
        with open(f"databases/{collection}.txt", "r") as db:
            return json.loads(db.read())[lot]["condition"]["state"]
