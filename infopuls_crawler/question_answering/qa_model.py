import os

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from stop_words import get_stop_words
from stemming.porter2 import stem

from infopuls_crawler.dao.storage import Storage

MODEL_FILE = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), "../../..")), "model")

DAO = Storage()


def get_vectors():
    vectors = []

    for item in DAO.get_all():
        vectors.append(remove_stopwords(item['text'].lower().split()))

    return vectors


def train_model(vectors):
    model = Word2Vec(vectors, min_count=1)
    model.save(MODEL_FILE)


def get_model():
    model = Word2Vec.load(MODEL_FILE)

    return model


def get_answer(model, question):
    question_words = remove_stopwords(question.lower().split())
    model.build_vocab([question_words], update=True)

    best_sentence = None
    score = 0

    for item in DAO.get_all():
        sentence = item['text']
        splitted_sentence = sentence.lower().split()
        new_score = sum(sum(cosine_similarity(
                model.wv[remove_stopwords(splitted_sentence)],
                model.wv[question_words]))
        )/(len(splitted_sentence))**(2/3)
        if new_score > score:
            score = new_score
            best_sentence = sentence

    if score < 0.4:
        return 'Could you please rephrase the question?', score

    return best_sentence, score


def remove_stopwords(word_list):
    stop_words = list(get_stop_words('en'))

    return [stem(w) for w in word_list if w not in stop_words]


if __name__ == '__main__':
    question = "how many mobile developers do you have?"
    model = get_model()
    print(get_answer(model, question))
