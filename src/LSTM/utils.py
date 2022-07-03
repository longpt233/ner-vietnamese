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

def pre_process():
    PREFIX_PATH = "/content/drive/MyDrive/ner-vietnamese/data/final/conll/*.conll"
  
    Sentence = []
    Word = []
    POS = []
    Phrase = []
    NER_main = []
    Ner_extension = []
    sent_idx = 0
    files = glob.glob(PREFIX_PATH)

    for file in files:
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
    
    
    words, labels = fix_percent(words, labels)
    words, labels = fix_gb(words, labels)
    words, labels = fix_distance(words, labels)
    words, labels = fix_age(words, labels)
    words, labels = fix_distance_vie(words, labels)
    words, labels = fix_currency_vie(words, labels)
    data = pd.DataFrame.from_dict({'sentence_id': sentence_id, 'words': words, 'labels': labels})
    return data


def process_data(df, sentences):
    # Xây dựng vocab cho word và tag
    words = list(df['words'].unique())
    tags = list(df['labels'].unique())

    # Tạo dict word to index, thêm 2 từ đặc biệt là Unknow và Padding
    word2idx = {w : i + 2 for i, w in enumerate(words)}
    word2idx["UNK"] = 1
    word2idx["PAD"] = 0

    # Tạo dict tag to index, thêm 1 tag đặc biệt và Padding
    tag2idx = {t : i + 1 for i, t in enumerate(tags)}
    tag2idx["PAD"] = 0

    # Tạo 2 dict index to word và index to tag
    idx2word = {i: w for w, i in word2idx.items()}
    idx2tag = {i: w for w, i in tag2idx.items()}

    # Chuyển các câu về dạng vector of index
    X = [[word2idx[w[0]] for w in s] for s in sentences]
    # Padding các câu về max_len
    X = pad_sequences(maxlen = max_len, sequences = X, padding = "post", value = word2idx["PAD"])
    # Chuyển các tag về dạng index
    y = [[tag2idx[w[1]] for w in s] for s in sentences]
    # Tiền hành padding về max_len
    y = pad_sequences(maxlen = max_len, sequences = y, padding = "post", value = tag2idx["PAD"])

    # Chuyển y về dạng one-hot
    num_tag = df['labels'].nunique()
    y = [to_categorical(i, num_classes = num_tag + 1) for i in y]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)

    # Save data
    return X_train, X_test, y_train, y_test, word2idx, tag2idx, idx2word, idx2tag, num_tag, words, tags






    