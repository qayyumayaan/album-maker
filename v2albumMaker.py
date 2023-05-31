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
                with open(os.path.join(outputDir, "Unprocessed.txt"), "a") as album_file:
                    album_file.write(linux2windows(itemWithPath) + "\n")
            elif not item.startswith("._"):
                imageDetected(itemWithPath)
                    
                    
def imageDetected(itemWithPath):
    global numDictFaces
    global knownFaces
    try:
        image = face_recognition.load_image_file(itemWithPath)
    except Exception as e:
        print(f"Exception: {e}")
        return False
        
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    for i in range(len(face_locations)):
        person = face_encodings[i]
        for j in range(numDictFaces):
            match = face_recognition.compare_faces(knownFaces[j], person)
            if (match):
                addEntryInAlbumTXTFile(person, itemWithPath, outputDir)
                

def importDictionary(inputDictPath):
    global knownFaces
    global numDictFaces
    for item in os.listdir(inputDictPath):
        itemWithPath = os.path.join(inputDictPath, item)
        if isImageFile(item):
            headshot = face_recognition.load_image_file(itemWithPath)
            face_encodings = face_recognition.face_encodings(headshot)
            if len(face_encodings) > 0:
                knownFaces[numDictFaces] = face_encodings[0]
                numDictFaces += 1
            else:
                print("No face found in", item)
        
    
knownFaces = {}
numDictFaces = 0
inputDictPath = windows2linux(r"C:\Users\amazi\Downloads\important-people\candidates\actual")
outputDir = windows2linux(r"C:\Users\amazi\Downloads\output")
inputDir = windows2linux(r"C:\Users\amazi\Downloads\test")


import pickle
outputPickleLocation = os.path.join(outputDir, "knownFaces.pickle")
if os.path.exists(outputPickleLocation):
    with open(outputPickleLocation, 'rb') as file:
        knownFaces = pickle.load(file)
else: 
    importDictionary(inputDictPath)
    with open(outputPickleLocation, 'wb') as file:
        pickle.dump(knownFaces, file)

directorySearch(inputDir)