def model():
    return """

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
# 1. Import Libraries
df = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/heart.csv")  
X = df.drop('target', axis=1)  
y = df['target']         


# 3. Data Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Dictionary to store results
results = {}

# Helper function to evaluate and store metrics
def evaluate_model(name, model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n{name} Classification Report:\n", classification_report(y_test, y_pred))
    
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc  # For bar chart
    
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f"{name} - Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()


# 1. K-Nearest Neighbors
evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5))

# 2. Decision Tree
evaluate_model("Decision Tree", DecisionTreeClassifier(random_state=42))

# 3. Random Forest
evaluate_model("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42))

# Optional: Add SVM, Logistic Regression, Naive Bayes for comparison
evaluate_model("SVM", SVC(kernel='linear', random_state=42))
evaluate_model("Logistic Regression", LogisticRegression(random_state=42))
evaluate_model("Naive Bayes", GaussianNB())

# 4. Plot accuracy comparison
plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values(), color='skyblue')
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison of Classifiers")
plt.ylim(0.7, 1.0)
plt.xticks(rotation=45)
plt.show()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
# 1. Import Libraries
df = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/heart.csv")  
X = df.drop('target', axis=1)  
y = df['target']         


# 3. Data Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Dictionary to store results
results = {}

# Helper function to evaluate and store metrics
def evaluate_model(name, model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n{name} Classification Report:\n", classification_report(y_test, y_pred))
    
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc  # For bar chart
    
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f"{name} - Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()


# 1. K-Nearest Neighbors
evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5))

# 2. Decision Tree
evaluate_model("Decision Tree", DecisionTreeClassifier(random_state=42))

# 3. Random Forest
evaluate_model("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42))

# Optional: Add SVM, Logistic Regression, Naive Bayes for comparison
evaluate_model("SVM", SVC(kernel='linear', random_state=42))
evaluate_model("Logistic Regression", LogisticRegression(random_state=42))
evaluate_model("Naive Bayes", GaussianNB())

# 4. Plot accuracy comparison
plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values(), color='skyblue')
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison of Classifiers")
plt.ylim(0.7, 1.0)
plt.xticks(rotation=45)
plt.show()


"""