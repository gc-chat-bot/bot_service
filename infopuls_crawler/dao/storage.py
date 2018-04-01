import json
import os
import sys
import glob
from pymongo import MongoClient

MONGO_CLIENT = MongoClient('mongodb', 27017)

DATABASE = "scrapper_db"
COLLECTION = "texts_collection"


class Storage(object):
    client = MONGO_CLIENT
    db = client[DATABASE]
    collection = db[COLLECTION]

    def save_from_file(self, file):
        with open(file) as data_file:
            data = json.load(data_file)
            for item in data:
                category = item["category"]
                text = item["text"]
                self.save(category, text)

    def safe_from_dir(self, directory):
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


def main(argv):
    texts_dir = os.path.join(argv)

    dao = Storage()
    dao.clear()
    dao.safe_from_dir(texts_dir)
    print(dao.get_all())


if __name__ == "__main__":
    main(sys.argv[1])
