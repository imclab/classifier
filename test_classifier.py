import os
import os.path as path
import re
import codecs
from classifier import Classifier
from train_classifier import token_iterator, TOKEN_PATTERN, TEST_FILE

if __name__ == "__main__":
    c = Classifier()
    c.load_model("char_level_classifier.json")
    test_file = TEST_FILE
    
    # Grab all test data from the file.
    test_data = []
    actual_class = []
    with codecs.open(test_file, 'r', 'utf-8') as f:
        for line in f:
            class_name, text = line.split('\t', 1)
            text = text.strip()
            token_list = []
            for token in token_iterator(text, TOKEN_PATTERN):
                token_list.append(token)
            test_data.append(token_list)
            actual_class.append(class_name)
    
    classifier_data_directory = 'classifiers_data'
    if not path.exists(classifier_data_directory):
        os.mkdir(classifier_data_directory)
    
    
    print "Number of test documents:", len(test_data)
    # Use a suite of classifiers and gather statistics.
    classifiers = [
        ('random classifier', c.classify_random),
        ('greedy', c.classify_greedy),
        ('naive classifier no smoothing', c.classify),
        ('one word token classifier no smoothing', c.classify_prev_token),
        ('two word token classifier no smoothing', c.classify_prev_prev_token),
        ('naive classifier with smoothing', c.classify_plus_one),
        ('one word token classifier with smoothing', c.classify_prev_token_plus_one),
        ('two word token classifier with smoothing', c.classify_prev_prev_token_plus_one),
        ('assume_seen', c.classify_assume_seen),
        ('assume_seen one prev word token', c.classify_assume_seen_prev),
        ('assume_seen two prev word token', c.classify_assume_seen_prev_prev),
        #~ ('semi-supervised', c.classify_semi_supervised),
    ]
    for classifier_name, classifier in classifiers:
        confusion_matrix = {} # TODO save confusion_matrices for write-up
        confused_documents = [] # TODO save mis-classified text to file
        success_count = 0
        for i, token_list in enumerate(test_data):
            predicted_class = classifier(token_list)
            if actual_class[i] == predicted_class:
                success_count += 1
            else:
                key = (actual_class[i], predicted_class)
                confusion_matrix[key] = confusion_matrix.setdefault(key, 0) + 1
                confused_documents = [actual_class[i], predicted_class, ''.join(token_list)]
        # Print output
        print "Percent Success ("+str(classifier_name)+"):", str(float(success_count)/float(len(test_data)))
        #~ print "Confused:", confusion_matrix
