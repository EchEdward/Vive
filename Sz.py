from PIL import Image, ImageDraw, ImageFont
Razd_simv = '-'

Ar_20 = ImageFont.truetype ( 'Fonts/arial.ttf', 20 ) # Подкльчаем руский шрифт
n_x , n_y = 200 , 159 # Координаты начала линии в пикселях
k_x , k_y = 1047, 159 # Координаты конца в пикселях
Napr={'В':{'С-В':-1,'С':-1,'С-З':-1,'Ю-В':1,'Ю':1,'Ю-З':1},\
      'С-В':{'З':-1,'С':-1,'С-З':-1,'Ю-В':1,'Ю':1,'В':1},\
      'С':{'Ю-З':-1,'З':-1,'С-З':-1,'С-В':1,'В':1,'Ю-В':1},\
      'С-З':{'Ю':-1,'Ю-З':-1,'З':-1,'С':1,'С-В':1,'В':1},\
      'З':{'Ю-В':-1,'Ю':-1,'Ю-З':-1,'С-З':1,'С':1,'С-В':1},\
      'Ю-З':{'В':-1,'Ю-В':-1,'Ю':-1,'З':1,'С-З':1,'С':1},\
      'Ю':{'С-В':-1,'В':-1,'Ю-В':-1,'Ю-З':1,'З':1,'С-З':1},\
      'Ю-В':{'С':-1,'С-В':-1,'В':-1,'Ю':1,'Ю-З':1,'З':1},}

isxodnik1=([1, 'ПС Миоры fseefgrer  feefefe wefew  rtefwefwef - ПС БПС Дисна', 0, 202, 0, True, True],\
           [[1,2],[10, 76],[77, 79]], [[1,'БЗ'],[15,'БЗ'],[78,'БЗ']], 'В', [[1, 'Ю', 'ПС Труково drghdrgr drgdrgrdgd']\
                                                                            ,[123, 'Ю', 'ПС Труково1 drgdrgdr drgdrgdr']\
                                                                            ,[1, 'С', 'ПС Металургический зовод']])
isxodnik2=([1, 'отп. на ПС Труково-ПС Труково', 200, 0, 1, 0, True], [[150,100]], [], 'С', [])


# Функция для удаления опор описывающих подстанции
def DelOp(tip, n, k, spX, off_on):
    a=False
    b=False
    if off_on:
        n1,k1=n,k
        for i in range(len(spX)):
            if tip==1 and abs(n-k)>=3:
                if n==spX[i][0]:
                    a=True
                    if n<k:
                        spX[i][0]=n+1
                    elif n>k:
                        spX[i][0]=n-1
                if k==spX[i][1]:
                    b=True
                    if n<k:
                        spX[i][1]=k-1
                    elif n>k:
                        spX[i][1]=k+1
            if tip==2 and abs(n-k)>=2:
                if n==spX[i][0]:
                    a=True
                    if n<k:
                        spX[i][0]=n+1
                    elif n>k:
                        spX[i][0]=n-1
            if tip==3 and abs(n-k)>=2:
                if k==spX[i][1]:
                    b=True
                    if n<k:
                        spX[i][1]=k-1
                    elif n>k:
                        spX[i][1]=k+1

        if tip==1 and abs(n-k)>=3:
            if n<k:
                n1=n+1
            elif n>k:
                n1=n-1
            if n<k:
                k1=k-1
            elif n>k:
                k1=k+1
        if tip==2 and abs(n-k)>=2:
            if n<k:
                n1=n+1
            elif n>k:
                n1=n-1
        if tip==3 and abs(n-k)>=2:
            if n<k:
                k1=k-1
            elif n>k:
                k1=k+1
                
        return n1, k1, a, b, spX
    else:
        for i in range(len(spX)):
            if n==spX[i][0]:
                a=True
            if k==spX[i][1]:
                b=True
        return n, k, a, b, spX
    
#print(DelOp(1, 0, 202, [[0, 50],[100, 202]], True))
            
