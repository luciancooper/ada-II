import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import pyutil

class PygraphError(Exception):
    pass

def axis_border(ax,color='black',width=1.5):
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(width)

def create_axis(w=4,h=4):
    #fig = plt.figure(figsize=(w,h),facecolor='lightgray',edgecolor='black')
    fig = plt.figure(figsize=(w,h),edgecolor='black')
    ax = plt.axes()
    return fig,ax

def _scatter_grid(labels,figsize,pltsize):
    dim = len(labels)
    if figsize==None:
        figsize = tuple(dim*x for x in pltsize)
    fig,axs = plt.subplots(dim,dim,figsize=figsize,squeeze=True,frameon=True)
    for ax in (i for j in axs for i in j):
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        axis_border(ax,'black',1.5)
    for i,x in enumerate(labels):
        axs[0][i].set_title(str(x),fontsize=20,family='monospace')
        axs[i][0].set_ylabel(str(x),fontsize=20,family='monospace')
    return fig,axs

def _grid_inxs(*dim):
    m,n = dim[0],dim[-1]
    for i in range(m):
        for j in range(n):
            yield i,j

def scatterplot_matrix(data,labels=None,facet_hue=None,figsize=None,pltsize=(5,4),show=False):
    if type(data)==pd.DataFrame:
        if labels==None:
            labels=list(data.columns)
        if facet_hue!=None:
            if facet_hue in labels:
                labels.remove(facet_hue)
            fh = data[facet_hue]
            enc,cat = fh.factorize()
            data = data[labels].values
            groups = tuple(data[enc==i] for i in range(len(cat)))
            fig,axs = _scatter_grid(labels,figsize,pltsize)
            colors = sns.color_palette("muted",n_colors=len(groups)).as_hex()
            for i,j in _grid_inxs(len(labels)):
                if i==j:
                    axs[i][j].hist(data[:,i],bins=30,alpha=0.7,edgecolor='black',histtype='stepfilled')
                    continue
                for g,color in zip(groups,colors):
                    axs[i][j].scatter(g[:,j],g[:,i],s=10,c=color,alpha=0.6)
        else:
            data = data[labels].values
            fig,axs = _scatter_grid(labels,figsize,pltsize)
            for i,j in _grid_inxs(len(labels)):
                if i==j:
                    axs[i][j].hist(data[:,i],bins=30,alpha=0.7,edgecolor='black',histtype='stepfilled')
                    continue
                axs[i][j].scatter(data[:,j],data[:,i],s=10)
    elif type(data)==np.ndarray:
        fh,val = None,None
        if labels==None:
            labels=[*range(data.shape[1])]
            if facet_hue!=None:
                labels.remove(facet_hue)
                fh,val = data[:,facet_hue],data[:,labels]
            else:
                val = data
        elif all(type(x)==int for x in labels):
            if facet_hue!=None:
                if facet_hue in labels:
                    labels.remove(facet_hue)
                fh,val = data[:,facet_hue],data[:,labels]
            else:
                val = data[:,labels]
        else:
            if facet_hue!=None:
                if type(facet_hue)==str:
                    facet_hue = labels.index(facet_hue)
                fh,val = data[:,facet_hue],data[:,[*range(facet_hue)]+[*range(facet_hue+1,len(labels))]]
                # facet_hue_label = labels[facet_hue]
                labels = labels[:facet_hue]+labels[facet_hue+1:]
            else:
                val = data
        fig,axs = _scatter_grid(labels,figsize,pltsize)
        if fh!=None:
            enc,cat = pd.Series(fh).factorize()
            groups = tuple(val[enc==i] for i in range(len(cat)))
            colors = sns.color_palette("muted",n_colors=len(groups)).as_hex()
            for i,j in _grid_inxs(len(labels)):
                if i==j:
                    axs[i][j].hist(val[:,i],bins=30,alpha=0.7,edgecolor='black',histtype='stepfilled')
                    continue
                for g,color in zip(groups,colors):
                    axs[i][j].scatter(g[:,j],g[:,i],s=10,c=color)
        else:
            for i,j in _grid_inxs(len(labels)):
                if i==j:
                    axs[i][j].hist(val[:,i],bins=30,alpha=0.7,edgecolor='black',histtype='stepfilled')
                    continue
                axs[i][j].scatter(val[:,j],val[:,i],s=10)
    else:
        raise PygraphError('Scatterplot Matrix must recieve either pandas.DataFrame or numpy.ndarray as arguments')
    plt.tight_layout()
    if show:plt.show()


def piechart(data,size=(4,4),show=False,**args):
    fix,ax = create_axis(*size)
    if type(data)==pd.Series:
        ax.set_title(data.name,fontdict={'family':'monospace'})
        enc,cat = data.factorize()
        bins = [0]*len(cat)
        for x in enc:
            bins[x]+=1
        data = dict((str(k),v) for k,v in zip(cat,bins))
    elif type(data)!=dict:
        cat = pyutil.sort_set(data)
        bins = [0]*len(cat)
        for x in data:
            bins[pyutil.bin_index(cat,x)]+=1
        data = dict((str(k),v) for k,v in zip(cat,bins))
    val = list(data.values())
    lbl = list(data.keys())
    ax.pie(val,labels=lbl,**args)
    if show: plt.show()


def merge_kwargs(args,**kwargs):
    for k,v in kwargs.items():
        if k in args: continue
        args[k]=v
    return args


def histogram(data,size=(5,4),show=False,**args):
    args = merge_kwargs(args,histtype='stepfilled',alpha=0.3)
    if type(data)==pd.DataFrame:
        fig,axs = _axis_grid(len(data.columns),*size)
        for j,ax in zip(data.columns,axs):
            ax.set_title(j,fontdict={'family':'monospace'})
            ax.hist(data[j].values,**args)
    elif type(data)==pd.Series:
        fig,ax = create_axis(*size)
        ax.set_title(data.name,fontdict={'family':'monospace'})
        ax.hist(data.values,**args)
    plt.tight_layout()
    if show: plt.show()

def _axis_grid(count,pw,ph):
    n = count if count<4 else 3 if count>5 else 2
    m = count//n + int(count%n>0)
    grid = plt.GridSpec(m,n*2)
    sub = [a for b in [[grid[i,j:j+2] for j in range(0,n*2,2)] for i in range(count//n)] for a in b]+[grid[m-1,x:x+2] for x in range(n-count%n,n+count%n,2)]
    fig = plt.figure(figsize=(n*pw,m*ph),edgecolor='black')
    return fig,[fig.add_subplot(x,yticklabels=[]) for x in sub]
