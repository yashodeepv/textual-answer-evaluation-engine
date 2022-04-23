#pip install -U sentence-transformers
#pip install transformers
#pip install sumy
#pip install nltk


import re
from flask import Flask, request
from flask_cors import CORS


from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import torch

from sumy.summarizers.lsa import LsaSummarizer 
from sentence_transformers import SentenceTransformer, util

import nltk



app = Flask(__name__)
CORS(app)


# Set up Abstractive Summarizer
model = "facebook/bart-large-cnn"
tokenizer_abstractive = AutoTokenizer.from_pretrained(model)
summarizer_abstractive = pipeline("summarization", model=model, tokenizer=tokenizer_abstractive)

nltk.download('punkt')
summarizer_extractive = LsaSummarizer()


def abstractive_summary(t) :
  return summarizer_abstractive(t)

def extractive_summary(t, c) :
  parser_extractive = PlaintextParser.from_string(t, Tokenizer("english"))
  summary = summarizer_extractive(parser_extractive.document, c) 
  sumText = ""
  for sentence in summary:
    sumText += str(sentence)
  return sumText


def summarize(t) :
  return abstractive_summary(extractive_summary(t, 15))

@app.route('/')
def hello_world():
   return "Hello World"

import json

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

@app.route('/process', methods = ['POST'])
def calculate_score():
   data1 = request.data # a multidict containing POST data
   print(data1)
   data = json.loads(data1)  
   print(data)
   text_expected = data['expectedAnswer']
   text_actual = data['actualAnswer']
   exp_sum=summarize(text_expected)
   act_sum=summarize(text_actual)
   print(exp_sum)
   print(act_sum)
   sentences = [exp_sum, act_sum]

   model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

   #Compute embedding for both lists
   embeddings= model.encode(sentences[0])
   embedding_2 = model.encode(sentences[1])
 
   res = util.cos_sim(embeddings, embedding_2)
   xx = str(res[0][0].item())
   return xx
   

if __name__ == '__main__':
   app.run()