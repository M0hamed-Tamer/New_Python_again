class Profile:
    def __init__(self, user,gmail,language):
        """
        Initialize a new Profile instance.

        Args:
            user (str): The name of the user.
            gmail (str): The Gmail address of the user.
            language (int): The preferred language of the user.
        """
        self.user = user
        self.gmail = gmail
        self.language = language

# Collect user input
def User():
    user = input("Enter the name of the user: ")
    gmail = input("Enter the Gmail address: ")
    language = int(input("Enter the preferred language: "))
    return Profile(user,gmail,language)
# Create a Profile instance

profile=User()
# Print the attributes of the Profile instance
print(f"\nUser: {profile.user}")
print(f"Gmail: {profile.gmail}")
print(f"Language: {profile.language}")
