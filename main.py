import datetime as dt
from Sentence import Sentence
from Statistics import Statistics as stat
from sklearn import tree
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import wordnet
import nltk
import csv
path_to_jar = 'C:\Users\sam.rensenhouse\Downloads\stanford-corenlp-full-2015-12-09\stanford-corenlp-full-2015-12-09\stanford-corenlp-3.6.0.jar'
path_to_models_jar = 'C:\Users\sam.rensenhouse\Downloads\stanford-corenlp-full-2015-12-09\stanford-corenlp-full-2015-12-09\stanford-corenlp-3.6.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

originalFeatureList = list()
testFeatureList = list()
originalSentenceList = list()
testSentenceList = list()
originalTypeList = list()
testTypeList = list()

sentenceList = list()


def write_to_csv(list, file_name):
    with open(file_name, 'w') as csvfile:
        fieldnames = ['HasRelator', 'DiscreditRelator', 'HasCausalVerb', 'HasCause', 'tag']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for sent in originalSentenceList:
            features = sent.causal_features()
            writer.writerow({'HasRelator': features['HasRelator'], 'DiscreditRelator': features['DiscreditRelator'], 'HasCausalVerb': features['HasCausalVerb'], 'HasCause': features['HasCause'], 'tag': sent.is_causal_from_dataset()})


def read_in_csv(list, file_name):
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            features = {}
            features["HasRelator"] = row["HasRelator"]
            features["DiscreditRelator"] = row["DiscreditRelator"]
            features["HasCausalVerb"] = row["HasCausalVerb"]
            features["HasCause"] = row["HasCause"]
            # features["tag"] = row["tag"]
            list.append((features, row["tag"]))


def read_data_to_lists():
    with open('TRAIN_FILE.TXT') as infile:
        count = 0
        for line in infile:
            # if the line of the file is a s add it to the list
            if(line[0].isdigit()):
                # takes out all the digits from the line
                line = ''.join([i for i in line if not i.isdigit()])
                # originalSentenceList.append(Sentence(line.strip('\t\n\"'), next(infile).strip('\n')))
                originalSentenceList.append(line.strip('\t\n\"'))
                originalTypeList.append(next(infile).strip('\n'))
                # count += 1
                # print count

def read_data_to_lists_for_statistics():
    with open('TRAIN_FILE.TXT') as infile:
        for line in infile:
            # if the line of the file is a s add it to the list
            if(line[0].isdigit()):
                # takes out all the digits from the line
                line = ''.join([i for i in line if not i.isdigit()])
                #originalSentenceList.append(stat(line.strip('\t\n\"'), next(infile).strip('\n')))
                originalSentenceList.append(line.strip('\t\n\"'))
                originalTypeList.append(next(infile).strip('\n'))

def read_test_data_to_lists():
    with open('TEST_FILE_FULL.TXT') as infile:
        count = 0
        for line in infile:
            # if the line of the file is a s add it to the list
            if line[0].isdigit():
                # takes out all the digits from the line
                line = ''.join([i for i in line if not i.isdigit()])
                # testSentenceList.append(Sentence(line.strip('\t\n\"'), next(infile).strip('\n')))
                testSentenceList.append(line.strip('\t\n\"'))
                testTypeList.append(next(infile).strip('\n'))
                # count += 1
                # print count



def check_causal(notation):
    return "Cause-Effect" in notation


def change_to_string(bool):
    if bool:
        return "causal"
    return "noncausal"


def statistics_main():
    read_data_to_lists_for_statistics()

    not_captured_list = list()
    correct_list = list()
    error_list = list()
    total_count = 0.0
    correct = 0.0
    error = 0.0
    not_captured_total = 0
    for index,sentence in enumerate(originalSentenceList):
        parsed_sentence = stat(sentence, originalTypeList[index])
        if parsed_sentence.has_cause_lemma():
            if parsed_sentence.is_causal():
                correct_list.append(parsed_sentence.sentence)
                correct += 1
            else:
                error_list.append(parsed_sentence.sentence)
                error += 1
            total_count += 1
        elif parsed_sentence.is_valid_from():
            if parsed_sentence.is_causal():
                correct_list.append(parsed_sentence.sentence)
                correct += 1
            else:
                error_list.append(parsed_sentence.sentence)
                error += 1
            total_count += 1
        elif parsed_sentence.is_valid_after():
            if parsed_sentence.is_causal():
                correct_list.append(parsed_sentence.sentence)
                correct += 1
            else:
                error_list.append(parsed_sentence.sentence)
                error += 1
            total_count += 1
        else:
            if parsed_sentence.is_causal():
                not_captured_list.append(parsed_sentence.sentence)
                not_captured_total +=1
    i = 0
    while i < len(error_list):
        print error_list[i]
        i += 1
    i = 0
    print "\n\nCorrect: "
    while i < len(correct_list):
        print correct_list[i]
        i += 1
    i = 0
    print "\n\n\nNot Captured: "
    while i < len(not_captured_list):
        print not_captured_list[i]
        i += 1

    print "Not captured total: " + str(not_captured_total)
    print "Total amount: " + str(total_count)
    print "Incorrect amount: " + str(error)
    print "Correct amount: " + str(correct)
    print "Percentage correct: " + str((correct / total_count) * 100)

