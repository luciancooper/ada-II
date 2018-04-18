import matplotlib.pyplot as plt

def axis_border(ax,color='black',width=1.5):
    for spine in ax.spines.values():
        spine.set_edgecolor(color)
        spine.set_linewidth(width)

def create_axis(w=4,h=4):
    fig = plt.figure(figsize=(w,h))
    ax = plt.axes()
    return fig,ax

def scatterplot_matrix(df,figsize=None,pltsize=(5,4)):
    col,dim = list(df.columns),len(df.columns)
    if figsize==None:
        figsize = tuple(dim*x for x in pltsize)
    #fig,ax= plt.subplots(dim,dim,figsize=figsize,sharey='row',sharex='col',squeeze=False)
    fig,axs = plt.subplots(dim,dim,figsize=figsize,squeeze=True,frameon=True)
    for i,axrow in zip(col,axs):
        for j,ax in zip(col,axrow):
            if i==j:
                ax.hist(df[i],bins=30,alpha=0.7,edgecolor='black',histtype='bar')
                ax.text(ax.get_xlim()[0],ax.get_ylim()[1],i)
            else:
                ax.scatter(df[j],df[i],s=10)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            axis_border(ax,'black',1.5)
    for i,x in enumerate(col):
        axs[0][i].set_title(x,fontsize=20,family='monospace')
        axs[i][0].set_ylabel(x,fontsize=20,family='monospace')
    plt.tight_layout()
