import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pyutil


def axis_border(ax,color='black',width=1.5):
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(width)

def create_axis(w=4,h=4):
    #fig = plt.figure(figsize=(w,h),facecolor='lightgray',edgecolor='black')
    fig = plt.figure(figsize=(w,h),edgecolor='black')
    ax = plt.axes()
    return fig,ax

def scatterplot_matrix(df,figsize=None,pltsize=(5,4),show=False):
    col,dim = list(df.columns),len(df.columns)
    if figsize==None:
        figsize = tuple(dim*x for x in pltsize)
    #fig,ax= plt.subplots(dim,dim,figsize=figsize,sharey='row',sharex='col',squeeze=False)
    fig,axs = plt.subplots(dim,dim,figsize=figsize,squeeze=True,frameon=True)
    for i,axrow in zip(col,axs):
        for j,ax in zip(col,axrow):
            if i==j:
                ax.hist(df[i],bins=30,alpha=0.7,edgecolor='black',histtype='stepfilled')
                #ax.text(ax.get_xlim()[0],ax.get_ylim()[1],i)
            else:
                ax.scatter(df[j],df[i],s=10)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            axis_border(ax,'black',1.5)
    for i,x in enumerate(col):
        axs[0][i].set_title(x,fontsize=20,family='monospace')
        axs[i][0].set_ylabel(x,fontsize=20,family='monospace')
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
    
    
    