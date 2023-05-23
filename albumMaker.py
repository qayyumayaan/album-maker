import os
import face_recognition
from PIL import Image

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

def saveFirstImage(person, output_directory, image):
    first_image_path = os.path.join(output_directory, person + " first_image.jpg")
    Image.fromarray(image).save(first_image_path)


def saveHeadshot(person, output_directory, image, face_location):
    top, right, bottom, left = face_location
    headshot = image[top:bottom, left:right]
    headshot_path = os.path.join(output_directory, person + ".jpg")
    Image.fromarray(headshot).save(headshot_path)


def addEntryInAlbumTXTFile(person, photo_path, output_directory):
    album_path = os.path.join(output_directory, person + ".txt")
    with open(album_path, "a") as album_file:
        album_file.write(linux2windows(photo_path) + "\n")


def directorySearch(directory):
    for item in os.listdir(directory):
        itemWithPath = os.path.join(directory, item)
        if os.path.isdir(itemWithPath):
            directorySearch(itemWithPath)
            
        elif os.path.isfile(itemWithPath):
            if isImageFile(item):
                if not item.startswith("._"):
                    imageDetected(itemWithPath)
            else:
                with open(os.path.join(output_directory, "Unprocessed.txt"), "a") as album_file:
                    album_file.write(linux2windows(itemWithPath) + "\n")
                
            

def isImageFile(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', ".tiff"]
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in image_extensions

def imageDetected(itemWithPath):
    image = face_recognition.load_image_file(itemWithPath)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)

        if any(matches):
            # Face is already known, find the matching person
            face_index = matches.index(True)
            person = list(known_faces.keys())[face_index]
            addEntryInAlbumTXTFile(person, itemWithPath, output_directory)

        else:
            # Face is unknown, create a new person entry
            person = "Person " + str(len(known_faces) + 1)
            known_faces[person] = face_encoding
            
            saveFirstImage(person, output_directory, image)

            saveHeadshot(person, output_directory, image, face_location)
            
            addEntryInAlbumTXTFile(person, itemWithPath, output_directory)


# Example usage
windows_path = r'E:\Pictures'
output_windows = r'C:\Users\amazi\Downloads\people-album'
output_directory = windows2linux(output_windows)
directory = windows2linux(windows_path)

known_faces = {} 

try:
    directorySearch(directory)
    print("Success!")
    import pickle
    outputPickleLocation = os.path.join(output_directory, "known_faces.pickle")
    with open(outputPickleLocation, 'wb') as file:
        pickle.dump(known_faces, file)
except Exception as e:
    print(f"Exception: {e}")