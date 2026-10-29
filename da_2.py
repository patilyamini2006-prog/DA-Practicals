import pandas as pd

# Function to calculate average
def calculate_average(marks):
    return sum(marks) / len(marks)


# User Input
n = int(input("Enter number of students: "))

names = []
marks = []

for i in range(n):
    name = input("Enter student name: ")
    mark = float(input("Enter marks: "))

    names.append(name)
    marks.append(mark)


# Create Dataset
df = pd.DataFrame({
    "Name": names,
    "Marks": marks
})


# Function to calculate result
def result(mark):
    if mark >= 75:
        return "Distinction"
    elif mark >= 50:
        return "Pass"
    else:
        return "Fail"


# Apply condition to dataset
df["Result"] = df["Marks"].apply(result)


# Display Dataset
print("\nDataset:")
print(df)


# Loop for processing values
print("\nStudent Analysis:")

for mark in marks:
    if mark >= 75:
        print(mark, "Distinction")
    elif mark >= 50:
        print(mark, "Pass")
    else:
        print(mark, "Fail")


# Statistical Analysis
print("\nAverage Marks:", calculate_average(marks))
print("Highest Marks:", max(marks))
print("Lowest Marks:", min(marks))

