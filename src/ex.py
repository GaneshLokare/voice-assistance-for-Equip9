import os

folder_path = "pred"

# Get list of all files in the folder
files = os.listdir(folder_path)

# Iterate over each file and delete it
for file in files:
    file_path = os.path.join(folder_path, file)
    os.remove(file_path)