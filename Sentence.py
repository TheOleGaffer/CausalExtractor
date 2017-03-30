import re
from FeatureSet import FeatureSet


class Sentence:

    RelatorList = ["because", "after", "since", " as "]

    def __init__(self, string, type_of_sentence=None):
        self.type_of_sentence = type_of_sentence
        self.sentence = string
        self.nominal1 = None
        self.nominal2 = None

        self.get_nominal_pair()
        self.remove_tags()
        self.feature_set = FeatureSet(self)
        # have to remove tags before tokenizing

    def get_nominal_pair(self):
        # finds the tags in the s and returns four cases
        match = re.findall(r"(<.*?>(.*?)</.*?>)", self.sentence)
        if match:
            self.nominal1 = match[0][1]
            self.nominal2 = match[1][1]
        # returns the two cases we want which don't have the tags anymore

    def remove_tags(self):
        self.sentence = self.sentence.replace("<e>", "")
        self.sentence = self.sentence.replace("</e>", "")

    def is_causal_from_dataset(self):
        return "Cause-Effect" in self.type_of_sentence

    def causal_features(self):
        features = {"HasRelator": self.feature_set.has_relator(),
                    "DiscreditRelator": self.feature_set.discredit_relator(),
                    "HasCausalVerb": self.feature_set.check_for_causal_verb(),
                    "HasCause": self.feature_set.check_for_cause_in_sentence()}
        return features



