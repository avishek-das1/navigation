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

plt.rc('font', size = 36)
#plt.rc('text', usetex = True)
plt.rc('mathtext',rm='dejavusans')
plt.rc('mathtext',fontset='dejavusans')

fig = plt.figure(figsize = (25, 20))
plt.subplots_adjust(hspace=0.4,wspace=0.3)
gs = gridspec.GridSpec(6, 2)
ax00=fig.add_subplot(gs[:3,0])
ax01a=fig.add_subplot(gs[0,1])
ax01b=fig.add_subplot(gs[1,1])
ax01c=fig.add_subplot(gs[2,1])
ax10a=fig.add_subplot(gs[3,0])
ax10b=fig.add_subplot(gs[4,0])
ax10c=fig.add_subplot(gs[5,0])
ax11=fig.add_subplot(gs[3:,1])

def fix_alpha_edge_bleed(img):
    """Replace RGB under transparent pixels with the nearest opaque pixel's RGB,
    so resampling near the alpha boundary doesn't blend in a hidden background color."""
    if img.shape[-1] != 4:
        return img  # no alpha channel; not the issue
    img = img.copy()
    mask = img[..., 3] > 0  # opaque-ish pixels
    if mask.all() or not mask.any():
        return img
    _, indices = distance_transform_edt(~mask, return_distances=True, return_indices=True)
    for c in range(3):
        img[..., c] = img[..., c][tuple(indices)]
    return img

schmn=mpimg.imread('temporal_model.png')
schm=fix_alpha_edge_bleed(schmn[1:-1,1:-1,:])
imagebox1 = OffsetImage(schm, zoom=0.37,interpolation='hanning')
ab1 = AnnotationBbox(imagebox1, (0.95,0.5),frameon=False,pad=0.,xycoords='axes fraction')
ax00.add_artist(ab1)

ax00.axis('off')

xts=np.loadtxt('xts.txt')[2000:6000,:]
dt=0.01
ts=(np.arange(np.shape(xts)[0])+1)*dt
ax01a.plot(ts,xts[:,1],color='#C00000')
ax01b.plot(ts,xts[:,0],color='#0099FF')

ax01a.axes.get_xaxis().set_ticks([])

ax01a.set_xlim(0,40)
ax01b.set_xlim(0,40)
ax01a.set_ylim(-3,3)
ax01b.set_ylim(-2,2)
ax01c.axis('off')

ax01a.axes.get_xaxis().set_ticks([])
ax01a.axes.get_yaxis().set_ticks([-3,0,3])
ax01b.axes.get_yaxis().set_ticks([-2,0,2])

ax01a.hlines(0,0,100,zorder=-np.inf,alpha=0.2,color='k')
ax01b.hlines(0,0,100,zorder=-np.inf,alpha=0.2,color='k')

ax01b.set_xlabel(r'time t')
ax01a.set_ylabel(r'v(t)')
ax01b.set_ylabel(r'f(t)')
ax01a.yaxis.label.set_color('#C00000')
ax01b.yaxis.label.set_color('#0099FF')

ax10a.set_xticks([])
ax10b.set_xticks([])

pvals=np.loadtxt('pvalsfull.txt')
tv2f=np.loadtxt('tv2ffull.txt')
tf2v=np.loadtxt('tf2vfull.txt')

ax10a.errorbar(pvals[:,0],pvals[:,1],yerr=pvals[:,2],marker='o',fillstyle='none',linestyle='none',ms=20,mew=3,color='black',capsize=5)
ax10b.errorbar(tv2f[:,0],tv2f[:,1],yerr=tv2f[:,2],marker='x',fillstyle='none',linestyle='none',ms=20,mew=3,color='chocolate',capsize=5)
ax10c.errorbar(tf2v[:,0],tf2v[:,1],yerr=tf2v[:,2],marker='^',fillstyle='none',linestyle='none',ms=20,mew=3,color='seagreen',capsize=5)

