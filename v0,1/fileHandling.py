import os
import shutil

####------------EXCEPTIONS--------------####

class PathError(Exception):
    pass

####------------\EXCEPTIONS-------------####


## current working dir
cwd = os.getcwd()

## file destination
DEST_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/sample destination/"
LOG_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/log.txt"
## change dir to source
# os.chdir(sourcePath)
SOURCE_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/sample source/"


## destFileFolderExtractor: Returns a list with the folders and files in destPath
## (Str) -> List(Int, Str)
## eReqs:    destPath must be a String
## iReqs:    destPath must be a path to an existing directory
def destFileFolderExtractor(destPath: str):
    ## path must exist
    if not(os.path.exists(destPath)):
        raise PathNotFoundError(f"Path not found: {destPath}")
    
    ## existing path can be normalized
    normDestPath = os.path.normpath(destPath)

    ## path must be a folder
    if not(os.path.isdir(normDestPath)):
        raise PathError(f"Path must represent Directory {normDestPath}")
    
    ## retrieving directory list
    dirList = os.listdir(normDestPath)

    ## directory must not be empty
    newDirList = [0,0]
    ## segregating files & folders in listDir
    for pathName in dirList:
        ## pathName is a folder -> count & insert into first section of newDirList        
        if os.path.isdir(pathName):
            newDirList[0]++
            newDirList.insert(newDirList[0] + 1, pathName)
        ## pathName is a file -> count & insert into second section of newDirList
        elif os.path.isfile(pathName):
            newDirList[newDirList[0] + 1]++
            newDirList.insert(newDirList[newDirList[0] + 1] + 1], pathName)
        ## pathName is neither folder nor file -> PathError
        else:
            raise PathError(f"Path must represent Directory or File: {pathName}")
    
    return newDirList


