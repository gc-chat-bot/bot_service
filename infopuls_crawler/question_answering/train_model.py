from gensim.models import Word2Vec
from infopuls_crawler.dao.storage import Storage
import sys
import os

DAO = Storage()


def get_vectors():
    vectors = []

    for item in DAO.get_all():
        vectors.append(item['text'].lower().split())

    return vectors


def train_model(vectors):
    # to handle non existing words from question
    # vectors.append(question.split())

    model = Word2Vec(vectors, min_count=1)
    # model.wv.save_word2vec_format('model')
    model.save('model')


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
