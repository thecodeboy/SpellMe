#!/usr/bin/python
import re
import collections

#Extract each word and convert to lowercase
def words(text):
    return re.findall('[a-z]+', text.lower())

#Build statistical model of words
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#Data structure to store the statistical model
NWORDS = train(words(file('corpus.txt').read()))

#English alphabets
alphabet = 'abcdefghijklmnopqrstuvwxyz'

#Finds set of words possible with edit distance 1
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

#Finds set of words possible with edit distance 2
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

#Spell check engine
def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

#Text based program for spell check
def main():
    print "\n===================================\nSpellMe 0.1\nAuthor: Aishik Saha\n==================================="
    word = raw_input('\nEnter word: ')
    out = correct(word)
    if out==word:
        print "\nThe word you entered is correct."
    else:
        print "\nThe correct word is "+out+"."

#Configuration
if __name__ == '__main__':
  main()
