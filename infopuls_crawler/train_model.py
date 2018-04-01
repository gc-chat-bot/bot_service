from infopuls_crawler.dao.storage import Storage
from infopuls_crawler.question_answering.qa_model import train_model, get_vectors
import sys
import os


if __name__ == '__main__':

    texts_dir = os.path.join(sys.argv[1])

    # upload data to Mongo
    dao = Storage()
    dao.clear()
    dao.safe_from_dir(texts_dir)
    print(dao.get_all())

    # train model
    vectors = get_vectors()
    train_model(vectors)
