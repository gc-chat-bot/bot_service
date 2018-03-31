import json
import os
from pymongo import MongoClient
import glob

DATABASE = "scrapper_db"
COLLECTION = "texts_collection"
TEXTS_DIRECTORY = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..", "..")), "texts")


class Storage(object):
    client = MongoClient('localhost', 27017)
    db = client[DATABASE]
    collection = db[COLLECTION]

    def save_from_file(self, file):
        with open(file) as data_file:
            data = json.load(data_file)
            for item in data:
                category = item["category"]
                text = item["text"]
                self.save(category, text)

    def safe_from_dir(self, directory=TEXTS_DIRECTORY):
        """Load all documents from *.json files to Mongo"""

        files = glob.glob(os.path.join(directory, "*.json"))
        for file in files:
            self.save_from_file(file)

    def save(self, category, text):
        document = {"category": category, "text": text}
        id = self.collection.insert_one(document).inserted_id
        return id

    def get_by_category(self, category_like):
        self.collection.find({"category": {"$regex": category_like}})

    def get(self, doc_id):
        return self.collection.find_one({"_id": doc_id})

    def get_all(self):
        return list(self.collection.find())

    def get_size(self):
        return self.collection.count()

    def clear(self):
        return self.collection.drop()


# just for test
def test():
    dao = Storage()

    # dao.clear()
    # id1 = dao.save("cat1", "some text")
    # id2 = dao.save("cat2", "some text")
    # print(dao.get(id1))
    # print(dao.get(id2))
    # print(dao.get_all())
    dao.safe_from_dir()
    print(dao.get_all())


if __name__ == "__main__":
    test()
