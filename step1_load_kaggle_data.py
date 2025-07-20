import pandas as pd

# Load Kaggle Dataset
df = pd.read_csv("data/train.csv")  # Path from project root

# Display text and category columns
print("📊 Sample Rows:")
print("📄 Columns in your CSV:")
print(df.columns)


# Lowercase text
df['text'] = df['text'].str.lower()

# Save cleaned version
df[['text', 'category']].to_csv("data/cleaned_data.csv", index=False)

print("\n✅ Cleaned dataset saved to data/cleaned_data.csv")
