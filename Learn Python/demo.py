import os
import shutil

print(os.getcwd())

path = os.path.dirname(os.path.realpath(__file__))


for file in os.listdir(path):
    # if file.endswith(('.jpg', '.png')):
    #     if not os.path.exists("../Octocode/Images"):
    #         os.mkdir("../Octocode/Images")
    #         shutil.copy(file, "../Octocode/Images")
    #         os.remove(file)
    #         print(f"{file} ----> Done")

    if file.endswith(('.py', 'py')):
        if not os.path.exists("python"):
            os.mkdir("python")
        shutil.copy(file, "python")
        os.remove(file)
        print(f"{file} ----> Done")

    # if file.endswith(('.jpg', '.png')):
    #     if not os.path.exists("Images"):
    #         os.mkdir("Images")
    #         shutil.copy(file, "Images")
    #         os.remove(file)
    #         print(f"{file} ----> Done")
    #     
    # if file.endswith(('.jpg', '.png')):
    #     if not os.path.exists("Images"):
    #         os.mkdir("Images")
    #         shutil.copy(file, "Images")
    #         os.remove(file)
    #         print(f"{file} ----> Done")