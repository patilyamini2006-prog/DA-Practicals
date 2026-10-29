import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    "Name": ["Yamini", "Harshal", "Anjali", "Riya"],
    "Dept": ["CSE", "IT", "CSE", "IT"],
    "Marks": [85, 88, 98, 78]
})

# Display Original Data
print("Original Data:\n", df)

# Data Subsetting
print("\nSubset (Marks > 50):\n", df[df["Marks"] > 50])

# Sorting in Ascending Order
print("\nSorted by Marks (Ascending):\n", df.sort_values("Marks"))

# Sorting in Descending Order
print("\nSorted by Marks (Descending):\n",
      df.sort_values("Marks", ascending=False))

# Grouping: Average Marks by Department
print("\nGrouped (Average Marks by Department):\n",
      df.groupby("Dept")["Marks"].mean())

# Statistical Operations
print("\nMean:", df["Marks"].mean())

print("\nMedian:", df["Marks"].median())

print("\nMode:")
print(df["Marks"].mode())

