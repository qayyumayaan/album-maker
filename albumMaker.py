import os
import face_recognition
from PIL import Image
from tqdm import tqdm as tqdm_progress

file_types = [".jpg", ".png", ".gif", ".bmp", ".tiff"]

def windows2linux(windows_path):
    drive, path = windows_path[0], windows_path[3:]
    path = path.replace("\\", "/")
    linux_path = "/mnt/{}/{}".format(drive.lower(), path)
    return linux_path

def linux2windows(linux_path):
    path_components = linux_path.split("/")
    drive, path = path_components[2], "/".join(path_components[3:])
    path = path.replace("/", "\\")
    windows_path = "{}:\\{}".format(drive.upper(), path)
    return windows_path

def scan_photos(directory, output_directory):
    known_faces = {}  # Dictionary to store known faces and their corresponding photo locations

    file_list = os.listdir(directory)


    # Loop through all files in the directory
    for filename in tqdm_progress(file_list):
            
        if filename.startswith("._"):
            continue

        if not any(filename.lower().endswith(file_type.lower()) for file_type in file_types):
            print("not processed: " + filename)
        else:
            photo_path = os.path.join(directory, filename)
            
            try:
                image = face_recognition.load_image_file(photo_path)
            except Exception as e:
                print(f"Exception: {e}")
                continue
            
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Check if the face is already known
                matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)

                if any(matches):
                    # Face is already known, find the matching person
                    face_index = matches.index(True)
                    person = list(known_faces.keys())[face_index]
                else:
                    # Face is unknown, create a new person entry
                    person = "Person " + str(len(known_faces) + 1)
                    known_faces[person] = face_encoding
                    
                    # Save the first image of the person
                    first_image_path = os.path.join(output_directory, person + "_first_image.jpg")
                    Image.fromarray(image).save(first_image_path)

                    # Save the headshot of the person
                    top, right, bottom, left = face_location
                    headshot = image[top:bottom, left:right]
                    headshot_path = os.path.join(output_directory, person + ".jpg")
                    Image.fromarray(headshot).save(headshot_path)

                # Append photo location to the person's album
                album_path = os.path.join(output_directory, person + ".txt")
                with open(album_path, "a") as album_file:
                    album_file.write(linux2windows(photo_path) + "\n")

    print("Processing complete!")



# Provide the directory containing the photos
windows_path = r'C:\Users\amazi\Downloads\2001'
output_windows = r'C:\Users\amazi\Downloads\people-album'

output_directory = windows2linux(output_windows)
directory = windows2linux(windows_path)

scan_photos(directory, output_directory)

