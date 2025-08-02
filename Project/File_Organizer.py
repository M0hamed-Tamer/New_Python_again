import os
import shutil

# أنواع الملفات
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar"],
    "Scripts": [".py", ".sh", ".bat"]
}

def organize_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            for category, extensions in FILE_TYPES.items():
                if ext.lower() in extensions:
                    target_folder = os.path.join(folder_path, category)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, file))
                    print(f"Moved {file} → {category}")
                    break

if __name__ == "__main__":
    path = os.getcwd ()
    organize_folder(path)
    print("!The files are organized smoothly.")
