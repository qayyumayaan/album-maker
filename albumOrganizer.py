import os
import shutil

def move_single_link_files(source_folder):
    destination_folder = os.path.join(source_folder, 'justOnce')
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get a list of all files in the source folder
    file_list = os.listdir(source_folder)

    # Iterate over each file in the source folder
    for file_name in file_list:
        file_path = os.path.join(source_folder, file_name)

        # Check if the file is a regular file
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            # Open the file and read its contents
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Check the number of lines in the file
            if len(lines) == 1:
                # Move the file to the destination folder
                shutil.move(file_path, os.path.join(destination_folder, file_name))
    print("Success!")

# Usage example
source_folder = r'C:\Users\amazi\Downloads\tmp'

move_single_link_files(source_folder)
