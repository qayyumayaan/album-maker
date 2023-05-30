from coreDependencies import windows2linux, linux2windows, isImageFile, addEntryInAlbumTXTFile
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
            if not isImageFile(item):
                with open(os.path.join(output_directory, "Unprocessed.txt"), "a") as album_file:
                    album_file.write(linux2windows(itemWithPath) + "\n")
            elif not item.startswith("._"):
                imageDetected(itemWithPath)
                    
                    
def imageDetected(itemWithPath):
    try:
        image = face_recognition.load_image_file(itemWithPath)
    except Exception as e:
        print(f"Exception: {e}")
        return False
        
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    for i in range(len(face_locations)):
        person = face_encodings[i]
        for j in range(numDictionaryFaces):
            match = face_recognition.compare_faces(knownFacesLibrary[j], person)
            if (match):
                addEntryInAlbumTXTFile(person, itemWithPath, output_directory)
                

def importDictionary(inputDictPath):
    for item in os.listdir(inputDictPath):
        itemWithPath = os.path.join(inputDictPath, item)
        if isImageFile(item):
            headshot = face_recognition.load_image_file(itemWithPath)
            knownFacesLibrary[numFaces] = face_recognition.face_encodings(headshot)[0]
            numFaces += 1
        
    
knownFacesLibrary = 0
numDictionaryFaces = 0
inputDictPath = windows2linux(r"C:\Users\amazi\Downloads\important-people\candidates\actual")
output_directory = windows2linux(r"C:\Users\amazi\Downloads\output")
input_directory = windows2linux(r"C:\Users\amazi\Downloads\test")