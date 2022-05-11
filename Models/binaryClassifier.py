import pickle
    
def getPrediction(s, clf, count_vect, tfidf_transformer):
    sentence =[s]
    cv_output = count_vect.transform(sentence)
    tfidf_output = tfidf_transformer.transform(cv_output)
    return clf.predict(tfidf_output)[0]


if __name__ == "__main__": 
    with open('./../../Models/model_congif.pkl', 'rb') as f:
        count_vect, tfidf_transformer, clf = pickle.load(f)

    x = getPrediction('please give me a new screen')
    print(x)