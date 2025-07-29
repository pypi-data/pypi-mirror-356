import os
import errno
from . import utils


def abspath(filepath):
    return os.path.abspath(filepath)

def addExtension(filename,extension):
    if '.' not in filename:
        extension = '.' + extension
    #if not filename.lower().endswith(extension):
    #    filename = filename +extension
    return filename

def _createDirectories(filename):
    dirname =os.path.dirname(filename)
    if dirname == '':
        return True #local file
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            return True
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                utils.raiseException('OSError',f"Error creating directory {dirname}  {exc.errno}")
    return False

#def getFilePath(folder,filename):

def writeFileinFolder(folder,filename,data):
    return write(f"{folder}/{filename}",'.txt',data)

def delete(filename):
    os.remove(filename)

def write(filepath,data,mode="w"):
    _createDirectories(filepath)
    with open(filepath, mode, encoding="utf-8", errors='replace') as f:
        f.write(data)

    return os.path.abspath(filepath)

def exists(filepath):
    return os.path.exists(filepath)

def read(filepath):
    with open(filepath, 'r', encoding="utf-8", errors='ignore') as f:
        data = f.read()
    return data

def openFile(filepath,mode="w"):
    f = open(filepath,mode,encoding="utf-8",errors='ignore')
    return f
def write_line(f,line):
    f.write(line+ "\n")
    return f
def closeFile(f):
    f.close()

def emptyDirectory(directory):
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            os.remove(os.path.join(directory, f))


def writeDictionaty(filepath,extension,dictionary,firstLine=False,mode='a'):
  #  filepath = _checkExtension(filepath,extension)

    if os.path.isfile(filepath) == False:  #If theere is no file, always create header
        firstLine = True
    else:
        firstLine = False

    if firstLine == True:
        joined = ",".join(dictionary)+ "\n"
        #print(joined)
        write(filepath,extension,joined,mode=mode)

    values = list(dictionary.values())
    str_values = map(str,values)

    joined = ",".join(str_values) + "\n"
    write(filepath,extension,joined,'a')

