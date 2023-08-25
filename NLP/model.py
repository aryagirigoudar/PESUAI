from json import load
from numpy import array, dot, asarray, exp
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

# 'remainder', 'question', 'status', 'collage'
classes = ['remainder', 'question', 'status', 'collage']
words = ['had', "'", 'in', 'for', 'me', 'dat', 'i', 'stat', 'ar', 'which', 'ev', 'holiday', 'that', 'grad', 'it', 'we', 'plac', 'al', 'tel', 'string', 'syllab', 'a', 'is', 'when', 'my', 'of', 'hap', 'subject', 'cgpa', 'cur', 'weath', "'s", 'what', 'int', 'on', 'visit', 'company', 'sem', 'do', 'formul', "'int", 'thi', 's', 'today', 'the', 'remaind', 'hav', 'mark', 'wil', '’', 'set', 'did']
# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)
 
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(array(bag))

def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(dot(l1, synapse_1))
    return l2

# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses.json' 
with open(synapse_file) as data_file: 
    synapse = load(data_file) 
    synapse_0 = asarray(synapse['synapse0']) 
    synapse_1 = asarray(synapse['synapse1'])

def classify(sentence, show_details=False):
    results = think(sentence, show_details)

    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[classes[r[0]],r[1]] for r in results]
    # print ("%s \n classification: %s" % (sentence, return_results))
    return return_results

print()
print(classify("whats the weather")) # [['question', 0.9987833380222648]]