# Строку названия ПС подгоняет под ширину заданной области
def TextYm(s,r):
    s=s.strip()
    a=[]
    b=[]
    c=[]
    n=len(s)
    for i in range(n):
        if s[i]==' ':
            a.append(i)        
    for i in range(len(a)):
        m=s[:a[i]]+'\n'+s[a[i]+1:]
        b.append(m)
        for j in range(i,len(a)):
            if i!=j:
                m=s[:a[i]]+'\n'+s[a[i]+1:a[j]]+'\n'+s[a[j]+1:]
                c.append(m)
    (x,y)=draw.textsize(s, font=Ar_20)
    if x<=r:
       return s
    g=x
    for i in range(len(b)):
        (x,y)=draw.textsize(b[i], font=Ar_20)
        if x<g:
            g=x
            s=b[i]
    if g<=r:
        (x,y)=draw.textsize(s, font=Ar_20)
        return s
    for i in range(len(c)):
        try:
            (x,y)=draw.textsize(c[i], font=Ar_20)
            if x<g:
                g=x
                s=c[i]
        except Exception:
            continue
    return s
            
# Список отоброжаемых опор
def SpOp(n,k,spX,spSZ,spM,spN,re_op,spKL):
    bort=10 # Свободное место по краям элементов
    a={}
    # Опоры начала и конца линии
    if n in re_op:
        nam_op1=re_op[n]
    else:
        nam_op1=n
    if k in re_op:
        nam_op2=re_op[k]
    else:
        nam_op2=k
    (x,y)=draw.textsize(str(nam_op1), font=Ar_20)
    a[n]=[0,x/2+bort,x/2+bort,' ',' ',' ']
    (x,y)=draw.textsize(str(nam_op2), font=Ar_20)
    a[k]=[0,x/2+bort,x/2+bort,' ',' ',' ']
    # Опоры граничных участков
    for i in spX:
        if i[0] in re_op:
            nam_op1=re_op[i[0]]
        else:
            nam_op1=i[0]
        if i[1] in re_op:
            nam_op2=re_op[i[1]]
        else:
            nam_op2=i[1]
        (x,y)=draw.textsize(str(nam_op1), font=Ar_20)
        a[i[0]]=[1,x/2+bort,x/2+bort,' ',' ',' ']
        (x,y)=draw.textsize(str(nam_op2), font=Ar_20)
        a[i[1]]=[1,x/2+bort,x/2+bort,' ',' ',' ']
    # Опоры сопряжённые с КЛ
    for i in spKL:
        if i[1]=='L' or i[1]=='R':
            if i[0] in re_op:
                nam_op1=re_op[i[0]]
            else:
                nam_op1=i[0]
            (x,y)=draw.textsize(str(nam_op1), font=Ar_20)
            a[i[0]]=[9,x/2+bort,x/2+bort,' ',' ',' ']     
    # Опоры на которых только БЗ
    for i in spSZ:
        if i[0] in re_op:
            nam_op1=re_op[i[0]]
        else:
            nam_op1=i[0]
        (x,y)=draw.textsize(str(nam_op1), font=Ar_20)
        if 30<=x:
            a[i[0]]=[2,x/2+bort,x/2+bort,i[1],' ',' ']
        else:
            a[i[0]]=[2,30/2+bort,30/2+bort,i[1],' ',' ']
    # Отпайки и комбинации с зеземлителями
    for i in spN:
        if i[0] in re_op:
            nam_op1=re_op[i[0]]
        else:
            nam_op1=i[0]
        # Отпайка вниз
        if i[0] not in a and Napr[spM][i[1]]==1:
            st=TextYm(i[2],120)
            (x1,y1)=draw.textsize(st, font=Ar_20)
            (x2,y2)=draw.textsize(str(nam_op1), font=Ar_20)
            if y1>x2/2:
                a[i[0]]=[3,y1+7+bort,x2/2+bort,' ',' ',i[2]]
            else:
                a[i[0]]=[3,x2/2+7+bort,x2/2+bort,' ',' ',i[2]]
        # Отпайка вверх
        elif i[0] not in a and Napr[spM][i[1]]==-1:
            st=TextYm(i[2],120)
            (x1,y1)=draw.textsize(st, font=Ar_20)
            (x2,y2)=draw.textsize(str(nam_op1), font=Ar_20)
            if y1>x2:
                a[i[0]]=[4,y1+7+bort,bort,' ',i[2],' ']
            else:
                a[i[0]]=[4,x2+7+bort,bort,' ',i[2],' ']
        # Две отпайки и заземлители
        elif i[0] in a:
            # Отпайка вниз
            if  Napr[spM][i[1]]==1 and a[i[0]][3]==' ' and a[i[0]][4]==' ' and a[i[0]][5]==' ':
                st=TextYm(i[2],120)
                (x1,y1)=draw.textsize(st, font=Ar_20)
                (x2,y2)=draw.textsize(str(nam_op1), font=Ar_20)
                if y1>x2/2:
                    a[i[0]]=[3,y1+7+bort,x2/2+bort,' ',' ',i[2]]
                else:
                    a[i[0]]=[3,x2/2+7+bort,x2/2+bort,' ',' ',i[2]]
            # Отпайка вверх
            elif  Napr[spM][i[1]]==-1 and a[i[0]][3]==' ' and a[i[0]][4]==' ' and a[i[0]][5]==' ':
                st=TextYm(i[2],120)
                (x1,y1)=draw.textsize(st, font=Ar_20)
                (x2,y2)=draw.textsize(str(nam_op1), font=Ar_20)
                if y1>x2:
                    a[i[0]]=[4,y1+7+bort,bort,' ',i[2],' ']
                else:
                    a[i[0]]=[4,x2+7+bort,bort,' ',i[2],' ']
            # Две отпайки
            elif a[i[0]][3]==' ' and (a[i[0]][4]==' ' or a[i[0]][5]==' '):
                (x1,y1)=draw.textsize(str(nam_op1), font=Ar_20)
                (x2,y2)=draw.textsize(a[i[0]][4], font=Ar_20)
                (x3,y3)=draw.textsize(a[i[0]][5], font=Ar_20)
                st=TextYm(i[2],120)
                (x4,y4)=draw.textsize(st, font=Ar_20)
                a[i[0]][0]=5
                a[i[0]][1]=max(x1,y2,y3,y4)+bort+3
                a[i[0]][2]=y1+bort
                if a[i[0]][4]==' ':
                    a[i[0]][4]=st
                elif a[i[0]][5]==' ':
                    a[i[0]][5]=st
            
            # Отпайка и заземлитель
            elif a[i[0]][3]!=' ' and a[i[0]][4]==' ' and a[i[0]][5]==' ':
                (x1,y1)=draw.textsize(str(nam_op1), font=Ar_20)
                st=TextYm(i[2],120)
                (x2,y2)=draw.textsize(st, font=Ar_20)
                if Napr[spM][i[1]]==-1:
                    a[i[0]][0]=6
                    a[i[0]][1]=max(x1,y2,15)+bort+3
                    a[i[0]][2]=15+bort
                    a[i[0]][4]=st
                if Napr[spM][i[1]]==1:
                    a[i[0]][0]=7
                    a[i[0]][1]=max(x1,y2)+bort+3
                    a[i[0]][2]=30+5+bort
                    a[i[0]][5]=st
            # Две отпайки и заземлитель
            elif a[i[0]][3]!=' ' and (a[i[0]][4]!=' ' or a[i[0]][5]!=' '):
                (x1,y1)=draw.textsize(str(nam_op1), font=Ar_20)
                (x2,y2)=draw.textsize(a[i[0]][4], font=Ar_20)
                (x3,y3)=draw.textsize(a[i[0]][5], font=Ar_20)
                st=TextYm(i[2],120)
                (x4,y4)=draw.textsize(st, font=Ar_20)
                a[i[0]][0]=8
                a[i[0]][1]=max(x1,y2,y3,y4,15)+bort+3
                a[i[0]][2]=30+5+bort
                if a[i[0]][4]==' ':
                    a[i[0]][4]=st
                elif a[i[0]][5]==' ':
                    a[i[0]][5]=st
            
    return a

