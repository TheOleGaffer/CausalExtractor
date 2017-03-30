import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


class Statistics:
    NounPartOfSpeechList = ["NN", "NNS"]

    def __init__(self, sentence, type_of_sentence=None):
        self.type_of_sentence = type_of_sentence
        self.sentence = sentence
        self.nominal1, self.nominal2 = self.get_nominal_pair()
        self.remove_tags()
        self.set_nominal_pairs_to_one_word()
        self.tokenized_sentence = nltk.word_tokenize(self.sentence)
        self.nominal1_index, self.nominal2_index = self.get_nominal_pair_index()
        self.between_nominal_pairs = self.tokenized_sentence[self.nominal1_index:self.nominal2_index + 1]
        self.pos_sentence = nltk.pos_tag(self.between_nominal_pairs)

        # have to remove tags before tokenizing

    def is_valid_from(self):
        if "from" in self.between_nominal_pairs:
            length = len(self.pos_sentence)
            if self.pos_sentence[1][0] == "from" and length < 5:
                return True
            if length > 3:
                return False
            return True
            # index = self.between_nominal_pairs.index("from") - 1
            # pos_before = self.get_part_of_speech("from")
            # for pos in self.NounPartOfSpeechList:
            #     if pos == pos_before:
            #         return True
        return False

    def is_valid_because(self):
        if "because" in self.between_nominal_pairs:
            return True
        return False

    def is_valid_after(self):
        if "after" in self.between_nominal_pairs:
            return True
        return False

    def has_cause_lemma(self):
        stemmer = PorterStemmer()
        for word in self.between_nominal_pairs:
            test_word = stemmer.stem(word)
            if test_word == 'caus':
                return True
        return False

    def get_nominal_pair(self):
        # finds the tags in the s and returns four cases
        match = re.findall(r"(<.*?>(.*?)</.*?>)", self.sentence)
        if match:
            return match[0][1], match[1][1]
            # returns the two cases we want which don't have the tags anymore

    def remove_tags(self):
        self.sentence = self.sentence.replace("<e>", " ")
        self.sentence = self.sentence.replace("</e>", " ")

    def get_nominal_pair_index(self):
        return self.tokenized_sentence.index(self.nominal1), self.tokenized_sentence.index(self.nominal2)

    def is_causal(self):
        return "Cause-Effect" in self.type_of_sentence or "Product-Producer" in self.type_of_sentence

    def get_part_of_speech(self, word):
        for index, words in enumerate(self.pos_sentence):
            if words[0] == word:
                return self.pos_sentence[index - 1][1]

    #for when the nominal has multiple words in the tag
    def set_nominal_pairs_to_one_word(self):
        nom = nltk.word_tokenize(self.nominal1)
        self.nominal1 = nom[0]
        nom = nltk.word_tokenize(self.nominal2)
        self.nominal2 = nom[-1]