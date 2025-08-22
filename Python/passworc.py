import random
import string

# Function to generate a strong password

x=int(input("Enter The Length The Password? "))
def generate_strong_password(length=x):

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Generate a strong password of length 16
strong_password = generate_strong_password()
print(strong_password)