# Функция окончательного определения координат опор на схеме
def KordOp(n,k,d):
    koef = (k_x-n_x)/abs(k-n)
    a=sorted(list(d.keys()),reverse=(k<n))
    kord={}
    ysl={}
    def Prysl(a,kord,d,i,sdv1):
        ysl=[0,0,0,0]
        if n_x>(kord[a[i]]+sdv1)-d[a[i]][1]: # Левая граница
            ysl[0]=(n_x+10)-((kord[a[i]]+sdv1)-d[a[i]][1])
        if k_x<(kord[a[i]]+sdv1)+d[a[i]][2]: # Правая граница
            ysl[1]=(k_x-10)-((kord[a[i]]+sdv1)+d[a[i]][2])
        if i!=0:
            if kord[a[i-1]]+d[a[i-1]][2]>(kord[a[i]]+sdv1)-d[a[i]][1]: # Пересечение с опорой слева
                ysl[2]=(kord[a[i-1]]+d[a[i-1]][2])-((kord[a[i]]+sdv1)-d[a[i]][1])
        if i!=len(a)-1:
            if kord[a[i+1]]-d[a[i+1]][1]<(kord[a[i]]+sdv1)+d[a[i]][2]: # Пересечение с опорой спарава
                ysl[3]=(kord[a[i+1]]-d[a[i+1]][1])-((kord[a[i]]+sdv1)+d[a[i]][2])
        return ysl
    for i in a:
        kord[i]=int(n_x+abs(i-n)*koef)
    for j in range(200):
        for i in range(len(a)):
            ysl[a[i]]=Prysl(a,kord,d,i,0)
        ke=True
        #print(kord)
        #print(ysl)
        #print('---------')
        for i in range(len(a)):
            if not (ysl[a[i]][0]==0 and ysl[a[i]][1]==0 and ysl[a[i]][2]==0 and ysl[a[i]][3]==0):
                ke=False
                break
        if ke:
            return kord
        blok=len(a)
        for i in range(len(a)):
            if ((ysl[a[i]][0]!=0 and ysl[a[i]][1]==0 and ysl[a[i]][2]==0 and ysl[a[i]][3]==0) or\
               (ysl[a[i]][0]==0 and ysl[a[i]][1]!=0 and ysl[a[i]][2]==0 and ysl[a[i]][3]==0) or\
               (ysl[a[i]][0]==0 and ysl[a[i]][1]==0 and ysl[a[i]][2]!=0 and ysl[a[i]][3]==0) or\
               (ysl[a[i]][0]==0 and ysl[a[i]][1]==0 and ysl[a[i]][2]==0 and ysl[a[i]][3]!=0)) and i !=blok:
                sdv=max(ysl[a[i]])+min(ysl[a[i]])
                dv = 1 if sdv>0 else -1
                sdv+=dv
                if dv==1 and i!=len(a)-1:
                    if kord[a[i+1]]-(kord[a[i]]+sdv)>kord[a[i+1]]-kord[a[i]]:
                        sdv=kord[a[i+1]]-kord[a[i]]
                if dv==-1 and i!=0:
                    if kord[a[i-1]]-(kord[a[i]]+sdv)<kord[a[i-1]]-(kord[a[i]]+sdv):
                        sdv=kord[a[i-1]]-kord[a[i]]
                kord[a[i]]+=sdv-dv
                blok=i
            else:
                if ((ysl[a[i]][2]!=0 and ysl[a[i]][3]==0) or\
                   (ysl[a[i]][2]==0 and ysl[a[i]][3]!=0)) and i !=blok:
                    sdv=max(ysl[a[i]])+min(ysl[a[i]])
                    dv = 1 if sdv>0 else -1
                    sdv+=dv
                    if dv==1 and i!=len(a)-1:
                        if kord[a[i+1]]-(kord[a[i]]+sdv)>kord[a[i+1]]-kord[a[i]]:
                            sdv=kord[a[i+1]]-kord[a[i]]
                    if dv==-1 and i!=0:
                        if kord[a[i-1]]-(kord[a[i]]+sdv)<kord[a[i-1]]-(kord[a[i]]+sdv):
                            sdv=kord[a[i-1]]-kord[a[i]]
                    kord[a[i]]+=sdv-dv
                    blok=i
            
    return kord

    

