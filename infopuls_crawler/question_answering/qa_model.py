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
                model.wv[question.split()])))/len(sentence)
        if new_score > score:
            score = new_score
            best_sentence = sentence

    return best_sentence, score


if __name__ == '__main__':
    question = "mobile app developers"
    model = get_model()
    print(get_answer(model, question))
