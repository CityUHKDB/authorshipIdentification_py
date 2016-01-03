import itertools
import nltk
import numpy
import re
import os
import math
from collections import Counter
from bigram import Bigram


class Paragraph:

        def __init__(self, doc, para_no, para=[]):
            """
                Constructor of Paragraph class

            """
            """ The meta-data of the document """
            self.document = doc
            self.para_no = para_no
            self.file_path = ""

            """ Unhandled raw paragraph """
            self.paragraph = para

            """ Tagging the part of speech of each word in the paragraph and count the frequency """
            self.tagged_tokens = [] #nltk.pos_tag(self.paragraph)
            self.pos_counter = Counter(tag for word, tag in self.tagged_tokens)

            """ Extracting the word in paragraph and count the length """
            self.words_list = [word for word in self.paragraph if re.match(r'.*\w', word)]
            self.words_length = [len(word) for word in self.words_list]
            self.low_case_words_list = [word.lower() for word in self.words_list]
            self.char_list = list(itertools.chain(*self.words_list))
            self.word_occurrence = self.get_dict_of_word_and_occurrence()
            print self.word_occurence.values().count(1)

            self.write_paragraph_to_file()

        def write_paragraph_to_file(self):
            path = "/tmp/pladetect/{}/".format(self.document.get_doc_title())
            if not os.path.exists(path):
                os.makedirs(path)

            self.file_path = path + "paragraph_{}.txt".format(self.para_no)
            with open(self.file_path, 'w') as paragraph_file:
                paragraph_file.write(u' '.join(self.paragraph).encode('utf-8'))

        def get_para_insert_query(self):
            return "INSERT INTO paragraph(doc_id, chapter_id, path) " \
                   "VALUES (currval('document_doc_id_seq'), currval('chapter_chapter_id_seq'), '{}');\n"\
                    .format(self.file_path)

        def get_dict_of_word_and_occurrence(self):
            word = []
            no_of_occurrence = []
            for item in sorted(set(self.low_case_words_list)):
                word.append(item)
                no_of_occurrence.append(self.low_case_words_list.count(item))
            return dict(zip(word, no_of_occurrence))

        def get_total_no_of_words(self):
            return len(self.low_case_words_list)

        def get_total_no_of_distinct_words(self):
            return len(set(self.low_case_words_list))

        def get_vocabulary_richness(self):
            return float(self.get_total_no_of_distinct_words()) / float(self.get_total_no_of_words())

        def get_K_vocabulary_richness(self):
            total = 0
            for val in self.word_occurence.values():
                total += val * val
            return float(math.pow(10, 4) * (total - self.get_total_no_of_words())) / float(math.pow(self.get_total_no_of_words(), 2))

        def get_R_vocabulary_richness(self):
            return float(self.get_total_no_of_distinct_words()) / float(math.sqrt(self.get_total_no_of_words()))

        def get_C_vocabulary_richness(self):
            return float(math.log(self.get_total_no_of_distinct_words())) / float(math.log(self.get_total_no_of_words()))

        def get_H_vocabulary_richness(self):
            return float(100 * math.log(self.get_total_no_of_words())) / float(1 - self.word_occurrence.values().count(1) / self.get_total_no_of_distinct_words())

        def get_S_vocabulary_richness(self):
            return float(self.word_occurrence.values().count(2)) / float(self.get_total_no_of_distinct_words())

        def get_k_vocabulary_richness(self):
            return float(math.log(self.get_total_no_of_distinct_words())) / float(math.log(float(math.log(self.get_total_no_of_words()))))

        def get_LN_vocabulary_richness(self):
            return float(1 - math.pow(self.get_total_no_of_distinct_words(), 2)) / float(math.pow(self.get_total_no_of_distinct_words(), 2) * math.log(self.get_total_no_of_words()))

        def get_entropy(self):
            total = 0
            for val in self.word_occurrence.values():
                total += ((float(val) / float(self.get_total_no_of_words())) * math.log(float(val) / float(self.get_total_no_of_words())))
            return -100 * float(total)

        def get_average_word_length(self):
            return numpy.mean(self.words_length)

        def get_stddev_of_word_length(self):
            return numpy.std(self.words_length)

        def get_total_no_of_character(self):
            return sum(self.words_length)

        def get_total_no_of_english_character(self):
            eng_list = [char for char in self.char_list if re.match('[a-zA-Z]', char)]
            return len(eng_list)

        def get_total_no_of_special_character(self):
            special_list = [char for char in self.char_list if re.match('\W', char)]
            return len(special_list)

        def get_total_no_of_uppercase_character(self):
            uppercase_list = [char for char in self.char_list if char.isupper()]
            return len(uppercase_list)

        def get_total_no_of_lowercase_character(self):
            lowercase_list = [char for char in self.char_list if char.islower()]
            return len(lowercase_list)

        def get_total_no_of_digital_character(self):
            digit_list = [char for char in self.char_list if char.isdigit()]
            return len(digit_list)

        def get_total_no_of_sentences(self):
            """
                Still have some problems
            """
            return len(self.paragraph)

        def get_average_no_of_words_per_sentence(self):
            """
                Still have some problems
            """
            return numpy.mean([len(sen) for sen in self.paragraph])

        def get_freq_of_nouns(self):
            return self.pos_counter['NN']

        def get_freq_of_proper_nouns(self):
            return self.pos_counter['NP']

        def get_freq_of_adj(self):
            return self.pos_counter['JJ']

        def get_freq_of_adv(self):
            return self.pos_counter['RB']

        def get_freq_of_wh_words(self):
            return self.pos_counter['WH']

        def get_freq_of_verbs(self):
            return self.pos_counter['V'] + self.pos_counter['VD'] + self.pos_counter['VG'] + self.pos_counter['VN']

        def get_bigrams(self):
            bigram_list = []
            for bigram in nltk.bigrams(self.low_case_words_list):
                bigram_list.append(Bigram(bigram))
            return bigram_list