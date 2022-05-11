import nltk
# nltk.download('stopwords')

import re
import operator
import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

# dir_path = os.path.dirname(os.path.realpath('./../Data_Processing/'))
# sys.path.append(dir_path)
# from Data_Processing.functions import generateEmail

def get_glove_dict():
    glove_dict = {}
    with open("./../../GloVe/glove.6B.50d.txt", "r", encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            glove_dict[word] = vector
            
    f.close()
    
    return glove_dict


def calcEmbedding(s, embeddingDict, gloveEmbedding):
    stopwordList= set(stopwords.words('english'))
    triggerTerms = ['hey', 'hi', 'alaska']
    w2Vec_word = np.zeros(50, dtype="float32")
    word_in_model = 0
    solutionDict = {}
    
    s = s.lower()
    s = re.split(' |\.|@', s)
    for t in triggerTerms:
        try:
            s.remove(t)
        except:
            pass
    for term in s:
        if term not in stopwordList:
            if term in gloveEmbedding:
                w2Vec_word = np.add(w2Vec_word, gloveEmbedding[term])
                word_in_model += 1
    w2Vec_word = np.divide(w2Vec_word, word_in_model)
            
    for key, value in embeddingDict.items():
        c = cosine_similarity(embeddingDict[key].reshape(1,-1), w2Vec_word.reshape(1,-1)).flatten()[0]
        solutionDict[key] = c
    
    return max(solutionDict.items(), key=operator.itemgetter(1))[0]
    
    

def getClassification(sentence, gloveEmbedding):
    commandDict = {
        'ADD EMAIL ADDR': ['hotmail', 'yahoo', 'gmail', 'com', 'addresses', 'recipients'],
        'CLEAR EMAIL': ['clear', 'remove', 'screen', 'new', 'empty'],
        'SEND EMAIL': ['send'],
        'ADD ATTACHMENT': ['add', 'attachment'],
        'ADD SIGNATURE' : ['signature'],
        'ADD SALUTATION' : ['greeting', 'salutation']
    }

    w2Vec_word = np.zeros(50, dtype="float32")
    word_in_model = 0
    embeddingDict = {}
    for key, value in commandDict.items():
        for v in value:
            if v in gloveEmbedding:
                w2Vec_word = np.add(w2Vec_word, gloveEmbedding[v])
                word_in_model += 1
            else:
                print('No Word')
        w2Vec_word = np.divide(w2Vec_word, word_in_model)
        embeddingDict[key] = w2Vec_word
    
    return calcEmbedding(sentence, embeddingDict, gloveEmbedding)

if __name__ == "__main__": 
    
    sentence = 'please clear the entire screen for me'
    gloveEmbedding = get_glove_dict()
    print(getClassification(sentence, gloveEmbedding))