
import pandas

################################ [Pandas] ################################################################

def pd_dataframe(inx=None,col=None):
    def dec(fn):
        def wrapper(*args,**kwargs):
            i,d = [[*x] for x in zip(*fn(*args,**kwargs))]
            return pandas.DataFrame(d,pandas.Index(i,name=inx),columns=col)
        return wrapper
    return dec

def pd_series(inx=None,name=None):
    def dec(fn):
        def wrapper(*args,**kwargs):
            i,d = [[*x] for x in zip(*fn(*args,**kwargs))]
            return pandas.Series(d,index=pandas.Index(i,name=inx),name=name)
        return wrapper
    return dec


def pd_multi_index(names=None):
    def dec(fn):
        def wrapper(*args,**kwargs):
            return pandas.MultiIndex.from_tuples([*fn(*args,**kwargs)],names=names)
        return wrapper
    return dec

def pd_index(name=None):
    def dec(fn):
        def wrapper(*args,**kwargs):
            return pandas.Index([*fn(*args,**kwargs)],name=name)
        return wrapper
    return dec


def pd_concat(axis=0):
    def dec(fn):
        def wrapper(*args,**kwargs):
            return pandas.concat([*fn(*args,**kwargs)],axis=axis)
        return wrapper
    return dec


################################ [Generator] ################################################################

def list_gen(fn):
    def wrapper(*args,**kwargs):
        return list(fn(*args,**kwargs))
    return wrapper

def tuple_gen(fn):
    def wrapper(*args,**kwargs):
        return tuple(fn(*args,**kwargs))
    return wrapper

def dict_gen(fn):
    def wrapper(*args,**kwargs):
        return dict(fn(*args,**kwargs))
    return wrapper

def str_gen(fn):
    def wrapper(*args,**kwargs):
        return ''.join(fn(*args,**kwargs))
    return wrapper

def file_gen(fn):
    def wrapper(path,*args,**kwargs):
        with open(path,'w') as f:
            for l in fn(*args,**kwargs):
                f.write(l)
    return wrapper

def transpose_gen(fn):
    def wrapper(*args,**kwargs):
        for x in zip(*fn(*args,**kwargs)):
            yield list(x)
    return wrapper

def transpose_tuple_gen(fn):
    def wrapper(*args,**kwargs):
        for x in zip(*fn(*args,**kwargs)):
            yield tuple(x)
    return wrapper



################################ [Sort] ################################################################

# fn is comparator function
def mergesort(fn):
    def merge(a,b):
        i,j,x,y = 0,0,len(a),len(b)
        while i<x and j<y:
            z = fn(a[i],b[j])
            if z<0:
                yield a[i]
                i=i+1
            elif z>0:
                yield b[j]
                j=j+1
            else:
                yield a[i]
                yield b[j]
                i,j=i+1,j+1
        while i<x:
            yield a[i]
            i=i+1
        while j<y:
            yield b[j]
            j=j+1

    def wrapper(l):
        if len(l)<=1:return l
        m = len(l)//2
        return [*merge(wrapper(l[:m]),wrapper(l[m:]))]
    return wrapper

# fn is comparator function
def mergesort_set(fn):
    def merge(a,b):
        i,j,x,y = 0,0,len(a),len(b)
        while i<x and j<y:
            z = fn(a[i],b[j])
            if z<0:
                yield a[i]
                i=i+1
            elif z>0:
                yield b[j]
                j=j+1
            else:
                yield a[i]
                i,j=i+1,j+1
        while i<x:
            yield a[i]
            i=i+1
        while j<y:
            yield b[j]
            j=j+1

    def wrapper(l):
        if len(l)<=1:return l
        m = len(l)//2
        return [*merge(wrapper(l[:m]),wrapper(l[m:]))]
    return wrapper


# fn is generator function
def sorted(fn):
    def merge(a,b):
        i,j,x,y = 0,0,len(a),len(b)
        while i<x and j<y:
            if a[i]<b[j]:
                yield a[i]
                i=i+1
            elif a[i]>b[j]:
                yield b[j]
                j=j+1
            else:
                yield a[i]
                yield b[j]
                i,j=i+1,j+1
        while i<x:
            yield a[i]
            i=i+1
        while j<y:
            yield b[j]
            j=j+1

    def sort(l):
        if len(l)<=1:return l
        m = len(l)//2
        return [*merge(sort(l[:m]),sort(l[m:]))]

    def wrapper(*args,**kwargs):
        return sort([*fn(*args,**kwargs)])
    return wrapper


# fn is generator function
def sorted_set(fn):
    def merge(a,b):
        i,j,x,y = 0,0,len(a),len(b)
        while i<x and j<y:
            if a[i]<b[j]:
                yield a[i]
                i=i+1
            elif a[i]>b[j]:
                yield b[j]
                j=j+1
            else:
                yield a[i]
                i,j=i+1,j+1
        while i<x:
            yield a[i]
            i=i+1
        while j<y:
            yield b[j]
            j=j+1

    def sort(l):
        if len(l)<=1:return l
        m = len(l)//2
        return [*merge(sort(l[:m]),sort(l[m:]))]

    def wrapper(*args,**kwargs):
        return sort([*fn(*args,**kwargs)])
    return wrapper
