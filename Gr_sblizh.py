from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.lines as mlines
import matplotlib
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
arial_font = fm.FontProperties(fname = "Fonts/arial.ttf")

import numpy as np

sp1 = ["","","","o","v","^","<",">","1","2","3","4","s","p","*","h","H","+","x","D","d",
       "o","v","^","<",">","1","2","3","4","s","p","*","h","H","+","x","D","d"]

sp2 = ["-","--","-.","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",
       "--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--",
       "--","--","--"]
sp3 = ["b","g","r","c","m","y","k","b","g","r","c","m","y","k","b","g","r","c",
       "m","y","k","b","g","r","c","m","y","k","b","g","r","c","m","y","k","b","g","r","c"]


def Sx_sb(n,gr,axi,shr_gr,Tiks,otp):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    k=-1

    new_ax = [axi[0],axi[1],min(axi[2]*-1,axi[3]*-1),max(axi[2]*-1,axi[3]*-1)]
    if new_ax[2]>-0.0001:
        new_ax[2]=-100
    if new_ax[3]<0.0001:
        new_ax[3]=100
    
    ax.plot(new_ax[0:2],[0,0],color = "k",linewidth=5, label="Расч.")
    
    for i in gr:
        k+=1
        for j in range(len(gr[i])):
            if j == 0:
                ax.plot(gr[i][j][0],[gr[i][j][1][0]*-1,gr[i][j][1][1]*-1],
                        label=str(i),
                        linestyle = sp2[k],
                        marker = sp1[k],
                        color = sp3[k],
                        markerfacecolor = sp3[k],
                        markersize=9)
            else:
                ax.plot(gr[i][j][0], [gr[i][j][1][0]*-1,gr[i][j][1][1]*-1],
                        linestyle = sp2[k],
                        marker = sp1[k],
                        color = sp3[k],
                        markerfacecolor = sp3[k],
                        markersize=9)
    for i in otp:
        ax.plot(i[0],i[1],
                marker = '|',
                color = 'k',
                markerfacecolor = 'k',
                markersize=30)
    
    
    ax.axis(new_ax)
    ax.grid(True) # Включаем сетку
    ax.set_xlabel(u'Длина, км',fontsize=shr_gr) # Подпись оси х
    ax.set_ylabel(u'Ширина, м',fontsize=shr_gr) # Подпись оси у


    ax.legend(frameon=False,fontsize=shr_gr, loc='upper center',
              ncol=10, fancybox=True, bbox_to_anchor=(0.5, 1.20)) # Выводим легенду графика

         
    ax.set_xticks(Tiks)

    for obj in fig.findobj(matplotlib.text.Text):
        obj.set_fontproperties(arial_font)
        obj.set_fontsize(shr_gr)
                    
    
    fig.set_size_inches(17, 5,forward=True) # Изменяем размер сохраняемого графика
    fig.savefig('gr_sb/'+str(n)+'.jpg', format='jpg', dpi=100) # Cохраняем графики
