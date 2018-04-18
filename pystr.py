def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# (> : right) (< : left) (^ : center)
_ALIGN = { 'left':'<','right':'>','center':'^' }

################################ [INDENT] ################################################################

def indent(s,ind=5,end=''):
    if (type(ind)==int):
        ind = ind*' '
    space = len(ind)*' '
    if type(s)==str:
        s = (s[:-1] if s.endswith('\n') else s).split('\n')
    if (len(s)==1):
        return ind+s[0]
    lines = ind+s[0]+end+'\n'
    for i in s[1:-1]:
        lines+=space+i+end+'\n'
    return lines+space+s[-1]

################################ [JOIN] ################################################################

def join(a,b,sep=3):
    if (type(sep)==int):
        sep = sep*' '
    ln=''
    i,j,A,B = a.find('\n'),b.find('\n'),len(a),len(b)
    m,na,nb=0,0,0
    while i>0 and j>0:
        ln+=a[:i]+sep+b[:j+1]
        m,na,nb=m+1,na+i,nb+j
        a,b=a[i+1:],b[j+1:]
        i,j=a.find('\n'),b.find('\n')
    if j>0:
        ind = ' '*(na//m)
        ln+=a+sep+b[:j+1]
        b=b[j+1:]
        j=b.find('\n')
        while j>0:
            ln+=ind+sep+b[:j+1]
            b=b[j+1:]
            j=b.find('\n')
        ln+=ind+sep+b
    elif i>0:
        ind = ' '*(nb//m)
        ln+=a[:i]+sep+b+'\n'
        a = a[i+1:]
        i=a.find('\n')
        while i>0:
            ln+=a[:i]+sep+ind+'\n'
            a = a[i+1:]
            i=a.find('\n')
        ln+=a+sep+ind
    else:
        ln+=a+sep+b
    return ln

################################ [JOIN] ################################################################

def col(col,head='',cf='{}',hf='{}',minw=5):
    col = [str(x) for x in col]
    m = max(*(len(x) for x in col),minw)
    if (head!=None):
        mx = len(hf)-len(cf)
        m = max(len(head)+mx,m)
        #(> : right) (< : left) (^ : center)
        hf,cf = hf.format('{:^%i}'%(m-mx)),cf.format('{:>%i}'%m)
        return hf.format(head)+'\n'+'\n'.join(cf.format(x) for x in col)
    cf = cf.format('{:>%i}'%m)
    return '\n'.join(cf.format(x) for x in col)


################################ [ALIGN] ################################################################

def align(s,span,how='right'):
    if how not in ['<','>','^']: how = _ALIGN[how]
    af = '{:%s%i}'%(align,span)
    return af.format(s)

################################ [STACK] ################################################################

def stack(*s,align='right'):
    a = [i for l in [(x[:-1] if x.endswith('\n') else x).split('\n') for x in s] for i in l]
    #[item for sublist in l for item in sublist]
    if align.startswith('distribute'):
        symbol = align[-2]
        span = max(len(x.replace(symbol,'')) for x in a)
        a = [_align_distr(x,span,symbol) for x in a]
    else:
        if align not in ['<','>','^']: align = _ALIGN[align]
        af = '{:%s%i}'%(align,max(len(x) for x in a))
        a = [*map(af.format,a)]
    return '\n'.join(a)


####################################################################################################
#                                            KNIT                                                  #
####################################################################################################

def knit(*s,sep='',**kwargs):
    a = [(x[:-1] if x.endswith('\n') else x).split('\n') for x in s]
    #print('KNIT ')
    #for x in zip(*a):
    #    print('|'.join([*x]))
    maxlen = max([len(x) for x in a])
    a = [x+['']*(maxlen-len(x)) for x in a]
    if 'align' in kwargs:
        a = _align_knit(kwargs['align'],a)
    return '\n'.join([sep.join(x) for x in zip(*a)])

################################ [ALIGN DISTRIBUTE] ################################################################

def _next_distr_point(s,symbol):
    i = s.find(symbol,i)
    j = s.find(symbol,i+1)
    return s[i+1,j],j+1

def _parsenext_dspt(s,symbol):
    i = s.find(symbol)
    j = s.find(symbol,i+1)
    return s[i+1:j],s[j+1:]

def _get_distr_points(s,symbol,count):
    space = [None]*count
    for x in range(0,count):
        i = s.find(symbol)
        j = s.find(symbol,i+1)
        space[x],s=s[i+1:j],s[j+1:]
    return space

def _fill_distr_points(s,symbol,spaces):
    filled,i,j = '',0,0
    for space in spaces:
        j=s.find(symbol,i)
        filled+=s[i:j]+symbol+space+symbol
        i=s.find(symbol,j+1)+1
    return filled+s[i:]

def _levelout_spaces(spaces,maxlen,count):
    for i,x in enumerate(spaces):
        if len(x) < maxlen:
            spaces[i]=x+' '
            count-=1
            if count==0:
                return

def _distrib_space(spaces,count):
    for i in range(0,count):
        spaces[i]+=' '
    return spaces

def _align_distr(s,mspan,symbol):
    span = mspan-len(s.replace(symbol,''))
    if (span==0):
        return s
    count = s.count(symbol)//2
    if count==0:
        return s+' '*span
    spaces = _get_distr_points(s,symbol,count)
    ms = len(max(spaces, key=len))
    uneven = sum([ms-len(x) for x in spaces])
    if span >= uneven:
        _levelout_spaces(spaces,ms,uneven)
        span-=uneven
        allsp = span//count
        if allsp:
            spaces = [allsp*' '+x for x in spaces]
            span-=allsp*count
        if span:
            spaces =_distrib_space(spaces,span)

    else:
        _levelout_spaces(spaces,ms,span)
    return _fill_distr_points(s,symbol,spaces)

################################ [ALIGN] ################################################################


def _align_knit(atype,s):
    if (atype.startswith('distribute')):
        symbol = atype[-2]
        maxspan = [max([len(y.replace(symbol,'')) for y in x]) for x in s]
        s = [[_align_distr(j,maxspan[i],symbol) for j in x] for i,x in enumerate(s)]
    else:
        if atype not in ['<','>','^']: atype = _ALIGN[atype]
        af = ['{:%s%i}'%(atype,max(len(y) for y in x)) for x in s]
        s = [[*map(f.format,x)] for f,x in zip(af,s)]
    return s
