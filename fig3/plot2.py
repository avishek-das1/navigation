import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle, FancyBboxPatch
from scipy.ndimage import distance_transform_edt

plt.rc('font', size = 30)
#plt.rc('text', usetex = True)
plt.rc('mathtext',rm='dejavusans')
plt.rc('mathtext',fontset='dejavusans')

fig = plt.figure(figsize = (14, 20))
plt.subplots_adjust(hspace=0.3,wspace=0.3)
gs = gridspec.GridSpec(2,1)
ax00=fig.add_subplot(gs[0,0])
ax10=fig.add_subplot(gs[1,0])


M=5000
x=np.logspace(-6,3,M)
y=2/(((2*x+1)**2-1)**0.5+((2*x+1)**2-1)**(-0.5))

z1=2*((2*x+1)**2-1)**0.5
z2=2*(x*0+1)/2
z3=2/((2*x+1)**2-1)**0.5

u1=4*x**0.5
u3=1/x
ax00.plot(x,y,color='k',lw=3,label=r'$\mathcal{P}\;(\mathcal{T}_{\mathrm{FF}},\mathcal{T}_{\mathrm{FB}})\vert_{\mathrm{shallow}}/\mathcal{P}_{0}$')
ax00.plot(x,z2,color='seagreen',lw=3,linestyle='-')
ax00.plot(x,u1,color='#C00000',lw=3)
ax00.plot(x,u3,color='navy',lw=3)
ax00.vlines((2**0.5-1)/2,-10,10,color='grey',linestyle='--',lw=4)
ax00.set_xscale('log')
ax00.set_ylim(-0.05,1.2)
ax00.set_xticks([1e-4,1e-2,(2**0.5-1)/2,1])
ax00.set_yticks([0,0.5,1])
ax00.set_xticklabels([r'$10^{-4}$',r'$10^{-2}$',r'$\mathcal{T}_{\mathrm{FB}}^{~*}$',r'$10^{0}$'])
ax00.set_xlabel(r'$\mathcal{T}_{\mathrm{FB}}~[\mathrm{nats}]$',labelpad=10)
ax00.set_ylabel(r'$\mathcal{P}/\mathcal{P}_{0}$')
ax00.set_xlim(1e-5,1e2)

ax00.annotate(r'$4\mathcal{T}_{\mathrm{FF}}\sqrt{\mathcal{T}_{\mathrm{FB}}}$',xy=(0.05,0.15),xycoords='axes fraction',color='k')
ax00.annotate(r'$\mathcal{T}_{\mathrm{FF}}/\mathcal{T}_{\mathrm{FB}}$',xy=(0.85,0.15),xycoords='axes fraction',color='k')
ax00.annotate(r'$\mathcal{T}_{\mathrm{FF}}$',xy=(0.9,0.87),xycoords='axes fraction',color='k')

ax00.legend(frameon='False',framealpha=0.0,loc='upper left',handletextpad=0.3,bbox_to_anchor=(-0.01, 0.8),labelcolor='k')

G=1
H=1
J=1
F=0.5
Df=0.1
Dv=2.
kval=3

A=(G*kval/H**2*(Dv/Df)**0.5)
B=(J/F*(Df/Dv)**0.5)
AB=A*B

M=1000
xs=np.linspace(0,50,M)

ys=AB*xs*(1+xs-AB)/(xs*(1+xs)*(1+B**2)+AB)
ax10.plot(xs,ys,lw=3,color='#0099FF')
ax10.hlines(A/(B+1/B),0,50,lw=3,linestyle='--',color='k')

#ax10.set_xscale('log')
ax10.set_ylim(0,1.2*A/(B+1/B))
ax10.set_xlim(0,50)
ax10.set_xlabel(r'$\mathrm{\rho=F/H}$')
ax10.set_ylabel(r'$\mathrm{\mathcal{P}/\mathcal{P}_{0}}$',labelpad=35)

import matplotlib.transforms as mtransforms

