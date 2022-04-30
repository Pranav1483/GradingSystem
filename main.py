import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
import re
from nltk.stem.wordnet import WordNetLemmatizer
import enchant
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os
import time
import pwinput


def clrscr():
    clear = lambda: os.system("cls")
    clear()


def login():
    password = ""
    while password != "school":
        clrscr()
        print("  WELCOME\n===========\n\nUser : Administrator")
        password = pwinput.pwinput(prompt="Password : ")
        if password != "school":
            print("\nWrong Password !!\nTry Again")
        else:
            print("\nLogin Successful\nLoading Site...")
        time.sleep(3)
    clrscr()


def read_file(filename):
    model_answer = open(filename, "r")
    return model_answer.read()


def lemmatizer(words):
    l = [WordNetLemmatizer().lemmatize(w) for w in words]
    return l


def no_stopwords(words):
    s = []
    for w in words:
        if w not in stopwords.words("english"):
            s.append(w)
    return s


def misspelled(words):
    dictionary = enchant.Dict("en_IN")
    m = []
    for i in words:
        if not dictionary.check(i):
            m.append(i)
    return m


def syn_vector(obj):
    synonyms = []
    for syn in wordnet.synsets(obj):
        for i in syn.lemmas():
            synonyms.append(i.name())
    return synonyms


def unique(sequence):
    seen = set()
    return [z for z in sequence if not (z in seen or seen.add(z))]


def synonym_equaliser(text1, text2):
    for w in range(len(text2)):
        for x in range(len(unique(syn_vector(text2[w])))):
            for y in range(len(text1)):
                if unique(syn_vector(text2[w]))[x] == text1[y]:
                    text2[w] = text1[y]
    return text2


def vectorize(set_of_words, doc_text):
    vector = []
    for i in set_of_words:
        vector.append(doc_text.count(i))
    return vector


def BoW(text1, text2):
    vocab = unique(text1 + text2)
    bow1 = vectorize(vocab, text1)
    bow2 = vectorize(vocab, text2)
    return [vocab, bow1, bow2]


def marking(vocab, bow1, bow2, num_misspelled, num_word, total_marks, text1):
    sum_large = 0
    sum_small = 0
    num_large1 = 0
    num_small1 = 0
    for i in text1:
        if len(i) > 6:
            num_large1 += 1
        else:
            num_small1 += 1
    ratio = (num_small1 + num_large1)/num_large1
    coef_large = ratio*total_marks/num_word
    coef_small = total_marks/num_word
    for i in text1:
        if len(i) > 6:
            sum_large += coef_large
        else:
            sum_small += coef_small
    total = sum_small + sum_large
    change = total_marks/total
    coef_large = change*coef_large
    coef_small = change*coef_small
    student_mark = 0
    for i in range(len(vocab)):
        if bow1[i] > 0:
            if len(vocab[i]) > 6:
                student_mark += bow2[i]*coef_large
            else:
                student_mark += bow2[i]*coef_small
    student_mark = student_mark - (num_misspelled/num_word)*10
    return student_mark


# Main

login()
model_name = str(input("Enter Filename of Model Sheet : "))
answer_name = str(input("Enter Filename of Student Answer Sheet : "))

model_text = read_file(model_name)
answer_text = read_file(answer_name)

model_text_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", model_text.lower()))
answer_text_list = word_tokenize(re.sub(r"[A-Za-z\d]", " ", answer_text.lower()))

l_model = lemmatizer(model_text_list)
l_student = lemmatizer(answer_text_list)

l_s_model = no_stopwords(l_model)
l_s_student = no_stopwords(l_student)

sp_mistakes = misspelled(answer_text_list)

l_s_student1 = synonym_equaliser(l_s_model, l_s_student)
b = BoW(l_s_model, l_s_student1)

marks = marking(b[0], b[1], b[2], len(sp_mistakes), len(l_s_model), 100.0, l_s_model)
print("The Marks are : ", marks)
