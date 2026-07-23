# Variables
name = "Noor"
age = 21
marks = 85

print("Name:", name)
print("Age:", age)
print("Marks:", marks)


# Data Types
student_name = "Ali"      # String
student_age = 20          # Integer
percentage = 85.5         # Float
is_pass = True            # Boolean

print(type(student_name))
print(type(student_age))
print(type(percentage))
print(type(is_pass))


# Input / Output
user_name = input("Enter your name: ")
user_age = int(input("Enter your age: "))

print("Hello", user_name)
print("Your age is", user_age)


# If-Else
marks = int(input("Enter your marks: "))

if marks >= 50:
    print("You are Pass")
else:
    print("You are Fail")


# Loops
# For loop
for i in range(1, 6):
    print("Number:", i)

# While loop
count = 1
while count <= 5:
    print("Count:", count)
    count += 1


# Functions
def greet(name):
    print("Hello", name)

greet("Noor")