def old_main():
    # test_sent = Sentence("He had chest pains and headaches from mold in the bedrooms.")
    # print test_sent.sentence
    # print test_sent.causal_features()
    time1 = dt.datetime.now()


    read_data_to_lists()
    read_test_data_to_lists()
    read_in_csv(testFeatureList, "traindata.csv")
    read_in_csv(originalFeatureList, "testdata.csv")

    print (dt.datetime.now() - time1).seconds

    # write_to_csv(originalSentenceList, "traindata.csv")
    # write_to_csv(testSentenceList, "testdata.csv")


    # for i in range(10):
    #     sentenceList.append(Sentence(originalSentenceList[i], originalTypeList[i]))
    #
    # count2 = 0
    # while count2 < 5:
    #     print testFeatureList[count2]
    #     count2 += 1





    errors = []
    labeled_sentence = {}
    features_sets = {}
    for index, sentence in enumerate(originalSentenceList):
        labeled_sentence[sentence] = "Cause-Effect" in originalTypeList[index]

    train_set = originalFeatureList
    test_set = testFeatureList
    classifier = nltk.NaiveBayesClassifier.train(test_set)

    print classifier.classify(Sentence("aa long as long after ").causal_features())
    print Sentence("aa long as long after").causal_features()
    print nltk.classify.accuracy(classifier, train_set)
    print classifier.show_most_informative_features()

    i = 0
    count = 0
    while i < 10:
        guess_sentence = Sentence(testSentenceList[count], testTypeList[count])
        guess = classifier.classify(guess_sentence.causal_features())
        if guess != guess_sentence.is_causal_from_dataset():
            errors.append((guess, guess_sentence.is_causal_from_dataset(), guess_sentence.causal_features(), guess_sentence.sentence))
            print guess
            print guess_sentence.is_causal_from_dataset()
            print
            i += 1
        count += 1
        print "count: ", count, "i: ", i

    for (guess, tag, features, sentence) in errors:
        print 'correct={:<8} guess={:<8s} features={:<30} sentence={:<30}'.format(tag, guess, features, sentence)




    # count = 0
    # labeled_sentences = {}
    # # features_sets = {}
    # for unknown_sentence in sentenceList:
    #     labeled_sentences[unknown_sentence.sentence] = change_to_string(unknown_sentence.is_causal_from_dataset())
    #     # features_sets[unknown_sentence.causal_features()] =
    # print labeled_sentences
    # features_set = [(Sentence(string).causal_features(), causal) for string, causal in labeled_sentences.iteritems()]
    # print features_set
    # train_sets, test_sets = features_set[1:10], features_set[:len(labeled_sentences)]
    # classifier = nltk.NaiveBayesClassifier.train(train_sets)

    # print classifier.classify(test_sent.causal_features())
    # print nltk.classify.accuracy(classifier, test_set)
    # print classifier.show_most_informative_features()




























    # relator_count = 0
    # causal_causal_verb_count = 0
    # noncausal_causal_verb_count = 0
    # noncausal_relator_count = 0
    # cause_count = 0
    # cause_count2 = 0
    # for unknown_sentence in originalSentenceList:
    #     # if unknown_sentence.is_causal_from_dataset():
    #     if unknown_sentence.is_causal_from_dataset():
    #         count+=1
    #         print unknown_sentence.sentence
    #         print "Relator name: "
    #         print unknown_sentence.feature_set.relator_name
    #         print "Root: "
    #         print unknown_sentence.feature_set.root
    #         print "Discredit Relator: "
    #         print unknown_sentence.feature_set.feature_discredit_relator
    #         print "Causal verb: "
    #         print unknown_sentence.feature_set.feature_causal_verb
    #         print "Cause in sentence: "
    #         print unknown_sentence.feature_set.feature_cause_in_sentence
    #         if unknown_sentence.feature_set.feature_causal_verb:
    #             causal_causal_verb_count += 1
    #         if unknown_sentence.feature_set.has_relator():
    #             relator_count +=1
    #         if unknown_sentence.feature_set.feature_cause_in_sentence:
    #             cause_count+=1
    #         continue
    #     # noncausal_relator_count += 1
    #     if unknown_sentence.feature_set.feature_causal_verb:
    #         noncausal_causal_verb_count +=1
    #         print "Noncausal: "
    #         print unknown_sentence.sentence
    #     if unknown_sentence.feature_set.feature_cause_in_sentence:
    #         cause_count2 +=1
    #         print "Noncausal cause: "
    #         print unknown_sentence.sentence
    #     # if relator_count > 20:
    #     #     break
    #
    #
    # # print(len(originalSentenceList))
    # # print(len(causalTrainList))
    # print relator_count
    # # print because_count
    # print noncausal_relator_count
    # print causal_causal_verb_count
    # print noncausal_causal_verb_count
    # print cause_count
    # print cause_count2
    # print count


statistics_main()