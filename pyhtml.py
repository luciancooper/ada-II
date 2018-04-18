#!/usr/bin/env python

import IPython.core.display as _ipy
import random,os,re
from pystr import knit as strknit

################################ [Builtins] ################################################################

def _pyHTML_dict(d,maxrow=10,showall=False,**kwargs):
    m = len(d)
    if showall==True: maxrow=m
    if (m>maxrow):
        d = list(d.items())
        b0 = ''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(k,v) for k,v in d[:maxrow//2])
        b1 = ''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(k,v) for k,v in d[-maxrow//2:])
        tbody = '<tbody>%s</tbody><tbody>%s</tbody>'%(b0,b1)
    else:
        tbody = '<tbody>%s</tbody>'%''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(k,v) for k,v in d.items())
    return "<table class='py dict'>%s</table>"%tbody

def _pyHTML_list(d,maxrow=10,showall=False,**kwargs):
    m = len(d)
    if showall==True: maxrow=m
    if (m>maxrow):
        b0 = ''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(i,v) for i,v in zip(range(maxrow//2),d[:maxrow//2]))
        b1 = ''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(i,v) for i,v in zip(range(m-maxrow//2,m),d[-maxrow//2:]))
        tbody = '<tbody>%s</tbody><tbody>%s</tbody>'%(b0,b1)
    else:
        tbody = '<tbody>%s</tbody>'%''.join('<tr><th>{}</th><td>{}</td></tr>\n'.format(i,v) for i,v in enumerate(d))
    return "<table class='py list'>%s</table>"%tbody


################################ [Numpy] ################################################################

def _npHTML_array_1d(a,maxrow=10,showall=False,**kwargs):
    n = a.shape[0]
    if showall==True:maxrow=n
    if n>maxrow:
        d0 = ''.join('<td>{}</td>'.format(x) for x in a[:maxrow//2])
        d1 = ''.join('<td>{}</td>'.format(x) for x in a[-maxrow//2:])
        tbody = "<tbody><tr>%s<td class='row-sep'></td>%s</tr></tbody>"%(d0,d1)
    else:
        tbody = '<tbody><tr>%s</tr></tbody>'%''.join('<td>{}</td>'.format(x) for x in a)
    return "<table class='numpy array-1d'>%s</table>"%tbody

def _npHTML_array_2d(a,maxrow=10,showall=False,**kwargs):
    m,n = a.shape
    if showall==True:maxrow=m
    if m>maxrow:
        i0 = '\n'.join('<tr><th>%i</th>'%x for x in range(maxrow//2))
        i1 = '\n'.join('<tr><th>%i</th>'%x for x in range(m-maxrow//2,m))
        b0 = '\n'.join('%s</tr>'%''.join('<td>{}</td>'.format(i) for i in j) for j in a[:maxrow//2])
        b1 = '\n'.join('%s</tr>'%''.join('<td>{}</td>'.format(i) for i in j) for j in a[-maxrow//2:])
        tbody = '<tbody>%s</tbody><tbody>%s</tbody>'%(strknit(i0,b0),strknit(i1,b1))
    else:
        inx = '\n'.join('<tr><th>%i</th>'%x for x in range(m))
        data = '\n'.join('%s</tr>'%''.join('<td>{}</td>'.format(i) for i in j) for j in a)
        tbody = '<tbody>%s</tbody>'%strknit(inx,data)
    return "<table class='numpy array-2d'>%s</table>"%tbody

################################ [Pandas] ################################################################

def _pdHTML_Index(inx,maxrow=10,showall=False,**kwargs):
    m = len(inx)
    if showall==True:maxrow=m
    if (m>maxrow):
        top = ''.join('<tr><td>{}</td></tr>\n'.format(x) for x in inx[:maxrow//2])
        bot = ''.join('<tr><td>{}</td></tr>\n'.format(x) for x in inx[-maxrow//2:])
        tbody = '<tbody>%s</tbody><tbody>%s</tbody>'%(top,bot)
    else:
        tbody = '<tbody>%s</tbody>'%''.join('<tr><td>{}</td></tr>\n'.format(x) for x in inx)
    tfoot = '<tfoot><tr><td>%s</td></tr></tfoot>'%inx.dtype_str
    thead = '<thead><tr><td>%s</td></tr></thead>'%inx.name if inx.name!=None else ''
    return "<table class='pandas index'>%s%s%s</table>"%(thead,tbody,tfoot)

def _pdHTML_MultiIndex(inx,maxrow=10,showall=False,**kwargs):
    m,n = len(inx),inx.nlevels
    if showall==True:maxrow=m
    if (m>maxrow):
        top = ''.join('<tr>%s</tr>\n'%''.join('<td>{}</td>'.format(y) for y in x) for x in inx[:maxrow//2])
        bot = ''.join('<tr>%s</tr>\n'%''.join('<td>{}</td>'.format(y) for y in x) for x in inx[-maxrow//2:])
        tbody = '<tbody>%s</tbody><tbody>%s</tbody>'%(top,bot)
    else:
        tbody = '<tbody>%s</tbody>'%''.join('<tr>%s</tr>\n'%''.join('<td>{}</td>'.format(y) for y in x) for x in inx)
    tfoot = '<tfoot><tr><td colspan="%i">%s</td></tr></tfoot>'%(n,inx.dtype_str)
    if any(x!=None for x in inx.names):
        thead = '<thead><tr>%s</tr></thead>'%''.join('<td>{}</td>'.format(x) if x!=None else '<td></td>' for x in inx.names)
    else:
        thead = ''
    return "<table class='pandas index'>%s%s%s</table>"%(thead,tbody,tfoot)

def _pdindex_HTML(inx,maxrow):
    m,n = inx.shape[0],inx.nlevels
    th = '<th>{}</th>'*n+'\n'
    html = ''.join([('<th>{}</th>'.format(x) if x != None else '<th></th>') for x in inx.names])+'\n'
    if (m>maxrow):
        if (n>1):
            html += ''.join([th.format(*x) for x in inx[:maxrow//2]])+''.join([th.format(*x) for x in inx[-maxrow//2:]])
        else:
            html += ''.join([th.format(x) for x in inx[:maxrow//2]])+''.join([th.format(x) for x in inx[-maxrow//2:]])
    else:
        html += ''.join([th.format(*x) for x in inx] if n>1 else [th.format(x) for x in inx])
    return html+'<th colspan="{}">{}</th>'.format(n,inx.dtype_str)+'\n'

def _pdHTML_Series(series,maxrow=10,showall=False,**kwargs):
    m = series.shape[0]
    if showall==True:maxrow=m
    if (m>maxrow):
        html = "<thead><tr>\n</thead><tbody>"+('<tr>\n'*(maxrow//2))+'</tbody><tbody>'+('<tr>\n'*(maxrow//2))+'</tbody><tfoot><tr>\n'
        html = strknit(html,_pdindex_HTML(series.index,maxrow))
        dtype=re.sub(r'\d','',str(series.dtype))
        td = '<td>{:.3f}</td></tr>\n' if 'float' in dtype else '<td>{}</td></tr>\n'
        topTD = ''.join([td.format(x) for x in series[:maxrow//2]])
        botTD = ''.join([td.format(x) for x in series[-maxrow//2:]])
        html = strknit(html,'<th>{}</th></tr>\n{}{}<td>{}</td></tr></tfoot>\n'.format(series.name if series.name!=None else '',topTD,botTD,dtype))
    else:
        html = strknit("<thead><tr>\n</thead><tbody>"+('<tr>\n'*m)+'</tbody><tfoot><tr>\n',_pdindex_HTML(series.index,maxrow))
        dtype=re.sub(r'\d','',str(series.dtype))
        td = '<td>{:.3f}</td></tr>\n' if 'float' in dtype else '<td>{}</td></tr>\n'
        TD = ''.join([td.format(x) for x in series])
        html = strknit(html,'<th>{}</th></tr>\n{}<td>{}</td></tr></tfoot>\n'.format(series.name if series.name!=None else '',TD,dtype))
    return "<table class='pandas series'>"+html+"</table>"

def _pdHTML_DataFrame(df,maxrow=10,showall=False,**kwargs):
    m = df.shape[0]
    if showall==True: maxrow=m
    if (m>maxrow):
        html = "<thead><tr>\n</thead><tbody>"+('<tr>\n'*(maxrow//2))+'</tbody><tbody>'+('<tr>\n'*(maxrow//2))+'</tbody><tfoot><tr>\n'
        html = strknit(html,_pdindex_HTML(df.index,maxrow))
        for n in df.columns:
            dtype=re.sub(r'\d','',str(df[n].dtype))
            td = '<td>{:.3f}</td>\n' if 'float' in dtype else '<td>{}</td>\n'
            html = strknit(html,'<td>{}</td>\n{}{}<td>{}</td>\n'.format(df[n].name,''.join([td.format(x) for x in df[n][:maxrow//2]]),''.join([td.format(x) for x in df[n][-maxrow//2:]]),dtype))
        html = strknit(html,'</tr>\n'*(maxrow+2))
    else:
        html = "<thead><tr>\n</thead><tbody>"+('<tr>\n'*m)+'</tbody><tfoot><tr>\n'
        html = strknit(html,_pdindex_HTML(df.index,maxrow))
        for n in df.columns:
            dtype=re.sub(r'\d','',str(df[n].dtype))
            td = '<td>{:.3f}</td>\n' if 'float' in dtype else '<td>{}</td>\n'
            html = strknit(html,'<td>{}</td>\n{}<td>{}</td>\n'.format(df[n].name,''.join([td.format(x) for x in df[n]]),dtype))
        html = strknit(html,'</tr>\n'*(m+2))
    return "<table class='pandas dataframe'>"+html+'</tfoot></table>'

################################ [HTML] ################################################################

class DisplayHTMLError(Exception):
    def __init__(self,item):
        super().__init__('Cannot Produce HTML for [%s.%s]'%(item.__class__.__module__,item.__class__.__name__))

def _randomID(length=10):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return 'LC-'+''.join(random.choice(chars) for x in range(length))

def _buildCSS(cellid):
    return '<style>%s</style>'%_mincss('pyhtml.css').replace('#ID','#'+cellid)

def _mincss(path):
    with open(path,'r') as f:
        css = f.read()
    css = css.replace('\n','')
    css = css.replace('\t','')
    return css

def _HTML(item,**kwargs):
    mod = item.__class__.__module__
    if (mod.startswith('builtins')):
        if type(item)==dict:
            name = 'dict[{}]'.format(len(item))
            html = _pyHTML_dict(item,**kwargs)
        elif type(item)==list:
            name = 'list[{}]'.format(len(item))
            html = _pyHTML_list(item,**kwargs)
        else:
            raise DisplayHTMLError(item)
    elif (mod.startswith('numpy')):
        if len(item.shape)==1:
            name = 'array[{}]'.format(*item.shape)
            html = _npHTML_array_1d(item,**kwargs)
        else:
            name = 'array[{} x {}]'.format(*item.shape)
            html = _npHTML_array_2d(item,**kwargs)
    elif (mod.startswith('pandas')):
        if item.__class__.__name__=='DataFrame':
            name = 'DataFrame[{} x {}]'.format(*item.shape)
            html = _pdHTML_DataFrame(item,**kwargs)
        elif item.__class__.__name__=='Series':
            name = 'Series[%i]'%len(item)
            html = _pdHTML_Series(item,**kwargs)
        elif item.__class__.__name__ in ['Index','Int64Index']:
            name = '%s[%i]'%(item.__class__.__name__,len(item))
            html = _pdHTML_Index(item,**kwargs)
        elif item.__class__.__name__=='MultiIndex':
            name = '%s[%i,%i]'%(item.__class__.__name__,len(item),item.nlevels)
            html = _pdHTML_MultiIndex(item,**kwargs)
        else:
            raise DisplayHTMLError(item)
    elif hasattr(item,'to_html'):
        name,html = item.to_html(**kwargs)
    else:
        raise DisplayHTMLError(item)
    return html,name

def display(item,title='',**kwargs):
    cellid = _randomID()
    style = _buildCSS(cellid)
    if type(item)==dict:
        ctitle = '<h3>'+title+'</h3>' if len(title) else ''
        html = ''
        for k,i in item.items():
            h4 = '<h4>{}</h4>'.format(k)
            ihtml,name = _HTML(i,**kwargs)
            html += '<div><h4>{}</h4><h5>{}</h5>{}</div>'.format(k,name,ihtml)
        #style = ''.join([CSS_CODE[x].replace('#ID','#'+cellid) for x in css])
        _ipy.display(_ipy.HTML("<section id='{}'>{}{}<section>{}</section></section>".format(cellid,style,ctitle,html)))
    else:
        h4 = '<h4>{}</h4>'.format(title) if len(title) else ''
        html,name = _HTML(item,**kwargs)
        _ipy.display(_ipy.HTML("<section id='{}'>{}<div>{}<h5>{}</h5>{}</div></section>".format(cellid,style,h4,name,html)))
