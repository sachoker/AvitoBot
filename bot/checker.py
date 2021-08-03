import enchant
import difflib
from transliterate import translit


def check_one(word, slovar='en_US'):
    woi = word
    woi = translit(woi, 'ru', reversed=True)
    sim = dict()
    dictionary = enchant.Dict(slovar)
    suggestions = set(dictionary.suggest(woi))

    for word in suggestions:
        measure = difflib.SequenceMatcher(None, woi, word).ratio()
        sim[measure] = word
    return sim[max(sim.keys())]


def check_all(word):
    woi = word
    woi = translit(woi, 'ru', reversed=True)
    sim = dict()
    dictionary = enchant.Dict("en_US")
    suggestions = set(dictionary.suggest(woi))

    for word in suggestions:
        measure = difflib.SequenceMatcher(None, woi, word).ratio()
        sim[measure] = word
    return sim.keys()
