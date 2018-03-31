import abc

from infopuls_crawler.question_answering.qa_model import get_best_match, train_model


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
        "fuck"
    ]

    def handle(self, input):
        for pattern in self.bad_questions:
            if pattern in input.text:
                return UserResponse("The question is not appropriate.")


class QuestionHandler(Handler):

    def handle(self, input):
        text = input.text

        # TODO extract more info from question
        user_question = text

        best_sentence, score = get_best_match(user_question)
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


if __name__ == "__main__":
    main()
