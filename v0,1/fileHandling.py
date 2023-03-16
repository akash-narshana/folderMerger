import os
import shutil

####------------CONSTANTS---------------####

MOVED_AS_DUPLICATE = 100
MOVED_AS_UNIQUE = 101
FOUND_MATCHING = 102
MATCH_NOT_FOUND = 103

PATH_NOT_FOUND = "Path does not exist: "

####------------/CONSTANTS--------------####


####------------EXCEPTIONS--------------####

class PathError(Exception):
    """
    ATTRIBUTES: message
    """

    def __init__(self, path: str, message: str = PATH_NOT_FOUND):
        self.message = message
        if message == PATH_NOT_FOUND: self.message += path ## for no passed message
        super().__init__(self.message)


####------------/EXCEPTIONS-------------####


# ## current working dir
# cwd = os.getcwd()

# ## file destination
# DEST_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/sample destination/"
# LOG_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/log.txt"
# ## change dir to source
# # os.chdir(sourcePath)
# SOURCE_PATH = "C:/Users/emper/OneDrive/Desktop/Winter 2023/Rashmi file sorter/sample source/"


## (dirFileFolderExtractor destPath)
##      Returns a list with the folders and files in destPath
## Str -> List(Int, Str) => [folderCount, folderPaths..., fileCount, filePaths...]
## O(n); n = size(subdirectories of destPath)
## eReqs:    destPath must be a String
## iReqs:    destPath must be a path to an existing directory => (Exception: PathError)
def dirFileFolderExtractor(destPath: str):
    if not(os.path.exists(destPath)):
        raise PathError(destPath)
    normDestPath = os.path.normpath(destPath) ## existing path can be normalized
    if not(os.path.isdir(normDestPath)):
        raise PathError(normDestPath, f"Path must represent Directory: {normDestPath}")
    
    dirList = os.listdir(normDestPath) ## retrieving directory list
    

    newDirList = [0,0]
    ## segregating files & folders in listDir
    for pathName in dirList:
        try:
            normPathName = os.path.normpath(pathName)
            ## pathName is a folder -> count & insert into first section of newDirList        
            if os.path.isdir(normPathName):
                newDirList[0] += 1
                newDirList.insert(newDirList[0] + 1, pathName)
            ## pathName is a file -> count & insert into second section of newDirList
            elif os.path.isfile(normPathName):
                newDirList[newDirList[0] + 1] += 1
                newDirList.insert(newDirList[newDirList[0] + 1] + 1], pathName)
            ## pathName is neither folder nor file -> PathError
            else:
                raise PathError(pathName, f"Path must represent Directory or File: {pathName}")
        except PathError:
            continue
    
    return newDirList


## (parentDirExtractor childPath)
##      Returns the name of the parent directory of childPath
## Str -> Str (Exception: PathError)
## eReqs:   childPath must be a String
## iReqs:   childPath must be an existing path => (Exception: PathError)
def parentDirExtractor(childPath: str):
    if not os.path.exists(childPath):
        raise PathError(childPath)
    
    childPathSplit = os.path.split(os.path.normpath(childPath))
    if not childPathSplit[1]: ## folder path ending with '/'
        return os.path.split(os.path.split(childPathSplit[0])[0])[1]
    elif not childPathSplit[0]:
        raise PathError(childPath, f"Path does not contain Parent Directory: {childPath}")
    return childPathSplit[0]


## (dirNameExtractor dirPath)
##      Returns the name of the folder or file that dirPath leads to
## Str -> Str (Exception: PathError)
## eReqs:   dirPath must be a String
## iReqs:   dirPath must be an existing path => (Exception: PathError)
def dirNameExtractor(dirPath: str):
    if not os.path.exists(dirPath):
        raise PathError(dirPath)

    dirPathSplit = os.path.split(os.path.normpath(dirPath))
    if not dirPathSplit[1]:
        return os.path.split(dirPathSplit[0])[1]
    return dirPathSplit[1]


## (fileDestFinder sourceFilePath, destPath, destDirList, potentialDupesPath)
##      Finds the appropriate new path for the file at sourceFilePath
##          Returns a constant and the appropriate new path
## Str, Str, List(Int, Str), Str -> List(Int, Str)
## eReqs:   sourceFilePath, destPath, potentialDupesPath must be Strings
##          desDirList must be a List
## iReqs:   sourceFilePath, destPath, potentialDupesPath must be existing paths
##              => (Exception: PathError)
## oReqs:   destDirList must be a List in the format: [folderCount, folderPaths..., fileCount, filePaths...]
def fileDestFinder(sourceFilePath: str, destPath: str, destDirList: list, potentialDupesPath: str)
    if not os.path.exists(sourceFilePath): ## iReqs
        raise PathError(sourceFilePath)
    if not os.path.isfile(os.path.normpath(sourceFilePath)):
        raise PathError(sourceFilePath, f"Path must represent a File: {sourceFilePath}")
    if not os.path.exists(destPath):
        raise PathError(destPath)
    if not os.path.exists(potentialDupesPath):
        raise PathError(potentialDupesPath) ## /iReqs

    sourceFileName = os.path.split(sourceFilePath)[1]
    for destDirFilePath in destDirList[destDirList[0] + 1: destDirList[destDirList[0] + 1] + 1]:
        try: ## iReqs
            if not os.path.exists(destDirFilePath):
                raise PathError(destDirFilePath)
        except PathError:
            continue ##/iReqs
            
        destDirFileName = os.path.split(destDirFilePath)[1]
        ## file Handling
        if sourceFileName == destDirFileName: ## matching file name
            return [MOVE_AS_DUPLICATE, potentialDupesPath]
    ## unique file name
    return [MOVE_AS_UNIQUE, destPath]


