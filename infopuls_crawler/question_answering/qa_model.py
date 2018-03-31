from gensim.models import Word2Vec

from sklearn.metrics.pairwise import cosine_similarity
from infopuls_crawler.dao.storage import *

DAO = Storage()


def get_best_match(question):
    sentences = []
    vectors = []

    for item in DAO.get_all():
        sentences.append(item['text'])
        vectors.append(item['text'].split())

    return train_model(sentences, vectors, question)


def train_model(sentences, vectors, question):
    # to handle non existing words from question
    vectors.append(question.split())

    model = Word2Vec(vectors, min_count=1)

    best_sentence = None
    score = 0

    for sentence in sentences:
        new_score = sum(sum(cosine_similarity(
                model.wv[sentence.split()],
                model.wv[question.split()])))
        if new_score > 0.5 and new_score > score:
            score = new_score
            best_sentence = sentence

    return best_sentence, score


if __name__ == '__main__':
    question = "marketing"
    print(get_best_match(question))
