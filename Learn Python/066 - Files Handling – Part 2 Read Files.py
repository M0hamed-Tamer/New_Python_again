# --------------------------------
# -- File Handling => Read File --
# --------------------------------

myFile = open(r"d:\Mohamed Tamer.txt", "r")

# print(myFile)  # File Data Object
# print(myFile.name)
# print(myFile.mode)
# print(myFile.encoding)

# print(myFile.read())
# print(myFile.read())

# print(myFile.readline())
# print(myFile.readline())
# print(myFile.readline())

# print(myFile.readlines())
# print(myFile.readlines())
# print(type(myFile.readlines()))

# for line in myFile:

#     print(line)

#     if line.startswith("ali"):

#         break

# # # Close The File

# myFile.close()
for x in myFile:
    print(x)