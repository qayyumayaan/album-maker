import os
import shutil

def move_single_link_files(source_folder):
    # Recursively search through the folders
    for root, dirs, files in os.walk(source_folder):
        print(root)
        destination_folder = os.path.join(root, 'justOnce')
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Check if the file is a regular file
            if os.path.isfile(file_path) and file_name.endswith('.txt'):
                # Open the file and read its contents
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Check the number of lines in the file
                if len(lines) == 1:
                    # Move the .txt file to the destination folder
                    shutil.move(file_path, os.path.join(destination_folder, file_name))

                    # Move the corresponding image file if it exists
                    image_file = os.path.splitext(file_path)[0] + ' first_image.jpg'
                    if os.path.exists(image_file):
                        shutil.move(image_file, os.path.join(destination_folder, os.path.basename(image_file)))

                    # Move the corresponding image file if it exists
                    image_file = os.path.splitext(file_path)[0] + '.jpg'  # Assuming the images have .jpg extension
                    if os.path.exists(image_file):
                        shutil.move(image_file, os.path.join(destination_folder, os.path.basename(image_file)))
    print("Success!")

# Usage example
source_folder = r'C:\Users\amazi\Downloads\tmp'

move_single_link_files(source_folder)