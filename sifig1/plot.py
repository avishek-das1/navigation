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
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable


plt.rc('font', size = 30)
#plt.rc('text', usetex = True)
plt.rc('mathtext',rm='dejavusans')
plt.rc('mathtext',fontset='dejavusans')

fig = plt.figure(figsize = (25, 10))
plt.subplots_adjust(hspace=0.2,wspace=0.3)
gs = gridspec.GridSpec(1,2)
ax00=fig.add_subplot(gs[0,0])
ax10=fig.add_subplot(gs[0,1])

#All in real units of seconds
P0=0.5106
H=0.496
Df=9.6/10**2

tl_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f.txt')
tlby5_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f_Dfby5.txt')
tlby20_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f_Dfby20.txt')
tlby100_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f_Dfby100.txt')
tlby400_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f_Dfby400.txt')
tlby1600_10_6=np.loadtxt('F10_tauE6_largeJ_tf2v_tv2f_Dfby1600.txt')

vl_10_6=np.loadtxt('F10_tauE6_largeJ_v.txt')
vlby5_10_6=np.loadtxt('F10_tauE6_largeJ_v_Dfby5.txt')
vlby20_10_6=np.loadtxt('F10_tauE6_largeJ_v_Dfby20.txt')
vlby100_10_6=np.loadtxt('F10_tauE6_largeJ_v_Dfby100.txt')
vlby400_10_6=np.loadtxt('F10_tauE6_largeJ_v_Dfby400.txt')
vlby1600_10_6=np.loadtxt('F10_tauE6_largeJ_v_Dfby1600.txt')


corr1=np.loadtxt('corr_tauD0.1.txt')
corr2=np.loadtxt('corr_tauD0.2.txt')
corr3=np.loadtxt('corr_tauD0.3.txt')
corr4=np.loadtxt('corr_tauD0.6.txt')

ax00.plot(corr1[:,0],corr1[:,1],lw=3,color='k',ls='-',label=r'$0.062~s^{-1}$')
ax00.plot(corr2[:,0],corr2[:,1],lw=3,color='k',ls='--',label=r'$0.031~s^{-1}$')
ax00.plot(corr3[:,0],corr3[:,1],lw=3,color='k',ls='-.',label=r'$0.021~s^{-1}$')
ax00.plot(corr4[:,0],corr4[:,1],lw=3,color='k',ls=':',label=r'$0.010~s^{-1}$')

ax00.set_ylabel(r'$\mathrm{C_{vv}(t)|_{J=0}}$',labelpad=10)
ax00.set_xlabel(r'$\mathrm{t}$',labelpad=10)

ax00.set_xlim(0,2.5)
ax00.set_ylim(-1.3,0)

ax00.legend(frameon='False',framealpha=0.0,loc='lower left',handletextpad=0.3,bbox_to_anchor=(0., 0.),title=r'$\mathrm{D_{run}}\qquad $')

F=1/10
rho=F/H

cmap = plt.get_cmap('rainbow')
colors2 = np.concatenate(([cmap(i) for i in np.linspace(0, 1, 11)],[cmap(1.0) for i in np.linspace(0,1,9)]))
for i in range(20):		
	ax10.errorbar(tl_10_6[i,1]/F,vl_10_6[i,1]/P0,xerr=tl_10_6[i,2]/F,yerr=vl_10_6[i,2]/P0,marker='o',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i])
	ax10.errorbar(tlby5_10_6[i,1]/F,vlby5_10_6[i,1]/P0,xerr=tlby5_10_6[i,2]/F,yerr=vlby5_10_6[i,2]/P0,marker='s',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i])
	ax10.errorbar(tlby20_10_6[i,1]/F,vlby20_10_6[i,1]/P0,xerr=tlby20_10_6[i,2]/F,yerr=vlby20_10_6[i,2]/P0,marker='^',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i])
	ax10.errorbar(tlby100_10_6[i,1]/F,vlby100_10_6[i,1]/P0,xerr=tlby100_10_6[i,2]/F,yerr=vlby100_10_6[i,2]/P0,marker='v',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i])
	ax10.errorbar(tlby400_10_6[i,1]/F,vlby400_10_6[i,1]/P0,xerr=tlby400_10_6[i,2]/F,yerr=vlby400_10_6[i,2]/P0,marker='x',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i])

i=19
ax10.errorbar(tl_10_6[i,1]/F,vl_10_6[i,1]/P0,xerr=tl_10_6[i,2]/F,yerr=vl_10_6[i,2]/P0,marker='o',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i],label='1')
ax10.errorbar(tlby5_10_6[i,1]/F,vlby5_10_6[i,1]/P0,xerr=tlby5_10_6[i,2]/F,yerr=vlby5_10_6[i,2]/P0,marker='s',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i],label='1/5')
ax10.errorbar(tlby20_10_6[i,1]/F,vlby20_10_6[i,1]/P0,xerr=tlby20_10_6[i,2]/F,yerr=vlby20_10_6[i,2]/P0,marker='^',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i],label='1/20')
ax10.errorbar(tlby100_10_6[i,1]/F,vlby100_10_6[i,1]/P0,xerr=tlby100_10_6[i,2]/F,yerr=vlby100_10_6[i,2]/P0,marker='v',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i],label='1/100')
ax10.errorbar(tlby400_10_6[i,1]/F,vlby400_10_6[i,1]/P0,xerr=tlby400_10_6[i,2]/F,yerr=vlby400_10_6[i,2]/P0,marker='x',fillstyle='none',linestyle='none',ms=20,mew=3,capsize=5,color=colors2[i],label='1/400')

ax10.set_yscale('log')
ax10.legend(frameon='False',framealpha=0.0,loc='center right',handletextpad=0.3,bbox_to_anchor=(1.4, 0.6),title=r'$\mathrm{D}_{\mathrm{f}}\;/\;\mathrm{D}_{\mathrm{f;WT}}$')

ax10.fill_betweenx(np.array([1e-3,1e0]),2.5,3.9,color='grey',alpha=0.3)
ax10.set_ylim(3.5e-3,1.4e-1)

ax10.set_xlabel(r'$\mathcal{T}_{\mathrm{FB}}\mathrm{~[nats]}$',labelpad=10)
ax10.set_ylabel(r'$\mathcal{P}/\mathcal{P}_{0}$',labelpad=10)


N=200
colors3 = np.concatenate(([cmap(i) for i in np.linspace(0, 1, 11*10)],[cmap(1.0) for i in np.linspace(0,1,9*10)]))
new_cmap = mcolors.LinearSegmentedColormap.from_list('rainbow_capped', colors3, N=N)
norm = mcolors.Normalize(vmin=0, vmax=1)

divider = make_axes_locatable(ax10)
cax = divider.append_axes("top", size="5%", pad=0.5)
cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=new_cmap), cax=cax, orientation='horizontal')
cax.xaxis.set_ticks_position('top')
cax.xaxis.set_label_position('top')
cb.set_ticks([0,0.25,0.5,0.75])
cb.set_ticklabels(['1','10','100','1000'],fontsize=30)
cax.set_title(r'$\mathrm{J}\;/\;\mathrm{J}_{\mathrm{WT}}$',x=1.1,y=0.1,fontsize=30)

divider = make_axes_locatable(ax00)
cax = divider.append_axes("top", size="5%", pad=0.5)
cax.axis('off')

ax00.annotate(r'A',xy=(-0.3,1.05),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'B',xy=(1.05,1.05),xycoords='axes fraction',zorder=np.inf)

plt.savefig('figsi_ecoli.png',bbox_inches='tight',pad_inches=0.1)
#plt.tight_layout()
#plt.show()
