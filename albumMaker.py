import os
import face_recognition
import pickle

file_types = [".jpg", ".png", ".gif", ".bmp"]

def windows2linux(windows_path):
    drive_letter_path = windows_path.split('\\', 1)[0].rstrip(':')
    linux_path = '/mnt/' + drive_letter_path.lower() + windows_path.replace('\\', '/').lstrip('C:')
    return linux_path

def scan_photos(directory, output_directory):
    known_faces = {}  # Dictionary to store known faces and their corresponding photo locations

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if any(filename.endswith(file_type) for file_type in file_types):
            photo_path = os.path.join(directory, filename)
            
            try:
                image = face_recognition.load_image_file(photo_path)
            except Exception as e:
                print(f"Exception: {e}")
                continue
            
            image = face_recognition.load_image_file(photo_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for face_encoding in face_encodings:
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

                # Append photo location to the person's album
                album_path = os.path.join(output_directory, person + ".txt")
                with open(album_path, "a") as album_file:
                    album_file.write(photo_path + "\n")

    print("Scanning complete!")



# Provide the directory containing the photos
windows_path = r'C:\Users\amazi\Downloads\2001'

output_windows = r'C:\Users\amazi\Documents\GitHub\album-maker'

output_directory = windows2linux(output_windows)

directory = windows2linux(windows_path)
print(directory)

# scan_photos(directory, output_directory)
scan_photos(directory, output_directory)