nltk.download('omw-1.4')
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import pickle
model = pickle.load(open('finalized_model.pkl', 'rb'))
cv=  pickle.load(open('finalized_model_tfidf.pkl', 'rb'))
emo_la={0:'sadness',1:'joy',2:'love',3:'anger',4:'fear',5:'surprise'}

def final_preprocessed(func):
    def inner(text):
        #text=[str(i).split(".") for i in text]
        text=pd.Series(text)
        #print(text)
        text=text.apply(lambda x:func(x))
        text=text.apply(lambda x:' '.join(x))
        #print('ajjkkkkkkffkfkvgkgj')
        text = cv.transform(text)
        output=[emo_la[s] for s in model.predict(text)]
        return output
    return inner    

@final_preprocessed
def text_cleaning(x):
    sentences=[]
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for i in range(1):
        paragraph=x
        text = re.sub(r'\[[0-9]*\]',' ',paragraph)
        text =' '.join(word for word in text.split(' ') if not word.startswith('@'))
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
        sentenc = nltk.word_tokenize(text)
        #sentenc = sentenc.split()
        #print(sentenc)
        sentenc = [lemmatizer.lemmatize(sentence)  for sentence in sentenc if sentence not in stopwords.words('english')]
        #if sentence not in stopwords.words('english')
    return sentenc   
