import pickle
import time
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

from Models.questionAnswering import extractAnswers
from Models.commandClassification import get_glove_dict, getClassification
from Models.binaryClassifier import getPrediction


class Model:
    def __init__(self,):
        print('Initializing Model . . .')
        start_time = time.time()
        
        self.gloveEmbedding = get_glove_dict()
        
        with open('./../../Models/model_congif.pkl', 'rb') as f:
            count_vect, tfidf_transformer, clf = pickle.load(f)

        self.clf = clf 
        self.count_vect = count_vect
        self.tfidf_transformer = tfidf_transformer

        self.tokenizer = AutoTokenizer.from_pretrained("SpanBERT/spanbert-large-cased")
        self.model = AutoModelForQuestionAnswering.from_pretrained("./../../Models/Span_Bert/model_weights")

        self.questionList = [
            "What are the email addresses?",
            "What is the email subject?",
            "What is the email content?"
        ]

        end_time = time.time()
        epoch_mins, epoch_secs = epoch_time(start_time, end_time)
        print(f"Model Initialized | Time: {epoch_mins}m {epoch_secs}s")

    def run(self, sentence):
        # sentence = cleanSentence()
        bin_output = getPrediction(sentence, self.clf, self.count_vect, self.tfidf_transformer)
        if bin_output == 'Commands':
            command_output = getClassification(sentence, self.gloveEmbedding)
            return {"COMMANDS": command_output}
        elif bin_output == 'Emails':
            answers = {}
            for q in self.questionList:
                ans = extractAnswers(q, sentence, self.tokenizer, self.model)
                answers[q] = ans
            return {"EMAILS": answers}
        else:
            print('No Idea?')


def epoch_time(start_time, end_time):
    
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

if __name__ == "__main__":
    print('Initializing Model . . .')
    start_time = time.time()
    model = Model()
    end_time = time.time()
    epoch_mins, epoch_secs = epoch_time(start_time, end_time)
    print(f"Model Initialized | Time: {epoch_mins}m {epoch_secs}s")

    x = model.run('hey alaska could you please add umarsalman@hotmail.com')
    print(x)