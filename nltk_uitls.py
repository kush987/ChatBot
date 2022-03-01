import nltk
# nltk.download('punkt')
import numpy as np
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_word(tokenize_sentence,words):


    tokenize_sentence = [stem(w) for w in tokenize_sentence]
    bag = np.zeros(len(words), dtype = np.float32)
    for idx, w in enumerate(words):
        if w in tokenize_sentence:
            bag[idx] = 1
    return bag

# sentence = ['hello', 'how', ' are', 'you']
# words = ['hi', 'hello', 'I', 'you','bye', 'thank', 'cool']
# bag = bag_of_word(sentence,words)
# print("bag of words",bag)
# a = "How long does shipping take ?"
# print(a)

# a = tokenize(a)
# print(a)
# words = ["Organize", "organizes", "Chocolate", "Universe"]
# stemmed_words = [stem(w) for w in words] 
# print(stemmed_words)