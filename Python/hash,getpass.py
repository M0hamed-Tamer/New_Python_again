
import hashlib , getpass

password = getpass.getpass("Enter the pass: ")
hash_pass = hashlib.sha256 (password.encode())

# # print(f"The Password --> {password}\nThe Hash password--> {hash_pass}\nand ==> {len(hash_pass)}")#{len(hash_pass)} دايما 64 

# file = open("one_file.txt", "+")
# file.write(hash_pass)
# file.write("\n------------\n")
# file.write(password)

print(hash_pass)
