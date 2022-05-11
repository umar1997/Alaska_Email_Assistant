import os
import re
import math
import random

import pandas as pd
import numpy as np

from faker import Faker
faker = Faker(locale='en_US')


################################### process Functions
def write_to_master(dirs, filename, data):   
    if not os.path.isfile(dirs + filename):
        data.to_csv(dirs + filename)
    else:
        data.to_csv(dirs + filename, mode='a', header=False)

def cleanS(sentence):
    numbers = re.findall(r"\d+", sentence)
    if len(numbers) != 0:
        return "REMOVE TEXT"
    x = sentence.lower()
    x = re.sub(r'fw:','', x)
    x = re.sub(r're:','', x)
    x = re.sub(r'[^\w\s]', ' ', x)
    x = x.strip()
    x = re.sub(r' {2,}', ' ',x)
    return x

def cleanC(sentence):
    if '---' in sentence:
        return "REMOVE TEXT"
    
    search = re.search(r'\d\d\/\d\d', sentence)
    if search == None:
        search = re.search(r'From:', sentence)
        if search == None:
            pass
        else:
            sentence = sentence[:search.start()] 
    else:
        sentence = sentence[:search.start()] 
        
    x = sentence.lower()
    x = re.sub(r'[^\w\s]', ' ', x)
    x = x.strip()
    x = re.sub(r' {2,}', ' ',x)
    return x

def cleanSubject(row):
    try:
        if math.isnan(row):
            return "REMOVE TEXT"
        return "REMOVE TEXT" 
    except:
        x = cleanS(row)
        if (len(x.split()) <= 3) or (len(x.split()) >= 9):
            return "REMOVE TEXT"
        else:
            return x
        
        
def cleanContent(row):
    try:
        if math.isnan(row):
            return "REMOVE TEXT"
        return "REMOVE TEXT" 
    except:
        x = cleanC(row)
        if (len(x.split()) <= 8):
            return "REMOVE TEXT"
        else:
            return x
        
domains  = {'gmail.com', 'hotmail.com', 'yahoo.com'}
email_address_types = [
    faker.free_email,
    faker.email,
    faker.ascii_free_email,
    faker.ascii_safe_email,
    faker.company_email
]

# Letter Numbers to Digit Numbers
# https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers

# https://faker.readthedocs.io/en/master/providers/faker.providers.internet.html?highlight=email
def generateEmail():
    
#     num_emails = random.randint(1, 3)
    prob = random.random()
    if prob <= 0.65: num_emails=1
    elif prob <= 0.95: num_emails=2
    else: num_emails=3
        
    email_list = []
    for i in range(num_emails):
        email_list.append(faker.free_email())
    email_list = ' and '.join(email_list)
    return email_list

def getFormatted(df):

    df.drop(columns = ['Unnamed: 0', 'Message-ID', 'Date', 'From', 'To', 'X-From',
           'X-To', 'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName', 'user', 'Cat_1_level_1', 'Cat_1_level_2', 'Cat_1_weight',
           'Cat_2_level_1', 'Cat_2_level_2', 'Cat_2_weight', 'Cat_3_level_1',
           'Cat_3_level_2', 'Cat_3_weight', 'Cat_4_level_1', 'Cat_4_level_2',
           'Cat_4_weight', 'Cat_5_level_1', 'Cat_5_level_2', 'Cat_5_weight',
           'Cat_6_level_1', 'Cat_6_level_2', 'Cat_6_weight', 'Cat_7_level_1',
           'Cat_7_level_2', 'Cat_7_weight', 'Cat_8_level_1', 'Cat_8_level_2',
           'Cat_8_weight', 'Cat_9_level_1', 'Cat_9_level_2', 'Cat_9_weight',
           'Cat_10_level_1', 'Cat_10_level_2', 'Cat_10_weight', 'Cat_11_level_1',
           'Cat_11_level_2', 'Cat_11_weight', 'Cat_12_level_1', 'Cat_12_level_2',
           'Cat_12_weight', 'labeled'], inplace = True)
    print('   - Cleaning Content and Subject...')
    df['Subject'] = df['Subject'].apply(cleanSubject)
    df['content'] = df['content'].apply(cleanContent)
    
    print('   - Updating DataFrame...')
    updateDF = df[(df['content'] != "REMOVE TEXT") & (df['Subject'] != "REMOVE TEXT")]
    updateDF.reset_index(drop=True, inplace=True)
    print('   - Getting Email Addresses...')
    emailAddresses = [generateEmail() for _ in range(len(updateDF))]
    updateDF['Emails'] = pd.Series(emailAddresses)
    
    return updateDF, len(updateDF)



################################### makeData Functions
def getAugmented(s, f):
    s = s.replace('__EMAIL_ADDRESS__', f.loc['Emails'])
    s = s.replace('__SUBJECT__', f.loc['Subject'])
    s = s.replace('__CONTEXT__', f.loc['content'])
    return s

def getEmail(s, f):
    q = "What are the email addresses?"
    start_index = s.index(f.loc['Emails'])
    text = f.loc['Emails']
    a = {
        'answer_start': [start_index],
        'text': [text]
    }    
    return q, s, a

def getSubject(s, f):
    q = "What is the email subject?"
    start_index = s.index(f.loc['Subject'])
    text = f.loc['Subject']
    a = {
        'answer_start': [start_index],
        'text': [text]
    }    
    return q, s, a

def getContent(s, f):
    q = "What is the email content?"
    start_index = s.index(f.loc['content'])
    text = f.loc['content']
    a = {
        'answer_start': [start_index],
        'text': [text]
    }    
    return q, s, a