# Функция прорисовки текста отличного от 0 грудусов
def TextRor(kord,st,rot,ogr,t):
    (x1,y1)=kord
    st=TextYm(st,ogr)
    (x,y)=draw.textsize(st, font=Ar_20)
    im = Image.new('RGB',(x,y), 'white')
    dr = ImageDraw.Draw(im) 
    dr.text((0,0), st, fill="black", font=Ar_20)
    if rot==90:
        im=im.transpose(Image.ROTATE_90)
    elif rot==180:
        im=im.transpose(Image.ROTATE_180)
    elif rot==270:
        im=im.transpose(Image.ROTATE_270)
    w,h=im.size
    if t==1:
        image.paste(im, (int(x1),int(y1),int(x1+w),int(y1+h)))
    elif t==2:
        image.paste(im, (int(x1),int(y1-h),int(x1+w),int(y1)))
    elif t==3:
        image.paste(im, (int(x1-w),int(y1-h),int(x1),int(y1)))
    elif t==4:
        image.paste(im, (int(x1-w),int(y1),int(x1),int(y1+h)))
    return w,h

def Point(sp,k):
    x, y = sp
    return (x-k,y-k,x+k,y+k)
            
# Подписи подстанций
def PS(s,n):
    s1,s2 =s.split(Razd_simv,1)
    s1=s1.strip()
    s2=s2.strip()
    if n != 3 and n != 4:
        s1=TextYm(s1,180)
        (x,y)=draw.textsize(s1, font=Ar_20)
        draw.text((110-x/2,107-y), s1, fill="black", font=Ar_20)
    if n != 2 and n != 4: 
        s2=TextYm(s2,180)
        (x,y)=draw.textsize(s2, font=Ar_20)
        draw.text((1132-x/2,107-y), s2, fill="black", font=Ar_20)
    
