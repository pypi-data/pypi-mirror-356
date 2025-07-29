def unsupervised():
    return """
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


data = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/wine-clustering.csv")
data.shape
dataTypes = data.dtypes
data.columns.tolist()
missval = data.isnull().sum()
print(missval)

missvalPerc = data.isnull().sum() / data.shape[0] * 100
print(missvalPerc)
print(data.mean())
print(data.median())
print(data.min())
print(data.max())
print(data.std())

# Scatter plot matrix for a few features
sns.pairplot(data.iloc[:, :5])  # Pair plot for first five features
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()

# Box plots for all features
# Create separate box plots for each feature
for column in data.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(y=data[column])
    plt.title(f"Box Plot for {column}")
    plt.ylabel(column)
    plt.show()

# Handle missing values (if any)
data = data.dropna()  # Drop rows with missing values (not needed here, no missing values)

from sklearn.preprocessing import StandardScaler
# Scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Convert scaled data back to DataFrame
scaled_df = pd.DataFrame(scaled_data, columns=data.columns)

# Extract the 'Color_Intensity' and 'Proline' columns for clustering
clustering_data = scaled_df[['Color_Intensity', 'Proline']]
print("Clustering data sample:")
print(clustering_data.head())



# Data for clustering (using scaled_df from preprocessing)
X = scaled_df  # Ensure data is normalized

# Calculate WCSS for different numbers of clusters
wcss = []
k_values = range(1, 11)  # Testing cluster counts from 1 to 10

for k in k_values:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)  # Append the Within-Cluster Sum of Squares (WCSS)

# Plot the Elbow Method
plt.figure(figsize=(10, 6))
plt.plot(k_values, wcss, marker='o', linestyle='--', color='b')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.xticks(k_values)
plt.grid(True)
plt.show()



# Selected features for clustering
features = scaled_df[['Color_Intensity', 'Proline']]

# Optimal number of clusters (replace 'optimal_k' with the identified value of k)
optimal_k = 3  # Example value, update based on the elbow method results
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
cluster_labels = kmeans.fit_predict(features)

# Add cluster labels to the original dataset
data['Cluster'] = cluster_labels

# Display the resulting data with cluster labels
print("Data with cluster labels:")
print(data.head())

# Cluster centers
print("Cluster Centers (scaled values):")
print(kmeans.cluster_centers_)

# Silhouette Score
from sklearn.metrics import silhouette_score
sil_score = silhouette_score(features, cluster_labels)
print(f"Silhouette Score: {sil_score:.4f}")
# Cluster Visualization
plt.figure(figsize=(8, 6))
sns.scatterplot(data=features, x='Color_Intensity', y='Proline', hue=cluster_labels, palette='Set1')
plt.title(f'K-Means Clustering (k={optimal_k})')
plt.xlabel('Color_Intensity')
plt.ylabel('Proline')
plt.legend(title='Cluster')
plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


data = pd.read_csv("D:/6th Semester/Artificial Inteligence Lab/Programs/wine-clustering.csv")
data.shape
dataTypes = data.dtypes
data.columns.tolist()
missval = data.isnull().sum()
print(missval)

missvalPerc = data.isnull().sum() / data.shape[0] * 100
print(missvalPerc)
print(data.mean())
print(data.median())
print(data.min())
print(data.max())
print(data.std())

# Scatter plot matrix for a few features
sns.pairplot(data.iloc[:, :5])  # Pair plot for first five features
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()

# Box plots for all features
# Create separate box plots for each feature
for column in data.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(y=data[column])
    plt.title(f"Box Plot for {column}")
    plt.ylabel(column)
    plt.show()

# Handle missing values (if any)
data = data.dropna()  # Drop rows with missing values (not needed here, no missing values)

from sklearn.preprocessing import StandardScaler
# Scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Convert scaled data back to DataFrame
scaled_df = pd.DataFrame(scaled_data, columns=data.columns)

# Extract the 'Color_Intensity' and 'Proline' columns for clustering
clustering_data = scaled_df[['Color_Intensity', 'Proline']]
print("Clustering data sample:")
print(clustering_data.head())



# Data for clustering (using scaled_df from preprocessing)
X = scaled_df  # Ensure data is normalized

# Calculate WCSS for different numbers of clusters
wcss = []
k_values = range(1, 11)  # Testing cluster counts from 1 to 10

for k in k_values:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)  # Append the Within-Cluster Sum of Squares (WCSS)

# Plot the Elbow Method
plt.figure(figsize=(10, 6))
plt.plot(k_values, wcss, marker='o', linestyle='--', color='b')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.xticks(k_values)
plt.grid(True)
plt.show()



# Selected features for clustering
features = scaled_df[['Color_Intensity', 'Proline']]

# Optimal number of clusters (replace 'optimal_k' with the identified value of k)
optimal_k = 3  # Example value, update based on the elbow method results
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
cluster_labels = kmeans.fit_predict(features)

# Add cluster labels to the original dataset
data['Cluster'] = cluster_labels

# Display the resulting data with cluster labels
print("Data with cluster labels:")
print(data.head())

# Cluster centers
print("Cluster Centers (scaled values):")
print(kmeans.cluster_centers_)

# Silhouette Score
from sklearn.metrics import silhouette_score
sil_score = silhouette_score(features, cluster_labels)
print(f"Silhouette Score: {sil_score:.4f}")
# Cluster Visualization
plt.figure(figsize=(8, 6))
sns.scatterplot(data=features, x='Color_Intensity', y='Proline', hue=cluster_labels, palette='Set1')
plt.title(f'K-Means Clustering (k={optimal_k})')
plt.xlabel('Color_Intensity')
plt.ylabel('Proline')
plt.legend(title='Cluster')
plt.show()





"""