def rainbow_annotate(ax, x, y, strings, colors, **kwargs):
    renderer = ax.figure.canvas.get_renderer()
    t =ax.transData
    for s, c in zip(strings, colors):
        text = ax.annotate(s, xy=(x, y), xycoords=t, color=c, **kwargs)
        text.draw(renderer)
        bbox = text.get_window_extent(renderer)
        t = mtransforms.offset_copy(text.get_transform(), x=bbox.width, units='dots')

ax10.annotate(r'$\mathcal{P}\;(\mathcal{T}_{\mathrm{FF}},\mathcal{T}_{\mathrm{FB}})\vert_{\mathrm{shallow}}/\mathcal{P}_{0}$',xy=(30,5.3),xycoords='data',color='k')
rainbow_annotate(ax10, 30,3.5,
                  [r'$\mathcal{P}\;(\mathcal{T}_{\mathrm{FF}},\mathcal{T}_{\mathrm{FB}},$' , r'$\mathrm{\rho}$', r'$)\vert_{\mathrm{steep}}/\mathcal{P}_{0}$'],
                  ['#0099FF', 'chocolate','#0099FF'], va='bottom')


ax10.set_xticks([AB-1,20,40])
ax10.set_xticklabels([r'$\mathrm{\rho_{lim}(\mathcal{T}_{FF},\mathcal{T}_{FB})}$','20','40'])
ax10.tick_params(axis='x', which='major', pad=15)
ax10.get_xticklabels()[0].set_color('chocolate')

def rainbow_annotate(ax, x, y, strings, colors, **kwargs):
    iter=0
    renderer = ax.figure.canvas.get_renderer()
    t =ax.transData
    for s, c in zip(strings, colors):
        if iter==0:
            xoffset=0
            yoffset=0.04
        else:
            xoffset=0
            yoffset=0

        text = ax.annotate(s, xy=(x+xoffset, y+yoffset), xycoords=t, color=c, **kwargs)
        text.draw(renderer)
        bbox = text.get_window_extent(renderer)
        t = mtransforms.offset_copy(text.get_transform(), x=bbox.width, units='dots')
        iter+=1

rainbow_annotate(ax00, 1e-4,1.4,
                  [r'$\mathrm{\mathcal{P}/\mathcal{P}_{0}}$',r'$\mathrm{\;=\;\frac{2\mathcal{T}_{\mathrm{FF}}}{ [(2\mathcal{T}_{\mathrm{FB}}+1)^{2}-1]^{1/2}+[(2\mathcal{T}_{\mathrm{FB}}+1)^{2}-1]^{-1/2}}}$'],
                  ['k', 'k'], va='bottom')

def rainbow_annotate(ax, x, y, strings, colors, **kwargs):
    iter=0
    renderer = ax.figure.canvas.get_renderer()
    t =ax.transData
    for s, c in zip(strings, colors):
        if iter!=5:
            xoffset=0
            yoffset=0.04
        else:
            xoffset=0
            yoffset=0
        if iter==1 or 7:
            text = ax.annotate(s, xy=(x+xoffset, y+yoffset), xycoords=t,color=c, **kwargs)
        else:
            text = ax.annotate(s, xy=(x+xoffset, y+yoffset), xycoords=t, color=c, **kwargs)
        text.draw(renderer)
        bbox = text.get_window_extent(renderer)
        t = mtransforms.offset_copy(text.get_transform(), x=bbox.width, units='dots')
        iter+=1

rainbow_annotate(ax00, 1e-4,1.2,[r'$\mathrm{\mathcal{P}/\mathcal{P}_{0}\leq MIN}$','{',r'$\mathrm{4\mathcal{T}_{FF}\sqrt{\mathcal{T}_{FB}}}$', r',',r'$\mathrm{\mathcal{T}_{FF}}$',r',',r'$\mathrm{\frac{\mathcal{T}_{FF}}{\mathcal{T}_{FB}}}$','}'],['k','k','#C00000','k','seagreen','k','navy','k'], va='bottom')


ax00.annotate(r'A',xy=(-0.13,1.2),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'B',xy=(-0.13,-0.33),xycoords='axes fraction',zorder=np.inf)

plt.savefig('fig_spatialinfo.png',bbox_inches='tight',pad_inches=0.1)
#plt.tight_layout()
#plt.show()
