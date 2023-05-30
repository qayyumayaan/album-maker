from coreDependencies import windows2linux, linux2windows, isImageFile
import os
import face_recognition
from PIL import Image

def directorySearch(directory):
    print(directory)
    for item in os.listdir(directory):
        itemWithPath = os.path.join(directory, item)
        if os.path.isdir(itemWithPath):
            directorySearch(itemWithPath)
            print(directory)
            
        elif os.path.isfile(itemWithPath):
            if isImageFile(item):
                if not item.startswith("._"):
                    imageDetected(itemWithPath)
            else:
                with open(os.path.join(output_directory, "Unprocessed.txt"), "a") as album_file:
                    album_file.write(linux2windows(itemWithPath) + "\n")
                    
                    
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
    
# def importDictionary(inputDictPath):
    

inputDictPath = windows2linux(r"C:\Users\amazi\Downloads\important-people\candidates\actual")
output_directory = windows2linux(r"C:\Users\amazi\Downloads\output")
input_directory = windows2linux(r"C:\Users\amazi\Downloads\test")