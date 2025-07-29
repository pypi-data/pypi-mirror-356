from searchlib.algorithms import astar_code
from searchlib.eda import eda_code
from searchlib.plots import plots_code
from searchlib.beam import beam_code
from searchlib.modeleval import model
from searchlib.bidirectional import bidirectional_code
from searchlib.sentiment import sentiment
from searchlib.supervised import supervised
from searchlib.unsupervised import unsupervised

def Astar():
    return astar_code()

def EDA():
    return eda_code()

def Plots():
    return plots_code()

def Beam():
    return beam_code()

def Model():
    return model()

def Bidirectional():
    return bidirectional_code()

def Sentiment():
    return sentiment()

def Supervised():
    return supervised()

def Unsupervised():
    return unsupervised()

def list_algorithms():
    return {
        "Astar()",
        "EDA()",
        "Plots()",
        "Beam()",
        "Model()",
        "Bidirectional()",
        "Sentiment()",
        "Supervised()",
        "Unsupervised()"
    }