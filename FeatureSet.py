import nltk
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import wordnet
import datetime as dt


class FeatureSet:
    RelatorList = ["because", "after ", "since", " as "]
    path_to_jar = 'C:\Users\sam.rensenhouse\Downloads\stanford-corenlp-full-2015-12-09\stanford-corenlp-full-2015-12-09\stanford-corenlp-3.6.0.jar'
    path_to_models_jar = 'C:\Users\sam.rensenhouse\Downloads\stanford-corenlp-full-2015-12-09\stanford-corenlp-full-2015-12-09\stanford-corenlp-3.6.0-models.jar'
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

    def __init__(self, sentence_object):
        self.sentence_object = sentence_object
        self.sentence = sentence_object.sentence
        self.nominal1 = sentence_object.nominal1
        self.nominal2 = sentence_object.nominal2

        self.relator_index = None
        self.relator_name = None
        self.relator_right = None
        self.relator_right_index = None
        self.relator_left = None
        self.relator_left_index = None
        self.root = None

        # time1 = dt.datetime.now()
        self.pos_sentence = nltk.pos_tag(nltk.word_tokenize(self.sentence))
        # print ("Part of speech: ", (dt.datetime.now() - time1).microseconds)

        # time1 = dt.datetime.now()
        self.check_for_relator()
        # print ("Relator: ", (dt.datetime.now() - time1).microseconds)
        # time1 = dt.datetime.now()
        self.set_words_near_relator()
        # print ("Near Relator: ", (dt.datetime.now() - time1).microseconds)
        # time1 = dt.datetime.now()
        self.dependency_result = self.dependency_parser.raw_parse(self.sentence)
        # print ("dep restult: ", (dt.datetime.now() - time1).microseconds)
        self.get_root() # sets the root variable

        # self.feature_relator = self.has_relator()
        # self.feature_discredit_relator = self.discredit_relator()
        # self.feature_causal_verb = self.check_for_causal_verb()
        # self.feature_cause_in_sentence = self.check_for_cause_in_sentence()

    def check_for_relator_because(self):
        for string in self.RelatorList:
            if string in self.sentence:
                self.relator_name = string
                self.relator_index = self.sentence.index(string)

    def check_for_relator(self):
        for string in self.RelatorList:
            if string in self.sentence:
                self.relator_name = string
                self.relator_index = self.sentence.index(string)

    def check_for_relator(self):
        for string in self.RelatorList:
            if string in self.sentence:
                self.relator_name = string
                self.relator_index = self.sentence.index(string)

    def check_for_relator(self):
        for string in self.RelatorList:
            if string in self.sentence:
                self.relator_name = string
                self.relator_index = self.sentence.index(string)



    def set_words_near_relator(self):
        if self.has_relator():
            if self.relator_index != 0:
                self.relator_left_index = self.relator_index - 1
                self.relator_left = self.sentence[self.relator_left_index]
            if self.relator_index != len(self.sentence):
                self.relator_right_index = self.relator_index + 1
                self.relator_right = self.sentence[self.relator_right_index]

    def get_part_of_speech(self, word):
        for words in self.pos_sentence:
            if words[0] == word:
                return words[1]

    def get_root(self):
        for parse in self.dependency_result:
            string = str(parse.tree())
            self.root = string[string.find("(") + 1:string.find(" ")]

    def has_relator(self):
        if self.relator_name is not None:
            return True
        return False

    def discredit_relator(self):
        # if the word to the left is a adverb
        if self.get_part_of_speech(self.relator_left) == "RB" and self.relator_name == "after":
            return True
        # if the word to the right is a preposition
        if self.relator_name == "as" and self.get_part_of_speech(self.relator_right) == "IN":
            return True
        return False

    def check_for_causal_verb(self):
        for syn in wordnet.synsets(self.root.strip()):
            if "change" in syn.definition() or "cause" in syn.definition():
                return True
        return False

    def check_for_cause_in_sentence(self):
        if " cause" in self.sentence or "causing" in self.sentence:
            return True
        return False

    # def causal_features(self):
    #     features = {}
    #     features["HasRelator"] = self.has_relator()
    #     features["DiscreditRelator"] = self.discredit_relator()
    #     features["HasCausalVerb"] = self.check_for_causal_verb()
    #     features["HasCause"] = self.check_for_cause_in_sentence()
    #     return features

