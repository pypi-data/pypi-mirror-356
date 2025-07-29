def sentiment():
    return """

import pandas as pd
import numpy as np
import re
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


df = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/IMDB.csv")  # Make sure the file is in your working directory

df = df.sample(5000, random_state=42)

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

# 6. Preprocessing Function
def preprocess(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Keep letters only
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

# 7. Apply Preprocessing
df['clean_review'] = df['review'].apply(preprocess)

# 8. Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(max_features=1000)  # Reduce feature space for speed
X = vectorizer.fit_transform(df['clean_review'])
y = df['sentiment']

# 9. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 10. Define Classifiers
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": MultinomialNB(),
    "SVM (Linear)": SVC(kernel='linear'),
    "Random Forest": RandomForestClassifier(n_jobs=-1),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

# 11. Train and Evaluate Models
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred)
    }

# 12. Convert Results to DataFrame
results_df = pd.DataFrame(results).T
results_df = results_df.round(3)

# 13. Plot Performance
results_df.plot(kind='bar', figsize=(10, 6))
plt.title("Sentiment Analysis - Model Performance")
plt.ylabel("Score")
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 14. Print Results
print("Model Performance:\n")
print(results_df)

import pandas as pd
import numpy as np
import re
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


df = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/IMDB.csv")  # Make sure the file is in your working directory

df = df.sample(5000, random_state=42)

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

# 6. Preprocessing Function
def preprocess(text):
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Keep letters only
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

# 7. Apply Preprocessing
df['clean_review'] = df['review'].apply(preprocess)

# 8. Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(max_features=1000)  # Reduce feature space for speed
X = vectorizer.fit_transform(df['clean_review'])
y = df['sentiment']

# 9. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 10. Define Classifiers
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": MultinomialNB(),
    "SVM (Linear)": SVC(kernel='linear'),
    "Random Forest": RandomForestClassifier(n_jobs=-1),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

# 11. Train and Evaluate Models
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred)
    }

# 12. Convert Results to DataFrame
results_df = pd.DataFrame(results).T
results_df = results_df.round(3)

# 13. Plot Performance
results_df.plot(kind='bar', figsize=(10, 6))
plt.title("Sentiment Analysis - Model Performance")
plt.ylabel("Score")
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 14. Print Results
print("Model Performance:\n")
print(results_df)

"""