# Заземление ПС1
def PZ1(vkl):
    draw.text((199-12,245), 'ПЗ', fill="black", font=Ar_20)
    if vkl:
        draw.line((199, 215, 199, 196), fill="black", width=3) # ПЗ-1 включено
    else:
        draw.line((199, 215, 188, 199), fill="black", width=3) # ПЗ-1 выключено
# Заземление ПС2
def PZ2(vkl):
    draw.text((1047-12,245), 'ПЗ', fill="black", font=Ar_20)
    if vkl:
        draw.line((1047, 215, 1047, 196), fill="black", width=3) # ПЗ-1 включено
    else:
        draw.line((1047, 215, 1036, 199), fill="black", width=3) # ПЗ-1 выключено

def mashtab(kord,spX):
    len_point = n_x
    j=n_x
    for i in range(len(spX)):
        n1 = int(kord[spX[i][0]])
        n2 = int(kord[spX[i][1]])
        draw.line((len_point, 159, n1, 159), fill="black", width=3)

        if n1 == n2:
            draw.line((n1-4, 155, n1+4, 163), fill="black", width=3)
            draw.line((n1+4, 155, n1-4, 163), fill="black", width=3)
            j=n2
        else:
            k=0
            for j in range(n1,n2+1):
                k +=1
                if k == 20 or (k == 20 and j == n2) or (k != 20 and j == n2) or j == n1:
                    k = 0
                    draw.line((j-4, 155, j+4, 163), fill="black", width=3)
                    draw.line((j+4, 155, j-4, 163), fill="black", width=3)

        len_point = n2
    draw.line((j, 159, k_x, 159), fill="black", width=3)

def SZ(n,tip,st):
    if tip==2 or tip==6:
        draw.line((n, 159, n, 195), fill="black", width=3)
        draw.line((n-15, 195, n+15, 195), fill="black", width=3)
        draw.line((n-10, 200, n+10, 200), fill="black", width=3)
        draw.line((n-5, 205, n+5, 205), fill="black", width=3)
        draw.text((n-11,207), st, fill="black", font=Ar_20)
    if tip==7 or tip==8:
        n1=n
        n+=19
        draw.line((n1, 159, n, 175), fill="black", width=3)
        draw.line((n, 175, n, 195), fill="black", width=3)
        draw.line((n-15, 195, n+15, 195), fill="black", width=3)
        draw.line((n-10, 200, n+10, 200), fill="black", width=3)
        draw.line((n-5, 205, n+5, 205), fill="black", width=3)
        draw.text((n-11,207), st, fill="black", font=Ar_20)

