from hazm import Normalizer, word_tokenize

normalizer = Normalizer()

def preprocess(text):
    text = normalizer.normalize(text)
    tokens = word_tokenize(text)
    return " ".join(tokens)
