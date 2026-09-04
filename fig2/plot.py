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

fig = plt.figure(figsize = (40, 7))
plt.subplots_adjust(hspace=0.1,wspace=0.3)
gs = gridspec.GridSpec(3, 3)
ax00=fig.add_subplot(gs[:,0])
ax01=fig.add_subplot(gs[0,1])
ax11=fig.add_subplot(gs[1,1])
ax21=fig.add_subplot(gs[2,1])
ax02=fig.add_subplot(gs[:,2])

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

schmn=mpimg.imread('spatial_model.png')
#print(schmn.shape)
schm=fix_alpha_edge_bleed(schmn[1:-1,1:-1,:])
imagebox1 = OffsetImage(schm, zoom=0.38,interpolation='hanning')
ab1 = AnnotationBbox(imagebox1, (1.2,0.5),frameon=False,pad=0.,xycoords='axes fraction')
#imagebox1.image.set_clip_box(ax00.bbox)
#imagebox1.image.set_clip_on(True)
ax00.add_artist(ab1)

ax00.axis('off')

xts=np.loadtxt('xts.txt')
dt=0.01
ts=(np.arange(np.shape(xts)[0])+1)*dt
ax01.plot(ts,xts[:,0],color='#C00000')
ax11.plot(ts,xts[:,1],color='#0099FF')
#ax21.plot(ts,xts[:,2],color='k')
ax21.axis('off')

ax01.axes.get_xaxis().set_ticks([])

ax01.set_xlim(0,100)
ax11.set_xlim(0,100)
ax21.set_xlim(0,100)
ax01.set_ylim(-10,10)
ax11.set_ylim(-9,9)
ax21.set_ylim(-9,9)

ax01.axes.get_xaxis().set_ticks([])
ax01.axes.get_yaxis().set_ticks([-5,5])
ax11.axes.get_yaxis().set_ticks([-5,5])

ax01.hlines(0,0,100,zorder=-np.inf,alpha=0.2,color='k')
ax11.hlines(0,0,100,zorder=-np.inf,alpha=0.2,color='k')
#ax21.hlines(0,0,100,zorder=-np.inf,alpha=0.2,color='k')

ax11.set_xlabel(r'time t')
ax01.set_ylabel(r'x(t)')
ax11.set_ylabel(r'f(t)')
ax01.yaxis.label.set_color('#C00000')
ax11.yaxis.label.set_color('#0099FF')

H=1
F=0.5
Df=2.
Dv=2.

M=500
perfarr=np.zeros((M,M))
Gs=np.linspace(0,2,M)
Js=np.linspace(0,2,M)
kval=1.
for i in range(M):
    for j in range(M):
        perfarr[j,i]=Gs[i]*kval*Js[j]*(F*H*(F+H)-Gs[i]*kval*Js[j])/(Df*(F+H)*Js[j]**2+Dv*(F**2*(F+H)+Gs[i]*kval*Js[j]))/(H**3/Dv)
        if perfarr[j,i]<0:
            perfarr[j,i]=np.nan

rho=F/H
pmaxn=rho*(1+rho)*((1+rho)**0.5-rho**0.5)**2
GJP=ax02.contourf(Gs,Js,perfarr,levels=np.linspace(0.,pmaxn,12),cmap='viridis',vmin=0,vmax=pmaxn)
ax02.plot(Gs,F*H*(F+H)/kval/Gs,color='r',lw=8,linestyle='-',label=r'$\mathrm{(G\;J)_{~lim}}$')

Jopts=((Dv*F**3*(F+H)**3*(Df*F*H**2*(F+H)+Dv*Gs**2*kval**2))**0.5-Dv*F**2*Gs*kval*(F+H))
Jopts/=(Df*F*H*(F+H)**2+Dv*Gs**2*kval**2)

Gopts=1/kval*(F+H)*(Df*Js**2+Dv*F**2)*((1+Dv*F*H/(Df*Js**2+Dv*F**2))**0.5-1)/Dv/Js

ax02.vlines(0.6,0,2,color='k',lw=4,alpha=0.5,linestyle=':')
ax02.hlines(0.6,0,2,color='k',lw=4,alpha=0.5,linestyle='--')
ax02.annotate(r'a',xy=(1.8,0.7),xycoords='data',zorder=np.inf,color='k',alpha=1.)
ax02.annotate(r'b',xy=(0.67,1.8),xycoords='data',zorder=np.inf,color='k',alpha=1.)

ax02.set_xlim(0,2)
ax02.set_ylim(0,2)
ax02.set_xlabel(r'$\mathrm{sensory~gain~G}$')
ax02.set_ylabel(r'$\mathrm{actuator~gain~J}$')
GJPc=plt.colorbar(GJP,ticks=[0,0.05,0.1,0.15,pmaxn])#,title=r'$\mathcal{P}/\mathcal{P}_{0}$')
GJPc.ax.set_yticklabels([r'$0.00$', r'$0.05$', r'$0.10$',r'$0.15$',r'$\mathcal{P}_{\mathrm{max}}/\mathcal{P}_{0}$'])
ax02.legend(frameon='False',framealpha=0.0,loc='upper center',handletextpad=0.9,bbox_to_anchor=(0.75, 1.02),title=r'$\mathrm{\mathcal{P}/\mathcal{P}_{0}}$')
ax02.set_xticks([0,1,2])
ax02.set_yticks([0,1,2])

ax00.annotate(r'A',xy=(-0.05,1.05),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'B',xy=(1.05,1.05),xycoords='axes fraction',zorder=np.inf)
ax00.annotate(r'C',xy=(2.4,1.05),xycoords='axes fraction',zorder=np.inf)

plt.savefig('fig_spatialmodel.png',bbox_inches='tight',pad_inches=0.1)
#plt.tight_layout()
#plt.show()
