from gensim.models import Word2Vec

from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity


DATABASE = 'scrapper_db'
COLLECTION = 'texts_collection'


def get_sentences():
    client = MongoClient('localhost', 27017)

    db = client[DATABASE]
    collection = db[COLLECTION]
    sentences = []
    vectors = []
    for item in list(collection.find()):
        sentences.append(item['text'])
        vectors.append(item['text'].split())

    return sentences, vectors


def train_model(sentences, vectors, question):
    model = Word2Vec(vectors, min_count=1)
    best_sentence = ''

    score = 0
    for sentence in sentences:
        new_score = sum(sum(cosine_similarity(
                model.wv[sentence.split()],
                model.wv[question.split()])))
        if new_score > 0.5 and new_score > score:
            score = new_score
            best_sentence = sentence

    print(best_sentence, score)


if __name__ == '__main__':
    sentences, vectors = get_sentences()
    question = 'mobile app developers'

    train_model(sentences, vectors, question)
