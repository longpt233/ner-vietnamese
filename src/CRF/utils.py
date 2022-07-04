import glob
import re
import pandas as pd
import swifter
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

max_len = 75


def remove_punct(word):
    res = re.sub(r'[^\w\s %,-@]', '', word)
    return res

def fix_percent(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if words[i] == '%' and words[i-1].isnumeric():
                labels[i-1] = 'B-QUANTITY-PER'
                labels[i] = 'I-QUANTITY-PER'
    return words, labels

def fix_gb(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if words[i] == 'GB' and words[i-1].isnumeric():
                labels[i-1] = 'B-QUANTITY-NUM'
                labels[i] = 'I-QUANTITY-NUM'
    return words, labels

def fix_distance(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if words[i] in ['cm', 'mm', 'km', 'm'] and words[i-1].isnumeric():
                if labels[i] == 'O':
                    labels[i-1] = 'B-QUANTITY-DIM'
                    labels[i] = 'I-QUANTITY-DIM'
    return words, labels

def fix_distance_vie(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if i + 1 < len(words):
                if words[i] in ['triệu', 'nghìn', 'ngàn', 'tỉ', 'tỷ'] and words[i-1].isnumeric() and words[i+1] in ['cm', 'mm', 'km', 'm']:
                    labels[i-1] = 'B-QUANTITY-DIM'
                    labels[i] = 'I-QUANTITY-DIM'
                    labels[i+1] = 'I-QUANTITY-DIM'
    return words, labels

def fix_currency_vie(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if i + 1 < len(words):
                if words[i] in ['triệu', 'nghìn', 'ngàn', 'tỉ', 'tỷ'] and words[i-1].isnumeric() and words[i+1] in ['đồng', "USD", 'euro']:
                    labels[i-1] = 'B-QUANTITY-CUR'
                    labels[i] = 'I-QUANTITY-CUR'
                    labels[i+1] = 'I-QUANTITY-CUR'
    return words, labels

def fix_age(words, labels):
    for i in range(len(words)):
        if i == 0:
            continue
        else:
            if words[i] == 'tuổi' and words[i-1].isnumeric():
                labels[i-1] = 'B-QUANTITY-AGE'
                labels[i] = 'I-QUANTITY-AGE'
    return words, labels

def pre_process(data_source, data_path):

    Sentence = []
    Word = []
    POS = []
    Phrase = []
    NER_main = []
    Ner_extension = []
    sent_idx = 0
    files = glob.glob(data_path + "/"+ data_source+ "/*.conll")

    for file in files:
        # print(file)
        with open(file, 'r') as f:
            full_text = f.readlines()
            for i in range(len(full_text)):
                full_text[i] = full_text[i].split('\t')
                if '.' in full_text[i] and '\n' in full_text[i + 1]:
                    sent_idx += 1
                elif '.' in full_text[i] and full_text[i + 1][0][0].isupper():
                    print(full_text[i + 1])
                    sent_idx += 1
                elif '\n' in full_text[i]:
                    sent_idx += 1
                else:
                    Sentence.append(sent_idx)
                    Word.append(full_text[i][0].replace('\ufeff', ''))
                    POS.append(full_text[i][1])
                    Phrase.append(full_text[i][2])

                    if len(full_text[i]) >= 4:
                        NER_main.append(full_text[i][3].replace('\n', ''))
                    else:
                        NER_main.append('O')

                    if len(full_text[i]) == 5:
                        Ner_extension.append(full_text[i][4].replace('\n', ''))
                    else:
                        Ner_extension.append('O') 
        
    data = pd.DataFrame.from_dict({'Sentence': Sentence,'Word': Word, 'NER_main': NER_main, \
                                    'Ner_extension': Ner_extension})
    X = data[["Sentence","Word"]]
    Y = data["NER_main"]
    
    data = pd.DataFrame({"sentence_id":X["Sentence"],"words":X["Word"],"labels":Y})
    data['words'] = data['words'].swifter.apply(remove_punct)
    data = data[data['words'] != '']
    
    # fix percent
    sentence_id = data.sentence_id.tolist()
    words = data.words.tolist()
    labels = data.labels.tolist()
    
    if data_source == 'train':
        print('load train')
        words, labels = fix_percent(words, labels)
        words, labels = fix_gb(words, labels)
        words, labels = fix_distance(words, labels)
        words, labels = fix_age(words, labels)
        words, labels = fix_distance_vie(words, labels)
        words, labels = fix_currency_vie(words, labels)
    data = pd.DataFrame.from_dict({'sentence_id': sentence_id, 'words': words, 'labels': labels})
    return data


def get_list_tag():
  labels= ['B-PERSONTYPE',
  'B-PERSON',
  'B-ORGANIZATION',
  'B-LOCATION-GPE',
  'B-LOCATION',
  'B-DATETIME',
  'B-QUANTITY',
  'B-DATETIME-DATE',
  'B-PRODUCT',
  'B-QUANTITY-AGE',
  'B-DATETIME-SET',
  'B-QUANTITY-NUM',
  'B-MISCELLANEOUS',
  'B-QUANTITY-PER',
  'B-DATETIME-TIMERANGE',
  'B-EVENT-CUL',
  'B-QUANTITY-CUR',
  'B-ORGANIZATION-STOCK',
  'B-DATETIME-TIME',
  'B-LOCATION-STRUC',
  'B-ADDRESS',
  'B-QUANTITY-ORD',
  'B-DATETIME-DURATION',
  'B-LOCATION-GEO',
  'B-EVENT',
  'B-SKILL',
  'B-URL',
  'B-QUANTITY-DIM',
  'B-EVENT-SPORT',
  'B-PRODUCT-LEGAL',
  'B-ORGANIZATION-SPORTS',
  'B-DATETIME-DATERANGE',
  'B-QUANTITY-TEM',
  'B-ORGANIZATION-MED',
  'B-EVENT-GAMESHOW',
  'B-EMAIL',
  'B-PHONENUMBER',
  'B-PRODUCT-COM',
  'B-IP',
  'B-EVENT-NATURAL',
  'B-PRODUCT-AWARD']

  return labels


def word2features(sent, i):
    word = sent[i][0] 

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(), 
    }
    if i > 0:
        word1 = sent[i-1][0] 
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(), 
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0] 
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(), 
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]