#k33 is F, k22 is H from the notation in the paper 
k33=1.
k32=0.08
k22=1.
D2=0.5
D3=0.1

M=100
epss=np.linspace(0,1.05,M)
pvalsth=epss*k32*D2/k22**2/(k22+k33)

r2=(k22**2+D2/D3*k32**2)**0.5
ff0=0.5*(r2-k22)*epss/epss
#this is the ff2 expression when k22 and k33 are equal.
ff2lim=epss**2*D3*(r2-k22)/r2*((r2**2-k22**2)/4/k22**4+r2/k22/(4*r2**2-k22**2)+(r2**2-k22**2)*(r2+k22)/k22**3/(2*r2+k22)**2-3*r2*(r2-k22)/2/(4*r2**2-k22**2)**2)
ffsmallk=k32**2*D2/4/k22*(1/D3*epss/epss+2*epss**2/k22/k33/(2*k22+k33))

fb=epss**2*D3/4/k22/k33

ax10a.plot(epss,pvalsth,color='black',lw=4)
ax10b.plot(epss,ff0+ff2lim,color='chocolate',lw=4)
ax10c.plot(epss,fb,color='seagreen',lw=4)

ax10a.set_xlim(0,1.05)
ax10b.set_xlim(0,1.05)
ax10c.set_xlim(0,1.05)
ax10c.set_ylim(-0.005,0.03)

ax10a.set_ylabel(r'$\mathcal{P}$',labelpad=10)
ax10b.set_ylabel(r'$\dot{\mathcal{T}}_{\mathrm{v\to f}}$',labelpad=10)
ax10c.set_ylabel(r'$\dot{\mathcal{T}}_{\mathrm{f\to v}}$',labelpad=10)
ax10c.set_xlabel(r'$\mathrm{actuator~gain~J}$')


Jmi=10
p0=(D2/k22)**0.5
H=k22
F=k33
rho=F/H
ax11.errorbar(tf2v[:Jmi,1]/F,pvals[:Jmi,1]/p0,xerr=tf2v[:Jmi,2]/F,yerr=pvals[:Jmi,2]/p0,marker='s',fillstyle='none',linestyle='none',ms=20,mew=3,color='navy',capsize=5)
infoth=4/(1+1/rho)*(tf2v[:Jmi,1]/F)**0.5*(tv2f[:Jmi,1]/H)**0.5
infotherr=infoth*((tf2v[:Jmi,2]/2/tf2v[:Jmi,1])**2+(tv2f[:Jmi,2]/2/tv2f[:Jmi,1])**2)**0.5/2
infothup=infoth+2*infotherr
infothdown=infoth-2*infotherr
ax11.plot(tf2v[:Jmi,1]/F,infoth[:Jmi],color='navy',lw=4,label=r'$\mathrm{4\;\frac{\rho}{1+\rho}}\sqrt{\mathcal{T}_{FF}}\sqrt{\mathcal{T}_{FB}}$')
ax11.fill_between(tf2v[:Jmi,1]/F,infothdown[:Jmi],infothup[:Jmi],color='navy',alpha=0.2)

ax11.legend(frameon='False',framealpha=0.0,loc='lower right',handletextpad=0.3,bbox_to_anchor=(1., -0.),labelcolor='navy')

ax11.set_xlabel(r'$\mathcal{T}_{\mathrm{FB}}\mathrm{~[nats]}$')
ax11.set_ylabel(r'$\mathcal{P}/\mathcal{P}_{0}$',labelpad=10)

ax00.annotate(r'A',xy=(-0.25,1.0),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'B',xy=(1.05,1.0),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'C',xy=(-0.25,-0.1),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'D',xy=(1.05,-0.1),xycoords='axes fraction',zorder=np.inf)

plt.savefig('fig_temporalmodel.png',bbox_inches='tight',pad_inches=0.1)
#plt.tight_layout()
#plt.show()
