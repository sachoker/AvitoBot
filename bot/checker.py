import enchant
import difflib
from transliterate import translit
from Levenshtein import distance


def check_one(word):
    wor = translit(word, 'ru', reversed=True)
    with open(r'C:\Users\mv149\PycharmProjects\eazybot\bot\cars.txt', 'r', encoding='UTF-8') as f:
        cars = f.readlines()
        f.close()
    # a = difflib.get_close_matches(wor, cars)
    s = {}
    for i in cars:
        s.update({i: distance(wor, i)})
    ls = sorted(list(s.items()), key=lambda i: i[1])
    return ls[:3]


if __name__ == '__main__':
    print(check_one("тойота камри"))

# def check_one(word, slovar='en_US'):
#    woi = word
#    woi = translit(woi, 'ru', reversed=True)
#    sim = dict()
#    dictionary = enchant.Dict(slovar)
#    suggestions = set(dictionary.suggest(woi))
#
#    for word in suggestions:
#        measure = difflib.SequenceMatcher(None, woi, word).ratio()
#        sim[measure] = word
# return sim[max(sim.keys())]