def DZ(n,t1,t2,k):

    if t2 == True and t1 == False and (k==1 or k==2 or k==3):

        if n==1 and (k==1 or k==2):
            draw.line((126, 159, 126, 230), fill="black", width=3)
            draw.line((126-15, 230, 126+15, 230), fill="black", width=3)
            draw.line((126-10, 235, 126+10, 235), fill="black", width=3)
            draw.line((126-5, 240, 126+5, 240), fill="black", width=3)
        elif n==2 and (k==1  or k==3):
            draw.line((1118, 159, 1118, 230), fill="black", width=3)
            draw.line((1118-15, 230, 1118+15, 230), fill="black", width=3)
            draw.line((1118-10, 235, 1118+10, 235), fill="black", width=3)
            draw.line((1118-5, 240, 1118+5, 240), fill="black", width=3)
            


def Otpaika(tip,n1):
    yn=259
    yv=59
    if tip==3 or tip==7:
        draw.line((n1, 159, n1, yn), fill="black", width=3)
        draw.line((n1, yn, n1-3, yn-6), fill="black", width=3)
        draw.line((n1, yn, n1+3, yn-6), fill="black", width=3)
    elif tip==4 or tip==6:
        draw.line((n1, 159, n1, yv), fill="black", width=3)
        draw.line((n1, yv, n1-3, yv+6), fill="black", width=3)
        draw.line((n1, yv, n1+3, yv+6), fill="black", width=3)
    elif tip==5 or tip==8:
        draw.line((n1, 159, n1, yn), fill="black", width=3)
        draw.line((n1, yn, n1-3, yn-6), fill="black", width=3)
        draw.line((n1, yn, n1+3, yn-6), fill="black", width=3)
        draw.line((n1, 159, n1, yv), fill="black", width=3)
        draw.line((n1, yv, n1-3, yv+6), fill="black", width=3)
        draw.line((n1, yv, n1+3, yv+6), fill="black", width=3)

def PSZp(tip,ysl,n,pz,a):
    if tip==1 and (n==1 or n==2) and (a==True or (ysl==True and pz==False)):
        draw.line((170, 152, 184, 167), fill="black", width=3)
        draw.line((184, 152, 170, 167), fill="black", width=3)
    if tip==2 and (n==1 or n==3) and (a==True or (ysl==True and pz==False)):
        draw.line((1061, 152, 1075, 167), fill="black", width=3)
        draw.line((1075, 152, 1061, 167), fill="black", width=3)

#
def OtkPit(sp_pit):
    for i in range(len(sp_pit)):
        nam = TextYm(sp_pit[i][2],170)
        (x,y)=draw.textsize(nam, font=Ar_20)
        if sp_pit[i][1] == -1 and sp_pit[i][3] == -1:
            draw.line((199, 159, 199, 180), fill="black", width=3)
            draw.line((199, 180, 192, 173), fill="black", width=3)
            draw.line((199, 180, 206, 173), fill="black", width=3)
            draw.text((int(171-x),int(218)), nam, fill="black", font=Ar_20)
        elif sp_pit[i][1] == -1 and sp_pit[i][3] == 0:
            draw.line((199, 159, 178, 159), fill="black", width=3)
            draw.line((178, 159, 185, 152), fill="black", width=3)
            draw.line((178, 159, 185, 166), fill="black", width=3)
            draw.text((int(171-x),int(159-y/2)), nam, fill="black", font=Ar_20)
        elif sp_pit[i][1] == -1 and sp_pit[i][3] == 1:
            draw.line((199, 159, 199, 138), fill="black", width=3)
            draw.line((199, 138, 192, 145), fill="black", width=3)
            draw.line((199, 138, 206, 145), fill="black", width=3)
            draw.text((int(171-x),int(100-y)), nam, fill="black", font=Ar_20)
        elif sp_pit[i][1] == 1 and sp_pit[i][3] == -1:
            draw.line((1047, 159, 1047, 180), fill="black", width=3)
            draw.line((1047, 180, 1040, 173), fill="black", width=3)
            draw.line((1047, 180, 1054, 173), fill="black", width=3)
            draw.text((int(1075),int(218)), nam, fill="black", font=Ar_20)
        elif sp_pit[i][1] == 1 and sp_pit[i][3] == 0:
            draw.line((1047, 159, 1068, 159), fill="black", width=3)
            draw.line((1068, 159, 1061, 152), fill="black", width=3)
            draw.line((1068, 159, 1061, 166), fill="black", width=3)
            draw.text((int(1075),int(159-y/2)), nam, fill="black", font=Ar_20)
        elif sp_pit[i][1] == 1 and sp_pit[i][3] == 1:
            draw.line((1047, 159, 1047, 138), fill="black", width=3)
            draw.line((1047, 138, 1040, 145), fill="black", width=3)
            draw.line((1047, 138, 1054, 145), fill="black", width=3)
            draw.text((int(1075),int(100-y)), nam, fill="black", font=Ar_20)
            



