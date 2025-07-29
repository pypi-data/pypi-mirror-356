def plots_code():
    return """
import matplotlib.pyplot as plt
import seaborn as sns

for feature in data:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=data[feature])
    plt.title(f'Box Plot for {feature}')
    plt.show()
    plt.tight_layout()

for feature in data:
    plt.figure(figsize=(10, 5))
    sns.histplot(data[feature], bins=20, kde=True)
    plt.title(f'Distribution Plot for {feature}')
    plt.show()
    plt.tight_layout()

corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix")
plt.show()

diabetes_counts = df['Outcome'].value_counts()
labels = ['Non-Diabetic', 'Diabetic']
plt.figure(figsize=(6, 6))
plt.pie(diabetes_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'salmon'])
plt.title("Distribution of Diabetic vs. Non-Diabetic")
plt.axis('equal')
plt.show()
"""