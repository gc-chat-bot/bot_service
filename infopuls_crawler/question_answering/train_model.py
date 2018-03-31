from gensim.models import Word2Vec
from infopuls_crawler.dao.storage import Storage


DAO = Storage()


def get_vectors():
    vectors = []

    for item in DAO.get_all():
        vectors.append(item['text'].split())

    return vectors


def train_model(vectors):
    # to handle non existing words from question
    # vectors.append(question.split())

    model = Word2Vec(vectors, min_count=1)
    # model.wv.save_word2vec_format('model')
    model.save('model')


if __name__ == '__main__':
    vectors = get_vectors()

    train_model(vectors)
