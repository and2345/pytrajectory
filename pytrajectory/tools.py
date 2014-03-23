import numpy as np
import pylab as plt

def plot(self):
    #provides graphics for each system variable, manipulated variable and error function
    #plots the solution of the simulation
    #at the end the error at the final state will be calculated
    
    log.info("Plot")
    
    z=self.n+self.m+len(self.eqind)
    z1=np.floor(np.sqrt(z))
    z2=np.ceil(z/z1)
    t=self.A[0]
    xt = self.A[1]
    ut= self.A[2]
    
    
    log.info("Ending up with:")
    for i,xx in enumerate(self.x_sym):
        log.info(str(xx)+" : "+str(xt[-1:][0][i]))
    
    log.info("Shoul be:")
    for i,xx in enumerate(self.x_sym):
        log.info(str(xx)+" : "+str(self.xb[xx]))
    
    log.info("Difference")
    for i,xx in enumerate(self.x_sym):
        log.info(str(xx)+" : "+str(self.xb[xx]-xt[-1:][0][i]))
    
    
    if not __name__=='__main__':
        return
    
    def setAxLinesBW(ax):
        """
        Take each Line2D in the axes, ax, and convert the line style to be 
        suitable for black and white viewing.
        """
        MARKERSIZE = 3
    
    
        ##?? was bedeuten die Zahlen bei dash[...]?
        COLORMAP = {
            'b': {'marker': None, 'dash': (None,None)},
            'g': {'marker': None, 'dash': [5,5]},
            'r': {'marker': None, 'dash': [5,3,1,3]},
            'c': {'marker': None, 'dash': [1,3]},
            'm': {'marker': None, 'dash': [5,2,5,2,5,10]},
            'y': {'marker': None, 'dash': [5,3,1,2,1,10]},
            'k': {'marker': 'o', 'dash': (None,None)} #[1,2,1,10]}
            }
    
        for line in ax.get_lines():
            origColor = line.get_color()
            line.set_color('black')
            line.set_dashes(COLORMAP[origColor]['dash'])
            line.set_marker(COLORMAP[origColor]['marker'])
            line.set_markersize(MARKERSIZE)
    
    def setFigLinesBW(fig):
        """
        Take each axes in the figure, and for each line in the axes, make the
        line viewable in black and white.
        """
        for ax in fig.get_axes():
            setAxLinesBW(ax)
    
    
    plt.rcParams['figure.subplot.bottom']=.2
    plt.rcParams['figure.subplot.top']= .95
    plt.rcParams['figure.subplot.left']=.13
    plt.rcParams['figure.subplot.right']=.95
    
    plt.rcParams['font.size']=16
    
    plt.rcParams['legend.fontsize']=16
    plt.rc('text', usetex=True)
    
    
    plt.rcParams['xtick.labelsize']=16
    plt.rcParams['ytick.labelsize']=16
    plt.rcParams['legend.fontsize']=20
    
    plt.rcParams['axes.titlesize']=26
    plt.rcParams['axes.labelsize']=26
    
    
    plt.rcParams['xtick.major.pad']='8'
    plt.rcParams['ytick.major.pad']='8'
    
    mm = 1./25.4 #mm to inch
    scale = 3
    fs = [100*mm*scale, 60*mm*scale]
    
    fff=plt.figure(figsize=fs, dpi=80)
    
    
    PP=1
    for i,xx in enumerate(self.x_sym):
        plt.subplot(int(z1),int(z2),PP)
        PP+=1
        plt.plot(t,xt[:,i])
        plt.xlabel(r'$t$')
        plt.title(r'$'+str(xx)+'(t)$')
    
    for i,uu in enumerate(self.u_sym):
        plt.subplot(int(z1),int(z2),PP)
        PP+=1
        plt.plot(t,ut[:,i])
        plt.xlabel(r'$t$')
        plt.title(r'$'+str(uu)+'(t)$')
    
    for hh in self.H:
        plt.subplot(int(z1),int(z2),PP)
        PP+=1
        plt.plot(t,self.H[hh])
        plt.xlabel(r'$t$')
        plt.title(r'$H_'+str(hh+1)+'(t)$')
    
    setFigLinesBW(fff)
    
    plt.tight_layout()
    
    plt.show()
