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
import matplotlib as mpl

plt.rc('font', size = 30)
#plt.rc('text', usetex = True)
plt.rc('mathtext',rm='dejavusans')
plt.rc('mathtext',fontset='dejavusans')

fig = plt.figure(figsize = (14, 20))
plt.subplots_adjust(hspace=0.2,wspace=0.3)
gs = gridspec.GridSpec(2,1)
ax00=fig.add_subplot(gs[0,0])
ax10=fig.add_subplot(gs[1,0])

#All in real units of seconds
P0=0.5106
H=0.496
Df=9.6/10**2

t_10_6=np.loadtxt('F10_tauE6_smallJ_tf2v_tv2f.txt')
t_10_10=np.loadtxt('F10_tauE10_smallJ_tf2v_tv2f.txt')
tl_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f.txt')

v_10_6=np.loadtxt('F10_tauE6_smallJ_v.txt')
v_10_10=np.loadtxt('F10_tauE10_smallJ_v.txt')
vl_10_6=np.loadtxt('F10_tauE6_largeJ_v.txt')

F=1/10
rho=F/H
ax00.errorbar(t_10_10[:,1]/F,v_10_10[:,1]/P0,xerr=t_10_10[:,2]/F,yerr=v_10_10[:,2]/P0,marker='s',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color='#0099FF',label=r'$\mathrm{g=0.017~mm^{-1}}$')
t_10_10[:,3]=np.average(t_10_10[:,3])
t_10_10[:,4]/=10**0.5
infoth=4*rho/(1+rho)*(t_10_10[:,1]/F)**0.5*(t_10_10[:,3]/H)**0.5
infotherr=infoth*((t_10_10[:,2]/2/t_10_10[:,1])**2+(t_10_10[:,4]/2/t_10_10[:,3])**2)**0.5/2
infothup=infoth+2*infotherr
infothdown=infoth-2*infotherr
ax00.plot(t_10_10[:,1]/F,infoth[:],color='#0099FF',lw=4)
ax00.fill_between(t_10_10[:,1]/F,infothdown[:],infothup[:],color='#0099FF',alpha=0.2)

F=1/10
rho=F/H
ax00.errorbar(t_10_6[:,1]/F,v_10_6[:,1]/P0,xerr=t_10_6[:,2]/F,yerr=v_10_6[:,2]/P0,marker='o',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color='#C00000',label=r'$\mathrm{g=0.028~mm^{-1}}$')
t_10_6[:,3]=np.average(t_10_6[:,3])
t_10_6[:,4]/=10**0.5
infoth=4*rho/(1+rho)*(t_10_6[:,1]/F)**0.5*(t_10_6[:,3]/H)**0.5
infotherr=infoth*((t_10_6[:,2]/2/t_10_6[:,1])**2+(t_10_6[:,4]/2/t_10_6[:,3])**2)**0.5/2
infothup=infoth+2*infotherr
infothdown=infoth-2*infotherr
ax00.plot(t_10_6[:,1]/F,infoth[:],color='#C00000',lw=4)
ax00.fill_between(t_10_6[:,1]/F,infothdown[:],infothup[:],color='#C00000',alpha=0.2)

F=1/10
rho=F/H
ax10.errorbar(tl_10_6[:,1]/F,vl_10_6[:,1]/P0,xerr=tl_10_6[:,2]/F,yerr=vl_10_6[:,2]/P0,marker='o',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color='#C00000',label=r'$\mathrm{g=0.028~mm^{-1}}$')


ax00.legend(frameon='False',framealpha=0.0,loc='upper left',handletextpad=0.3,bbox_to_anchor=(0. ,1.0))
ax10.legend(frameon='False',framealpha=0.0,loc='upper right',handletextpad=0.3,bbox_to_anchor=(1.0 ,1.0))

ax00.set_xlabel(r'$\mathcal{T}_{\mathrm{FB}}\mathrm{~[nats]}$',labelpad=10)
ax00.set_ylabel(r'$\mathcal{P}/\mathcal{P}_{0}$',labelpad=10)
ax10.set_xlabel(r'$\mathcal{T}_{\mathrm{FB}}\mathrm{~[nats]}$',labelpad=10)
ax10.set_ylabel(r'$\mathcal{P}/\mathcal{P}_{0}$',labelpad=10)

ax00.annotate(r'$\mathrm{\mathcal{P}/\mathcal{P}_{0}=4\;\frac{\rho}{1+\rho}\sqrt{\mathcal{T}_{FF}}\sqrt{\mathcal{T}_{FB}}}$',xy=(0.25,1.05),xycoords='axes fraction',zorder=np.inf)

ax00.annotate(r'A',xy=(-0.2,1.05),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'B',xy=(-0.2,-0.33),xycoords='axes fraction',zorder=np.inf)

plt.savefig('fig_ecoli.png',bbox_inches='tight',pad_inches=0.1)
#plt.tight_layout()
#plt.show()
