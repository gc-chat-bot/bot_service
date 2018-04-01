import os

DATASETS_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../..", "datasets"))


def load_key_values(file):
    mapping = {}
    with open(file) as f:
        for line in f:
            splitted = line.replace('\n', '').split(" ")
            k = str(splitted[0])
            v = str(splitted[1])
            mapping[k] = v
    return mapping



SPELLING = load_key_values(os.path.join(DATASETS_PATH, "spelling.txt"))
CONTRACTIONS = load_key_values(os.path.join(DATASETS_PATH, "contractions.txt"))
BRITISH = load_key_values(os.path.join(DATASETS_PATH, "british.txt"))


def normalize_word(word):
    if word in SPELLING:
        return SPELLING[word]
    else:
        return word


if __name__ == '__main__':

    print(normalize_word("releived"))
