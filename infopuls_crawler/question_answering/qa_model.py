import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

from infopuls_crawler.dao.storage import Storage


DAO = Storage()


def get_model():
    model = Word2Vec.load('model')

    return model


def get_answer(model, question):
    model.build_vocab([question.split()], update=True)

    best_sentence = None
    score = 0

    for item in DAO.get_all():
        sentence = item['text']
        new_score = sum(sum(cosine_similarity(
                model.wv[sentence.split()],
                model.wv[question.split()])))/(len(sentence))**(2/3)
        if new_score > score:
            score = new_score
            best_sentence = sentence

    if score < 0.1:
        return 'Could you please rephrase the question?', score

    return best_sentence, score


if __name__ == '__main__':
    question = "marketing specialists"
    model = get_model()
    print(get_answer(model, question))
