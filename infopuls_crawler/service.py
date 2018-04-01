import abc
import nltk
from re import *

from infopuls_crawler.question_answering.qa_model import get_model, get_answer


class UserRequest(object):
    """Request data class"""

    chat_id = None
    session_id = None
    text = None

    def __init__(self, chat_id, session_id, text):
        self.chat_id = chat_id
        self.session_id = session_id
        self.text = text


class UserResponse(object):
    """Response data class"""

    text = None

    def __init__(self, text):
        self.text = text


class Handler(object):

    def __init__(self, successor=None):
        self._successor = successor

    def process_request(self, input):
        result = self.handle(input)
        if result is not None:
            return result
        elif self._successor is not None:
            return self._successor.process_request(input)
        else:
            # cannot answer the question itself
            return UserResponse("Please contact our support.")

    @abc.abstractmethod
    def handle(self, input):
        return None


class FilterIrrelevant(Handler):
    # set of irrelevant question templates
    bad_questions = [
        r"fuck"
    ]

    def handle(self, input):
        for pattern in self.bad_questions:
            if pattern in input.text:
                return UserResponse("The question is not appropriate.")


class QuestionHandler(Handler):

    model = get_model()

    question_words = [
        "what ",
        "what's",
        "who",
        "who's",
        "where",
        "where's",
        "why ",
        "why's "
        "whom ",
        "which ",
        "how ",
        "when "
    ]


    def handle(self, input):
        text = input.text

        user_questions = text

        best_sentence, score = get_answer(self.model, user_questions)
        print("sentence: " + str(best_sentence) + ", score: " + str(score))
        if best_sentence is None:
            return None
        else:
            return UserResponse(best_sentence)


def handlers():
    handler1 = QuestionHandler()
    handler2 = FilterIrrelevant(handler1)
    return handler2


def main():
    handler = handlers()
    print(handler.process_request(UserRequest("chat1", "session1", "s fsdtext")).text)

    questions = "What is Infopulse? How many employees the company use?"
    sentences = questions.split()

    for sentence in sentences:
        print(sentence)


if __name__ == "__main__":
    main()
