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

def saveHeadshot(person, output_directory, image, face_location):
    top, right, bottom, left = face_location
    headshot = image[top:bottom, left:right]
    headshot_path = os.path.join(output_directory, person + ".jpg")
    Image.fromarray(headshot).save(headshot_path)


def imageDetected(itemWithPath):
    try:
        image = face_recognition.load_image_file(itemWithPath)
    except Exception as e:
        print(f"Exception: {e}")
        return False
        
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    output_win = r"C:\Users\amazi\Downloads"
    output_directory = windows2linux(output_win)
    
    for i in range(len(face_locations)):
        saveHeadshot(str(i), output_directory, image, face_locations[i])
    print(face_locations)
    print(face_encodings)
    
path = r"C:\Users\amazi\Downloads\womaen.jpg"
imageDetected(windows2linux(path))