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

import os
def isImageFile(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', ".tiff"]
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in image_extensions

def addEntryInAlbumTXTFile(person, photo_path, output_directory):
    album_path = os.path.join(output_directory, person + ".txt")
    with open(album_path, "a") as album_file:
        album_file.write(linux2windows(photo_path) + "\n")