## (fileNavigator sourceFilePath, sourceParentDirName, destDirList, potentialDupesPath)
##      Recursively finds whether a folder with the name sourceParentDirName exists in destDirList
##          Returns a constant and (the appropriate new path OR **)
## Str, Str, List(Int, Str), Str -> List(Int, List(Int, Str))
## eReqs:   sourceFilePath, sourceParentDirName, potentialDupesPath must be Strings
## iReqs:   sourceFilePath, potentialDupesPath must be existing paths
##              => (Exception: PathError)
## oReqs:   destDirList must be a List in the format: [folderCount, folderPaths..., fileCount, filePaths...]
def fileNavigator(sourceFilePath: str, sourceParentDirName: str, destDirList: list, potentialDupesPath: str):
    if not os.path.exists(sourceFilePath): ## iReqs
        raise PathError(sourceFilePath)
    if not os.path.exists(potentialDupesPath):
        raise PathError(potentialDupesPath) ## /iReqs
    
    for destDirFolderPath in destDirList[1:destDirList[0] + 1]:
        try: ## iReqs
            if not os.path.exists(destDirFolderPath):
                raise PathError(destDirFolderPath)
        except:
            continue ## /iReqs
        
        destDirFolderName = dirNameExtractor(destDirFolderPath)
        if destDirFolderName == sourceParentDirName: ## matching folder found
            fileDest = fileDestFinder(sourceFilePath, destDirFolderPath, dirFileFolderExtractor(destDirFolderPath), potentialDupesPath)
            ## exCon: matching folder found
            return [FOUND_MATCHING, fileDest]
    
    for destDirFolderPath in destDirList[1:destDirList[0] + 1]:
        newDirList = dirFileFolderExtractor(destDirFolderPath)
        navigatedFile = fileNavigator(sourceFilePath, sourceParentDirName, newDirList, potentialDupesPath)
        if navigatedFile[0] != MATCH_NOT_FOUND: ## matching folder found
            ## exCon: matching folder found deeper
            return [FOUND_MATCHING, navigatedFile[1]]
    
    ## exCon: no matching folder found
    return [MATCH_NOT_FOUND, destDirList]


## (fileHandler sourceFilePath, destPath, potentialDupesPath)
##      Finds the appropriate destination for the file at sourcePath
##          (a folder in destPath OR potentialDupesPath)
##      Moves the file at sourceFilePath to the appropriate destination
##          Returns the new path for the file at sourceFilePath
## Str, Str, Str -> Str
## eReqs:   all arguments must be Strings
## iReqs:   all arguments must be existing paths => (Exception: PathError)
def fileHandler(sourceFilePath: str, destPath: str, potentialDupesPath: str):
    if not os.path.exists(sourceFilePath): ## iReqs
        raise PathError(sourceFilePath)
    if not os.path.exists(destPath):
        raise PathError(destPath)
    if not os.path.exists(potentialDupesPath):
        raise PathError(potentialDupesPath) ## /iReqs
    
    destDirList = dirFileFolderExtractor(normDestPath)
    sourceParentDirName = parentDirExtractor(sourceFilePath)
    navigatedFile = fileNavigator(sourceFilePath, sourceParentDirName, destDirList, potentialDupesPath)
    if navigatedFile[0] == FOUND_MATCHING:
        fileDestPath = navigatedFile[1][1]
        return shutil.move(sourceFilePath, fileDestPath)
    
    fileDestPath = fileDestFinder(sourceFilePath, destPath, destDirList, potentialDupesPath)[1]
    return shutil.move(sourceFilePath, fileDestPath)


def folderMerger(sourcePath: str, destPath: str):
    if not os.path.exists(sourcePath): ## iReqs
        raise PathError(sourcePath)
    if not os.path.exists(destPath):
        raise PathError(destPath)
    if not os.path.isdir(os.path.normpath(sourcePath)):
        raise PathError(sourcePath, f"Path must represent a Directory: {sourcePath}") ## /iReqs
    if not os.path.isdor(os.path.normpath(destPath)):
        raise PathError(destPath, f"Path must represent a Directory: {destPath}")
    
    ## making folder for duplicates
    potentialDupesDir = dirNameExtractor(sourcePath) + "_duplicates"
    potentialDupesPath = os.path.join(destPath, potentialDupesDir)
    try:
        os.mkdir(potentialDupesPath)
    except FileExistsError: ## potentialDupesPath exists -> pass
        pass
    except FileNotFoundError: ## missing parent directories
        try:
            os.makedirs(os.path.join(destPath, potentialDupesDir))
        except FileExistsError: ## potentialDupePath exists -> pass
            pass
    
    