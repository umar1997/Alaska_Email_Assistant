import pandas as pd
import random

from functions import *

dirs = './../Data/'

df = pd.read_csv(dirs + 'Master.csv')


appendDF = pd.read_csv(dirs + 'Append.csv')
appendDF = appendDF.apply(lambda x: x.str.strip())
augment = list(appendDF['Append'])

allEmails = []
allContent = []
allSubject = []

allQuestion = []
allContext = []
allAnswer = []


for i, f in df.iterrows():
    s = random.choice(augment)
    s = getAugmented(s, f)
    q, c, a = getEmail(s, f)
    allQuestion.append(q)
    allContext.append(c)
    allAnswer.append(a)
    
    q, c, a = getSubject(s, f)
    allQuestion.append(q)
    allContext.append(c)
    allAnswer.append(a)
    
    q, c, a = getContent(s, f)
    allQuestion.append(q)
    allContext.append(c)
    allAnswer.append(a)
    for _ in range(3):
        allEmails.append(f.loc['Emails'])
        allContent.append(f.loc['content'])
        allSubject.append(f.loc['Subject'])
    
DF = pd.DataFrame()
DF['answer'] = pd.Series(allAnswer)
DF['context'] = pd.Series(allContext)
DF['question'] = pd.Series(allQuestion)
DF['email_addresses'] = pd.Series(allEmails)
DF['subject'] = pd.Series(allSubject)
DF['body'] = pd.Series(allContent)


DF.to_csv(dirs + 'Final.csv')