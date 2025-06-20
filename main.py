import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Settings
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Load dataset
df = pd.read_csv("train.csv")

# Display initial info
print("🔹 First 5 rows of dataset:")
print(df.head())
print("\n🔹 Dataset Info:")
print(df.info())
print("\n🔹 Summary Statistics:")
print(df.describe(include='all'))
print("\n🔹 Missing Values:")
print(df.isnull().sum())

# ------------------------
# 🔹 Data Cleaning
# ------------------------

# Fix missing values
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df = df.drop(columns=['Cabin', 'Ticket'])

# ------------------------
# 🔹 Feature Engineering
# ------------------------

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = 1
df.loc[df['FamilySize'] > 1, 'IsAlone'] = 0

# Encode 'Sex'
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# One-hot encode 'Embarked'
df = pd.get_dummies(df, columns=['Embarked'], drop_first=True)

# ------------------------
# 🔹 EDA
# ------------------------

# Survival count
sns.countplot(data=df, x='Survived')
plt.title("Survival Count")
plt.show()

# Survival by Sex
sns.countplot(data=df, x='Sex', hue='Survived')
plt.title("Survival by Sex")
plt.show()

# Age distribution by survival
sns.histplot(data=df, x='Age', hue='Survived', bins=30, kde=True)
plt.title("Age Distribution by Survival")
plt.show()

# Survival rate by Pclass
sns.barplot(x='Pclass', y='Survived', data=df)
plt.title("Survival Rate by Passenger Class")
plt.show()

# Correlation heatmap (only numeric columns)
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# Age distribution by Pclass
sns.boxplot(data=df, x='Pclass', y='Age')
plt.title("Age Distribution by Class")
plt.show()

# Family size vs Survival
sns.countplot(data=df, x='FamilySize', hue='Survived')
plt.title("Survival by Family Size")
plt.show()

# ------------------------
# 🔍 Key Insights
# ------------------------
print("\n🔍 Key Insights:")
print("""
1. Females had a much higher survival rate.
2. Passengers in 1st class were more likely to survive.
3. Being alone reduced survival chances.
4. Children and young adults had higher survival.
5. Very large families (>4) had lower survival rates.
""")
