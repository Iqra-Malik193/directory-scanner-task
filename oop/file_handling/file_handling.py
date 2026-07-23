# File Handling in Python

# Create and write to a file
with open("student.txt", "w") as file:
    file.write("Name: Ali\n")
    file.write("Course: BS Information Technology\n")
    file.write("Semester: 6th\n")

print("Data written successfully.")

# Read the file
with open("student.txt", "r") as file:
    print("\nReading File:")
    print(file.read())

# Append new data
with open("student.txt", "a") as file:
    file.write("University: NUML\n")

print("\nNew data appended successfully.")