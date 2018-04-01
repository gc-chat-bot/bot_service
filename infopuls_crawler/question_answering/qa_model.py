from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import os
from infopuls_crawler.dao.storage import Storage

MODEL_FILE = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), "../../..")), "model")

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
    model.save(MODEL_FILE)


def get_model():
    model = Word2Vec.load(MODEL_FILE)

    return model


def get_answer(model, question):
    model.build_vocab([question.split()], update=True)

    best_sentence = None
    score = 0

    for item in DAO.get_all():
        sentence = item['text'].lower()
        new_score = sum(sum(cosine_similarity(
                model.wv[sentence.lower().split()],
                model.wv[question.lower().split()])))/(len(sentence))**(2/3)
        if new_score > score:
            score = new_score
            best_sentence = sentence

    if score < 0.1:
        return 'Could you please rephrase the question?', score

    return best_sentence, score


if __name__ == '__main__':
    question = "APP developers"
    model = get_model()
    print(get_answer(model, question))