def Sxeme(name,spX,spSZ,spM,spN,off_on,zapr,dz,re_op,sp_pit,spKL,rzapr=(False,False,False)):

    
    

    global draw, koef, text, image
    text = {}
    if name[0] == 1:
        image = Image.open('template_scheme/scheme1.jpeg') # Открываем картинку шаблона
        draw = ImageDraw.Draw(image) # Создаём обьект картинки, которую вдальнейшем можем редактировать   
        PZ1(name[5]) # Вкл/выкл ПЗ1
        PZ2(name[6]) # Вкл/выкл ПЗ2
        #if off_on:
            #draw.text((164,167), 'ЛП', fill="black", font=Ar_20)
            #draw.text((1057,167), 'ЛП', fill="black", font=Ar_20)
    if name[0] == 2:
        image = Image.open('template_scheme/scheme2.jpeg') # Открываем картинку шаблона
        draw = ImageDraw.Draw(image) # Создаём обьект картинки, которую вдальнейшем можем редактировать   
        PZ1(name[5]) # Вкл/выкл ПЗ1
        #if off_on:
            #draw.text((164,167), 'ЛП', fill="black", font=Ar_20)
    if name[0] == 3:
        image = Image.open('template_scheme/scheme3.jpeg') # Открываем картинку шаблона
        draw = ImageDraw.Draw(image) # Создаём обьект картинки, которую вдальнейшем можем редактировать   
        PZ2(name[6]) # Вкл/выкл ПЗ2
        #if off_on:
            #draw.text((1057,167), 'ЛП', fill="black", font=Ar_20)
    if name[0] == 4:
        image = Image.open('template_scheme/scheme4.jpeg') # Открываем картинку шаблона
        draw = ImageDraw.Draw(image) # Создаём обьект картинки, которую вдальнейшем можем редактировать
    #print(1)    
    PS(name[1],name[0]) # подписи ПС
    #print(2)
    n, k, a, b, spX=DelOp(name[0], name[2], name[3], spX, off_on) # Обрезаем если нужно опоры ПС
    #print(3)
    spis_op=SpOp(n,k,spX,spSZ,spM,spN,re_op,spKL) # Формируем список опор, которые будут отображаться
    #print(4)
    kord=KordOp(n,k,spis_op)
    #print(5)
    f=list(kord.keys())
    for i in range(len(f)):
        if f[i] in re_op:
            nam_op=re_op[f[i]]
        else:
            nam_op=str(f[i])
        #draw.line((kord[f[i]], 159, kord[f[i]], 165), fill="black", width=3)
        #draw.line((kord[f[i]], 159, kord[f[i]], 154), fill="black", width=3)
        #draw.line((kord[f[i]]-spis_op[f[i]][1], 159, kord[f[i]]-spis_op[f[i]][1], 165), fill="green", width=3)
        #draw.line((kord[f[i]]+spis_op[f[i]][2], 159, kord[f[i]]+spis_op[f[i]][2], 154), fill="red", width=3)
        if spis_op[f[i]][0]==0:
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
        elif spis_op[f[i]][0]==1:
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
        if spis_op[f[i]][0]==2:
            SZ(kord[f[i]],2,spis_op[f[i]][3])
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
        if spis_op[f[i]][0]==3:
            Otpaika(3,kord[f[i]])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
            TextRor((kord[f[i]]-7,159+7),spis_op[f[i]][5],90,120,4)
        if spis_op[f[i]][0]==4:
            Otpaika(4,kord[f[i]])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x-5,164), str(nam_op), fill="black", font=Ar_20)
            TextRor((kord[f[i]]-7,152),spis_op[f[i]][4],90,120,3)
        if spis_op[f[i]][0]==5:
            Otpaika(5,kord[f[i]])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            TextRor((kord[f[i]]-7,152),spis_op[f[i]][4],90,120,3)
            TextRor((kord[f[i]]-7,159+7),spis_op[f[i]][5],90,120,4)
            TextRor((kord[f[i]]+2,156),str(nam_op),90,120,2)
        if spis_op[f[i]][0]==6:
            Otpaika(6,kord[f[i]])
            SZ(kord[f[i]],6,spis_op[f[i]][3])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            TextRor((kord[f[i]]-7,152),spis_op[f[i]][4],90,120,3)
            TextRor((kord[f[i]]+2,156),str(nam_op),90,120,2)
        if spis_op[f[i]][0]==7:
            Otpaika(7,kord[f[i]])
            SZ(kord[f[i]],7,spis_op[f[i]][3])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            (x,y)=draw.textsize(str(nam_op), font=Ar_20)
            draw.text((kord[f[i]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
            TextRor((kord[f[i]]-7,159+7),spis_op[f[i]][5],90,120,4)
        if spis_op[f[i]][0]==8:
            Otpaika(8,kord[f[i]])
            SZ(kord[f[i]],8,spis_op[f[i]][3])
            draw.ellipse(Point((kord[f[i]],159),3), fill="black", outline="black")
            TextRor((kord[f[i]]-7,152),spis_op[f[i]][4],90,120,3)
            TextRor((kord[f[i]]-7,159+7),spis_op[f[i]][5],90,120,4)
            TextRor((kord[f[i]]+2,156),str(nam_op),90,120,2)
        #print(6)    
        mashtab(kord,spX)
        #print(7)
        if name[0] == 1 or name[0] == 2:
            draw.ellipse(Point((kord[n],159),3), fill="black", outline="black")
        if name[0] == 1 or name[0] == 3:
            draw.ellipse(Point((kord[k],159),3), fill="black", outline="black")
    trngl = 5
    for i in range(len(spKL)):
        if spKL[i][0] in kord and (spKL[i][1]=='L' or spKL[i][1]=='R'):
            if spKL[i][0] in re_op:
                nam_op=re_op[spKL[i][0]]
            else:
                nam_op=str(spKL[i][0])
            if spis_op[spKL[i][0]][0] == 9:
                (x,y)=draw.textsize(str(nam_op), font=Ar_20)
                draw.text((kord[spKL[i][0]]-x/2,125), str(nam_op), fill="black", font=Ar_20)
            if spKL[i][1]=='L':
                xy = [kord[spKL[i][0]],159-trngl*2,kord[spKL[i][0]]+trngl*2,159,kord[spKL[i][0]],159+trngl*2,kord[spKL[i][0]],159-trngl*2]
                draw.polygon(xy, fill="black", outline="black")
            elif spKL[i][1]=='R':
                xy = [kord[spKL[i][0]],159-trngl*2,kord[spKL[i][0]]-trngl*2,159,kord[spKL[i][0]],159+trngl*2,kord[spKL[i][0]],159-trngl*2]
                draw.polygon(xy, fill="black", outline="black")
            

            
    if not rzapr[0]:
        #Запрет ПС
        PSZp(1,zapr,name[0],name[5],a)
    else:
        PSZp(1,False,name[0],name[5],rzapr[1])
    if not rzapr[2]:
        #Запрет ПС
        PSZp(2,zapr,name[0],name[6],b)
    else:
        PSZp(2,False,name[0],name[6],rzapr[3])
        

       
    # Уствановка ДЗ
    DZ(1,name[5],dz,name[0])
    DZ(2,name[6],dz,name[0])
    OtkPit(sp_pit)
            
            
                

        #print(spis_op)
        #print(TextRor((620,160),"black re erye eryey eryyy",90,120,2))
   
    del draw # Удаляем обьект картинки
    #image.save('result_schemes/'+str(name[4])+".jpeg", "JPEG") # сохраняем картинку в новом файле
    image.crop((0,20,1247,315)).save('result_schemes/'+str(name[4])+".jpg")


#Sxeme(isxodnik1[0],isxodnik1[1],isxodnik1[2],isxodnik1[3],isxodnik1[4])
