

################################ [Random] ################################################################

import random

def ranchar():
    return chr(random.randint(65,90))

def ranchars(n):
    return [ranchar() for x in range(n)]

def shuffle(l):
    inx = [*range(len(l))]
    random.shuffle(inx)
    if type(l)==tuple:
        return tuple(l[i] for i in inx)
    return [l[i] for i in inx]


################################ [Core] ################################################################

def getkey(d,key,default):
    """gets key from dict (d), if key does not exist, return default"""
    if key in d:
        return d[key]
    else:
        return default

def zipmap(inx,itr):
    for i in inx:
        yield i,itr[i]


# Reversed version of the built in enumerate() function
def enumerate_backwards(a):
    n = len(a)-1
    for i in reversed(a):
        yield (n,i)
        n-=1
# FILESYSTEM UTILITY FUNCTIONS


def is_iterable(a):
    if type(a)==str:
        return False
    try:
        iter(a)
        return True
    except TypeError:
        return False


################################ [IO] ################################################################

import os


def from_csv(filepath):
    with open(filepath,'r') as f:
        return [l[:-1].split(',') for l in f]


def verify_dir(p):
    if len(p) and not os.path.exists(p):
        verify_dir(os.path.dirname(p))
        os.mkdir(p)

def mkdir(name,path=''):
    fd = path+name
    if (os.path.exists(fd) and os.path.isdir(fd)):
        return False
    os.mkdir(fd)
    print('mkdir [{}]'.format(fd))
    return True

def listdir(path=''):
    return os.listdir(os.path.join(os.getcwd(),path))

def createpath(*pieces):
    return '/'.join(pieces)

def filename(path,ext=True):
    path = os.path.basename(path)
    if ext==False and '.' in path:
        path = path[:path.rfind('.')]
    return path

def files(path,filetype='',full=False):
    if full:
        filepaths = [os.path.join(path,f) for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) and f.endswith(filetype))]
    else:
        filepaths = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) and f.endswith(filetype))]
    return quicksort(filepaths)

def dirs(path,full=False):
    if full:
        dirpaths = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    else:
        dirpaths = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return quicksort(dirpaths)


def allfiles(path='',filetype=''):
    filepaths = []
    for r,d,f in os.walk(path):
        filepaths.extend([os.path.join(r,x) for x in f if x.endswith(filetype)])
    return quicksort(filepaths)

def alldirs(path=''):
    dirpaths = []
    for r,d,f in os.walk(path):
        dirpaths.extend([os.path.join(r,x) for x in d])
    return quicksort(dirpaths)


# IO UTILITY FUNCTIONS

def readfile(file,path=''):
    with open(path+file, 'r') as f:
        return f.read()

def writefile(file,data='',path=''):
    with open(path+file, 'w') as f:
        return f.write(data)

def readlines(filepath,end=0):
    txt = readfile(filepath)
    i,l=0,len(txt)
    while (i<l):
        j = txt.find('\n',i)
        yield txt[i:j+end]
        i=j+1

def filelines(path,end=1):
    with open(path,'r') as f:
        for l in f:
            yield l[:len(l)-end]

def linecount(path):
    count=0
    with open(path) as f:
        for l in f:
            count+=1
    return count
