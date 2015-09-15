# coding: utf-8

import random

adjectives = ["happy", "jolly", "dreamy", "sad", "angry", "pensive", "focused", "sleepy", "grave", "distracted", "determined", "stoic", "stupefied", "sharp", "agitated", "cocky", "tender", "goofy", "furious", "desperate", "hopeful", "compassionate", "silly", "lonely", "condescending", "naughty", "kickass", "drunk", "boring", "nostalgic", "ecstatic", "insane", "cranky", "mad", "jovial", "sick", "hungry", "thirsty", "elegant", "backstabbing", "clever", "trusting", "loving", "suspicious", "berserk", "high", "romantic", "prickly", "evil"]

names = ["albattani", "almeida", "archimedes", "ardinghelli", "babbage", "bardeen", "bartik", "bell", "blackwell", "bohr", "brattain", "brown", "carson", "colden", "curie", "darwin", "davinci", "einstein", "elion", "engelbart", "euclid", "fermat", "fermi", "feynman", "franklin", "galileo", "goldstine", "goodall", "hawking", "heisenberg", "hoover", "hopper", "hypatia", "jones", "kirch", "kowalevski", "lalande", "leakey", "lovelace", "lumiere", "mayer", "mccarthy", "mcclintock", "mclean", "meitner", "mestorf", "morse", "newton", "nobel", "pare", "pasteur", "perlman", "pike", "poincare", "ptolemy", "ritchie", "rosalind", "sammet", "shockley", "sinoussi", "stallman", "tesla", "thompson", "torvalds", "turing", "wilson", "wozniak", "wright", "yonath"]

def get_random_name(no_dash=False):
    rand = random.SystemRandom()
    if no_dash:
        name = '%s%s' % (rand.choice(adjectives), rand.choice(names))
    else:
        name = '%s-%s' % (rand.choice(adjectives), rand.choice(names))
    return name.lower()