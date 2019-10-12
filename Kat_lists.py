import openpyxl
import numpy as np
import rnn
import copy
# Создаёма словарь для обращения к ячеке таблицы Excel
Alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Katalog = rnn.ExDict()

# Создаём словарь для опоры по ширине
XHkat = { 'ABC': 1, 'ACB': 2, 'BCA': 3, 'BAC': 4, 'CAB': 5, 'CBA': 6,
          '-ABC': -1, '-ACB': -2, '-BCA': -3, '-BAC': -4, '-CAB': -5, '-CBA': -6}
        
Razd_simv = '-'

# Открываем каталог с данными по опорам и проводникам
Katal = openpyxl.load_workbook(filename = 'Katal.xlsx')
# выбирем необходимый рабочий лист
Kat = Katal['Kat']
# Создаём словарь для работы с фазировкой
def Sl_Faza():
    a=XHkat
    return a
# Список возможной фазировки
def Faza():
    a=list(Sl_Faza().keys())
    return a
# Словарь для работы с Типами опор
def Sl_TipOp():
    a={}
    i=0
    for key in Katalog.keys():
        if Kat[Katalog.get(key)+str(1)].value == None:
            break
        i +=1
        a.setdefault(Kat[Katalog.get(key)+str(1)].value, i)
    return a
def OpPisitionTip():
    a = Sl_TipOp()
    b = {}
    for key in a:
        b[key] = Kat[Katalog.get(a[key])+str(14)].value
    return b
op_position = OpPisitionTip()
# Список Типов опор
def TipOp():
    a=list(Sl_TipOp().keys())
    return a


# Словарь для работы с Марками проводов и тросов
def Sl_Marka():
    a={}
    i=0
    a.setdefault('Не выбран', i)
    for key in Katalog.keys():
        if Kat[Katalog.get(key)+str(17)].value == None:
            break
        i +=1
        a.setdefault(Kat[Katalog.get(key)+str(17)].value, i)
    return a
# Список Марок проводов и тросов
def Marka():
    a=list(Sl_Marka().keys())
    return a
# Пустой список для Выпадающих списков
def PystoiSpisok():
    m=[]
    for i in range(200):
        a=[]
        for j in range(7):
            a.append('')
        m.append(a)
    return m

# Преобразовываем Таблицу ИВЛ к удобному виду и ищем ошибки
def Sort_IVL(ivl1):
    ivl = copy.deepcopy(ivl1)
    
    s_ivl=[]
    s_nm_ivl=[] # Список названий отпаек
    yr_v=[] # Список уровней ветвей
    ivl_gr=[]
    b=0
    # Создаём словарь для дальнейшего преобразования номеров опор
    Ych_ivl = []
    ivl_dict = {}
    KL = []
    kl_len = -1
    for i in ivl:
        if i[0] != 'Конфигурация опоры':
            yr_v.append(i[4])
            k=(int(i[2]),int(i[3]))
            a=[]
            Ych_ivl.append([int(i[2]),int(i[3])])

            KL.append([])
            kl_len+=1

        else:
            sk1 = None
            sk2 = None
            sk3 = None
            sk4 = None
            sk5 = None
            sk6 = None
            for j in range(len(i[2])):
                if i[2][j] == "(":
                    sk1=j
                if i[2][j] == ")":
                    sk2=j
                if i[2][j] == ":":
                    sk5=j
            for j in range(len(i[3])):
                if i[3][j] == "(":
                    sk3=j
                if i[3][j] == ")":
                    sk4=j
                if i[3][j] == ":":
                    sk6=j

            if sk1 != None and sk2 != None:
                if sk5 != None:
                    n1 = i[2][sk1+1:sk5].lower()=="kl" or i[2][sk1+1:sk5].lower()=="кл"     
                    n2 = int(i[2][sk2+1:])
                    n3 = i[2][sk5+1:sk2]
                else:
                    n1 = False    
                    n2 = int(i[2][sk2+1:])
                    n3 = i[2][sk1+1:sk2]
                i[2] = str(n2)     
            else:
                n1 = False
                n2 = int(i[2])
                n3 = ''
                
            if sk3 != None and sk4 != None:
                if sk5 != None:
                    k1 = i[3][sk3+1:sk6].lower()=="kl" or i[3][sk3+1:sk6].lower()=="кл"
                    k2 = int(i[3][sk4+1:])
                    k3 = i[3][sk6+1:sk4]
                else:
                    k1 = False
                    k2 = int(i[3][sk4+1:])
                    k3 = i[3][sk3+1:sk4]
                i[3] = str(k2)
            else:
                k1 = False
                k2 = int(i[3])
                k3 = ''
            
            Ych_ivl.append([n2,k2,n1,k1])
            a.append([n2,k2])
            ivl_dict[k]=a

            KL[kl_len].append([n2,k2,n1,k1,n3,k3])

    l, s_km = Dlina(ivl,yr_v) # длинна участвков
    # Создаём словарь сопостовления опор       
    kop = 1
    yz = {}
    per = {}
    k=(list(ivl_dict.keys()))[0]
    for key in ivl_dict:
        a = {}
        if key[0] not in yz:
            yz[key[0]] = kop
        for i in ivl_dict[key]:
            if i[0] < i[1]:
                if k == key:
                    a[i[0]]=kop
                else:
                    a[i[0]]=yz[key[0]]
                    k=key
                for j in range(i[0]+1,i[1]+1):
                    kop += 1
                    a[j]=kop
            if i[0] > i[1]:
                if k == key:
                    a[i[0]]=kop
                else:
                    a[i[0]]=yz[key[0]]
                    k=key
                for j in range(-(i[0])+1,-(i[1])+1):
                    kop += 1
                    a[-j]=kop
        if key[1] not in yz:
            yz[key[1]] = kop
        per[key]=a

    gg=[]
    g=0
    for i in range(len(l)):
        g += l[i] 
        if l[i] == 0 and i !=0:
            gg.append(g)
            g=0
    gg.append(g)
    zz=0

    
    # Отправляем данные в расчет   
    for i in range(len(ivl)):
        a=[]
        if ivl[i][0] != 'Конфигурация опоры':
            s_nm_ivl.append(ivl[i][0])
            a.append(1)
            a.append(0)
            n=Ych_ivl[i][0]
            k=Ych_ivl[i][1]
            g=list(per[(n,k)].keys())
            a.append(yz[Ych_ivl[i][0]])
            a.append(yz[Ych_ivl[i][1]])
            ivl_gr.append([n,k,gg[zz],ivl[i][1],g[0],g[len(g)-1],ivl[i][0]])
            zz +=1
            for j in range(4,10):
                a.append(0)
        else:
            a.append(0)
            a.append(l[i])
            a.append(per[(n,k)][Ych_ivl[i][0]])
            a.append(per[(n,k)][Ych_ivl[i][1]])
            a.append(0)
            a.append(Sl_Faza().get(ivl[i][4]))
            a.append(Sl_TipOp().get(ivl[i][5]))
            a.append(Sl_Marka().get(ivl[i][6]))
            a.append(Sl_Marka().get(ivl[i][7]))
            a.append(Sl_Marka().get(ivl[i][8]))
        s_ivl.append(a)
    
    
    
    
    return s_ivl, s_nm_ivl, s_km, per, yz, ivl_gr, yr_v, KL
# Преобразовываем Таблицу ВВЛ к удобному виду и ищем ошибки
def Sort_VVL(vvl,per,yz):
    s_vvl=[]
    oid_vvl=[]
    for i in range(len(vvl)):
        a=[]
        if vvl[i][0] != 'Конфигурация опоры':
            a.append(float(Tochka(vvl[i][3])))
            a.append(0)
            n=int(vvl[i][1])
            k=int(vvl[i][2])
            a.append(0)
            a.append(0)
            b1=0
            c1=[]
            for j in range(len(vvl[i][4])):
                if vvl[i][4][j] == ';':
                    c1.append(j)
                    b1=1
            c2=[]
            for j in range(len(vvl[i][5])):
                if vvl[i][5][j] == ';':
                    c2.append(j)
                    b1=1
                    
            if len(c1)==0:
                P1=P2=P3=float(Tochka(vvl[i][4]))
            elif len(c1)==1:
                P1=float(Tochka(vvl[i][4][:c1[0]]))
                P2=P3=float(Tochka(vvl[i][4][c1[0]+1:]))
            elif len(c1)==2:
                P1=float(Tochka(vvl[i][4][:c1[0]]))
                P2=float(Tochka(vvl[i][4][c1[0]+1:c1[1]]))
                P3=float(Tochka(vvl[i][4][c1[1]+1:]))
                
            if len(c2)==0:
                Q1=Q2=Q3=float(Tochka(vvl[i][5]))
            elif len(c2)==1:
                Q1=float(Tochka(vvl[i][5][:c2[0]]))
                Q2=Q3=float(Tochka(vvl[i][5][c2[0]+1:]))
            elif len(c2)==2:
                Q1=float(Tochka(vvl[i][5][:c2[0]]))
                Q2=float(Tochka(vvl[i][5][c2[0]+1:c2[1]]))
                Q3=float(Tochka(vvl[i][5][c2[1]+1:]))
                
            a.append(P1)
            a.append(Q1)
            a.append(float(Tochka(vvl[i][6])))
            a.append(P2)
            a.append(P3)
            a.append(Q2)
            a.append(Q3)
            a.append(b1)
        else:
            
            sk1 = None
            sk2 = None
            sk3 = None
            sk4 = None
            for j in range(len(vvl[i][1])):
                if vvl[i][1][j] == "(":
                    sk1=j
                if vvl[i][1][j] == ")":
                    sk2=j
            for j in range(len(vvl[i][2])):
                if vvl[i][2][j] == "(":
                    sk3=j
                if vvl[i][2][j] == ")":
                    sk4=j

            razv = 1
            if sk1 != None and sk2 != None and sk3 != None and sk4 != None:
                n1 = int(vvl[i][1][sk1+1:sk2])
                k1 = int(vvl[i][2][sk3+1:sk4])
                n2 = int(vvl[i][1][sk2+1:])
                k2 = int(vvl[i][2][sk4+1:])
                if n1<=0:
                    razv = -1
                elif k1<=0:
                    razv = -1
                else:
                    razv = 1
                n1 = abs(n1)
                k1 = abs(k1)
            else:
                n1 = n
                k1 = k
                n2 = int(vvl[i][1])
                k2 = int(vvl[i][2])

            a.append(0)
            a.append(n1)
            
            a.append(per[(n1,k1)][n2])
            a.append(per[(n1,k1)][k2])

            b=False
            for j in range(len(vvl[i][3])):
                if vvl[i][3][j] == ';':
                    c = j
                    b = True
            if b:
                f1=float(Tochka(vvl[i][3][:c]))
                f2=float(Tochka(vvl[i][3][c+1:]))
            else:
                f1 = f2 = float(Tochka(vvl[i][3]))
            a.append(f1)
            a.append(Sl_Faza().get(vvl[i][4]))
            a.append(Sl_TipOp().get(vvl[i][5]))
            a.append(Sl_Marka().get(vvl[i][6]))
            a.append(Sl_Marka().get(vvl[i][7]))
            a.append(Sl_Marka().get(vvl[i][8]))
            a.append(f2)
            a.append(razv)
        s_vvl.append(a)
    return s_vvl
# Преобразовываем Таблицу Заземление в точке к удобному виду и ищем ошибки
def Sort_Zy(zy,per,yz):
    abc = {'A':1, 'B':2, 'C':3}
    F = {'3ф с тр.':1, '3ф без тр.':2, '2ф с тр':3, '2ф без тр':4, '1ф с тр':5, '1ф без тр':6, 'Разземлен':7}
    s_zy=[]
    for i in range(len(zy)):
        a=[]
        a.append(per[(int(zy[i][0]),int(zy[i][1]))][int(zy[i][2])])
        a.append(float(Tochka(zy[i][3])))
        a.append(F.get(zy[i][4]))
        a.append(abc.get(zy[i][5]))
        a.append(abc.get(zy[i][6]))
        s_zy.append(a)
    return s_zy
# Преобразовываем Таблицу Заземление тросов ИВЛ к удобному виду и ищем ошибки

def Sort_Zytr(zytr,per,yz):
    s_zytr=[]
    for i in range(len(zytr)):
        a=[]
        a.append(per[(int(zytr[i][0]),int(zytr[i][1]))][int(zytr[i][2])])
        a.append(per[(int(zytr[i][0]),int(zytr[i][1]))][int(zytr[i][3])])
        a.append(float(Tochka(zytr[i][4])))
        s_zytr.append(a)
    return s_zytr
# Преобразовываем Таблицу Заземление троссов ВВЛ к удобному виду и ищем ошибки
def Sort_Zvl(zvl):
    s_zvl=[]
    for i in range(len(zvl)):
        a=[]
        a.append(float(Tochka(zvl[i][0])))
        a.append(float(Tochka(zvl[i][1])))
        a.append(int(zvl[i][2]))
        a.append(float(Tochka(zvl[i][3])))
        a.append(int(zvl[i][4]))
        a.append(Sl_Faza().get(zvl[i][5]))
        a.append(Sl_TipOp().get(zvl[i][6]))
        a.append(Sl_Marka().get(zvl[i][7]))
        a.append(Sl_Marka().get(zvl[i][8]))
        s_zvl.append(a)
    return s_zvl
def adres(s):
    for i in range(-len(s),1):
        if s[-i-1] == '/':
            s = s[:-i]
            break         
    return s

# Словарь (Опора:км)
def Skm(n,k,no,ko):
    no=int(no)
    ko=int(ko)
    km = {}
    dL=(k-n)/abs(ko-no)
    km[no]=n
    if ko > no:
        for i in range(no+1,ko+1):
            n += dL
            km[i]=n
    elif ko < no:
        for i in range(-no+1,-ko+1):
            n += dL
            km[-i]=n
    return km

# Длины учасков, список для графиков
def Dlina(ivl,yr_v):
    Level = True
    for i in range(len(yr_v)):
        if yr_v[i] == "Нет":
            Level = False
            break
    #print(Level)
    l=[]
    km=[]
    dd = {}
    on_l = (False,)

    for i in range(len(ivl)):
        if ivl[i][0] != 'Конфигурация опоры':
            one = True
            n=0
            k=0
            l.append(0)
            if i != 0:
                ms = list(a.values())
                ld = len(ms)-1
                km.append(ms)
                dd[(x,y)]=[ms[ld], ms[ld]>ms[ld-1],ivl[i][4]]
            x=ivl[i][2]
            y=ivl[i][3]
            for key in dd:
                if key[1] == x and ivl[i][4] == dd[key][2] and Level:
                    on_l = (True,dd[key][1],dd[key][0])
                else:
                    on_l = (False,)
            a={}
        else:
            b=False
            # Определяем есть ли знак диапазона
            for j in range(len(ivl[i][1])):
                if ivl[i][1][j] == ';':
                    c = j
                    b = True
            # Записываем число (числа)
            if b:
                f1=float(Tochka(ivl[i][1][:c]))
                f2=float(Tochka(ivl[i][1][c+1:]))
            else:
                f1 = f2 = float(Tochka(ivl[i][1]))
            # Сравниваем числа
            if f1 == f2:
                if one:
                    if on_l[0]:
                        n=on_l[2]
                        if on_l[1]:
                            k = n+f2
                        else:
                            k = n-f2
                    else:
                        n=0
                        k=f1
                    l.append(f1)
                    a.update(Skm(n,k,ivl[i][2],ivl[i][3]))
                    one = False
                else:
                    if n > k:
                        a.update(Skm(k,k-f1,ivl[i][2],ivl[i][3]))
                        k -=f1
                        l.append(f1)
                    elif n < k:
                        a.update(Skm(k,k+f1,ivl[i][2],ivl[i][3]))
                        k +=f1
                        l.append(f1)
            elif f1 > f2:
                if one:
                    n=f1
                    k=f2
                    l.append(f1-f2)
                    a.update(Skm(f1,f2,ivl[i][2],ivl[i][3]))
                    one = False
                else:
                    if f1 == k:
                        k = f2
                        l.append(f1-f2)
                        a.update(Skm(f1,f2,ivl[i][2],ivl[i][3]))
                    else:
                        l.append(0)
            elif f1 < f2:
                if one:
                    n=f1
                    k=f2
                    l.append(f2-f1)
                    a.update(Skm(f1,f2,ivl[i][2],ivl[i][3]))
                    one = False
                else:
                    if f1 == k:
                        k = f2
                        l.append(f2-f1)
                        a.update(Skm(f1,f2,ivl[i][2],ivl[i][3]))
                    else:
                        l.append(0)
    km.append(list(a.values()))
    return l, km
# Определяем запрещённые и разрешённые участки
def Zapret(FiA, FiB, FiC,FiT1,p,sr_vel,FACh,FBCh,FCCh,FTRCh):#,lbsz,inf
    f=[]
    f2=[]
    for i in range(len(FiA)):
        c=[]
        a=0
        b={}
        for j in [0, len(FiA[i])-1]:
            m1 = max(FiA[i][j]*int(FACh),FiB[i][j]*int(FBCh),FiC[i][j]*int(FCCh),FiT1[i][j]*int(FTRCh))
            if m1 <= sr_vel:
                b[p[i][j]]=False
            elif m1 > sr_vel:
                b[p[i][j]]=True
                
        for j in range(len(FiA[i])): 
            if j != a:
                continue
            m1 = max(FiA[i][j]*int(FACh),FiB[i][j]*int(FBCh),FiC[i][j]*int(FCCh),FiT1[i][j]*int(FTRCh))
            if m1 > sr_vel:
                for k in range(j,len(FiA[i])):
                    m2 = max(FiA[i][k]*int(FACh),FiB[i][k]*int(FBCh),FiC[i][k]*int(FCCh),FiT1[i][k]*int(FTRCh))
                    if m2 <= sr_vel:
                        z=k
                        if j != 0:
                            j -= 1
                        break
                    elif m2 > sr_vel and k == len(FiA[i])-1:
                        z=k
                        if j != 0:
                            j -= 1
                        break
                c.append([[p[i][j],p[i][z]],True])
                if k != len(FiA[i])-1:
                    a = k
                else:
                    break
            elif m1 <= sr_vel:
                for k in range(j,len(FiA[i])):
                    m2 = max(FiA[i][k]*int(FACh),FiB[i][k]*int(FBCh),FiC[i][k]*int(FCCh),FiT1[i][k]*int(FTRCh))
                    if m2 > sr_vel:
                        z=k-1
                        break
                    elif m2 <= sr_vel and k == len(FiA[i])-1:
                        z=k
                        break
                c.append([[p[i][j],p[i][z]],False])
                if k != len(FiA[i])-1:
                    a = k
                else:
                    break
        f.append(c)
        f2.append(b)
    f1=[]
    for i in f:
        c1=[]
        for j in i:
            if j[1] == True:
                c1.append(j[0])
        f1.append(c1)

    """ for i in range(len(inf)):
        if len(f[i])==1:
            if f[i][0][1]==False: """

    """ print(f)
    print(f1)
    print(f2) """
    return f , f1 , f2
# Словарь концов ветвей
def Kon(per):
    p = {}
    for key in per:
        a = list(per[key].keys())
        p[key]={a[0]:0, a[len(a)-1]:0}
    return p
# Формируем данные для построения схемы заземления
def Szazeml(p,nm_ivl,sp_zy):
    z={}
    for key in p:
        z[key]={}
    for i in sp_zy:
        if i[7] == 'ПЗ':
            if i[4] != 'Разземлен':
                p[(int(i[0]),int(i[1]))][int(i[2])]=(True,True)
            else:
                p[(int(i[0]),int(i[1]))][int(i[2])]=(True,False)
        else:
            if i[4] != 'Разземлен':
                z[(int(i[0]),int(i[1]))][int(i[2])]=(int(i[2]),i[7], i[3]+' Ом')

    a=list(p.keys())
    inf=[]
    lbsz=[]
    sp_PZ=[]
    for i in range(len(a)):
        k=['','','','','','','']
        k[1]=nm_ivl[i]
        k[4]=i
        n=list(p[a[i]].keys())
        k[2]=n[0]
        k[3]=n[1]
        
        s1,s2 =nm_ivl[i].split(Razd_simv,1)
        s1=s1.strip()
        s2=s2.strip()
        
        if p[a[i]][n[0]] !=0 and p[a[i]][n[1]] !=0:
            k[0]=1
            k[5]=p[a[i]][n[0]][1]
            k[6]=p[a[i]][n[1]][1]
            sp_PZ.append([a[i][0],a[i][1],n[0],s1])
            sp_PZ.append([a[i][0],a[i][1],n[1],s2])
        elif p[a[i]][n[0]] !=0 and p[a[i]][n[1]] ==0:
            k[0]=2
            k[5]=p[a[i]][n[0]][1]
            k[6]=0
            sp_PZ.append([a[i][0],a[i][1],n[0],s1])
        elif p[a[i]][n[0]] ==0 and p[a[i]][n[1]] !=0:
            k[0]=3
            k[5]=0
            k[6]=p[a[i]][n[1]][1]
            sp_PZ.append([a[i][0],a[i][1],n[1],s2])
        elif p[a[i]][n[0]] ==0 and p[a[i]][n[1]] ==0:
            k[0]=4
            k[5]=0
            k[6]=0
        inf.append(k)
        b=list(z[a[i]].keys())
        c=[]
        for f in b:
            c.append(z[a[i]][f])
        lbsz.append(c)
    return inf, lbsz, sp_PZ
# Исходные данные для рисования топологической схемы
def Graph(vvl,ivl_gr):
    VVL_dict={}
    r={}
    l=0
    nm_d={}
    Sdvig = {'Ц':0,'Л':-0.001,'П':0.001}
    for i in range(len(vvl)):
        if vvl[i][0] != 'Конфигурация опоры':
            n=int(vvl[i][1])
            k=int(vvl[i][2])
            l+=1
            VVL_dict['L'+str(l)]=[]
            nm_d['L'+str(l)]=vvl[i][0]
                        
        else:
            sk1 = None
            sk2 = None
            sk3 = None
            sk4 = None
            for j in range(len(vvl[i][1])):
                if vvl[i][1][j] == "(":
                    sk1=j
                if vvl[i][1][j] == ")":
                    sk2=j
            for j in range(len(vvl[i][2])):
                if vvl[i][2][j] == "(":
                    sk3=j
                if vvl[i][2][j] == ")":
                    sk4=j

            if sk1 != None and sk2 != None and sk3 != None and sk4 != None:
                n1 = abs(int(vvl[i][1][sk1+1:sk2]))
                k1 = abs(int(vvl[i][2][sk3+1:sk4]))
                n2 = int(vvl[i][1][sk2+1:])
                k2 = int(vvl[i][2][sk4+1:])
            else:
                n1 = n
                k1 = k
                n2 = int(vvl[i][1])
                k2 = int(vvl[i][2])
 
            b=False
            for j in range(len(vvl[i][3])):
                if vvl[i][3][j] == ';':
                    c = j
                    b = True
            if b:
                f1=float(Tochka(vvl[i][3][:c]))+Sdvig[op_position[vvl[i][5]]]
                f2=float(Tochka(vvl[i][3][c+1:]))+Sdvig[op_position[vvl[i][5]]]
            else:
                f1 = f2 = float(Tochka(vvl[i][3]))+Sdvig[op_position[vvl[i][5]]]

            VVL_dict['L'+str(l)].append([n1,k1,n2,k2,f1,f2,-1])
    """
    #V_k = list(VVL_dict.keys())
    for i in range(len(ivl_gr)):
        for key in VVL_dict:
            for j in range(len(VVL_dict[key])):
                if ivl_gr[i][0] == VVL_dict[key][j][0] and ivl_gr[i][1] == VVL_dict[key][j][1]:
                    if ivl_gr[i][4] < ivl_gr[i][5]:
                        if ivl_gr[i][4] <= VVL_dict[key][j][2] and ivl_gr[i][5] >= VVL_dict[key][j][3]\
                           and abs(VVL_dict[key][j][4]) < 1 and abs(VVL_dict[key][j][5]) < 1:
                            VVL_dict[key][j][6] = 0
                    elif ivl_gr[i][4] > ivl_gr[i][5]:
                        if ivl_gr[i][4] >= VVL_dict[key][j][2] and ivl_gr[i][5] <= VVL_dict[key][j][3]\
                           and abs(VVL_dict[key][j][4]) < 1 and abs(VVL_dict[key][j][5]) < 1:
                            VVL_dict[key][j][6] = 0
    """
    return VVL_dict, nm_d
            
# Функция опред наибольшего напряжения среди фаз на опоре
def MF(FiA, FiB, FiC, FiT1):
    M=[]
    for i in range(len(FiA)):
        a=[]
        for j in range(len(FiA[i])):
            a.append(max(FiA[i][j], FiB[i][j], FiC[i][j], FiT1[i][j]))
        M.append(a)
    return M
# Выбор ПС для заземления
def Zpz(M,a,b):
    mi=M[0][a][b]
    c=0
    for i in range(1,len(M)):
        if mi > M[i][a][b]:
            mi=M[i][a][b]
            c=i
    return c
# Собираем строку для таблицы
def stTable(f, f2, c, sp_PZ, key2, ky, d_PZ, per_name,key1,i):
    st=[]

    if key2 in per_name[key1]:
        st.append(str(per_name[key1][key2]))
    else:
        st.append(str(key2))
    
    st.append(d_PZ[sp_PZ[c][3]])
    a=''
    b=False
    g=False
    for j in range(len(f[i])):
        if not f[i][j][1]:
                
            if f[i][j][0][0] in per_name[ky[i]]:
                nam_op1 = per_name[ky[i]][f[i][j][0][0]]
            else:
                nam_op1 = f[i][j][0][0]
            if f[i][j][0][1] in per_name[ky[i]]:
                nam_op2 = per_name[ky[i]][f[i][j][0][1]]
            else:
                nam_op2 = f[i][j][0][1]
                
            if not g:
                a+=str(nam_op1)+'-'+str(nam_op2)
                b=True
                g=True
            else:
                a+='\n'+str(nam_op1)+'-'+str(nam_op2)
                b=True
    for j in range(len(sp_PZ)):
        if ky[i][0]==sp_PZ[j][0] and ky[i][1]==sp_PZ[j][1] and sp_PZ[j][2] in f2[i]:
            if not f2[i][sp_PZ[j][2]]:
                if not b:
                    a+=d_PZ[sp_PZ[j][3]]
                    b=True
                else:
                    a+='\n'+d_PZ[sp_PZ[j][3]]
                    b=True
    if not b:
        a+='Запрещено'
    st.append(a)
    return st
# Словарь условных побозначений ПЗ
def dict_PZ(sp_PZ):
    d_PZ={}
    for i in range(len(sp_PZ)):
        d_PZ[sp_PZ[i][3]]='ПС-'+str(i+1)
    return d_PZ
def PK(p, km):
    a=[]
    for i in range(len(p)):
        b={}
        for j in range(len(p[i])):
            b[round(abs(km[i][j]),2)]=str(p[i][j])+'n'
        a.append(b)
    return a
def Opg(a, km_d):
    b=np.zeros((np.shape(a)))
    for i in range(np.shape(a)[0]):
        f=0
        for key in km_d:
            f+=1
            if f == 1:
                c=abs(key-a[i])
                b[0]=key
                continue
            if abs(key-a[i]) < c:
                c=abs(key-a[i])
                b[i]=key
    return b
# Функция которая заменит запятую на точку
def Tochka(s):
    s_new=''
    for i in s:
        if i == ',':
            s_new+='.'
        else:
            s_new+=i
    return s_new
# Функция списка ветвей для обьединения
def SpSoed(yr_v):
    yr_v_d={}
    for i in yr_v:
        yr_v_d[i]=[]
    for key in yr_v_d:
        for i in range(len(yr_v)):
            if yr_v[i]==key:
                yr_v_d[key].append(i)
    return yr_v_d
# функция обьеденения ветвей
def SoedV(yr_v_d,sp1):
    sp2=[]
    for key in yr_v_d:
        a=[]
        for i in range(len(yr_v_d[key])):
            if i==0:
                a+=sp1[yr_v_d[key][i]]
            else:
                a+=sp1[yr_v_d[key][i]][1:]
        
        sp2.append(a)
    return sp2
# Переименовываем обьеденённые участки
def ReName(yr_v_d,nm_ivl_1):
    nm_ivl_2=[]
    for key in yr_v_d:
        if len(yr_v_d[key])==1:
            nm_ivl_2.append(nm_ivl_1[yr_v_d[key][0]])
        elif len(yr_v_d[key])>1:          

            s1,s2 =nm_ivl_1[yr_v_d[key][0]].split(Razd_simv,1)
            s1=s1.strip()
            s2=s2.strip()

            s3,s4 =nm_ivl_1[yr_v_d[key][len(yr_v_d[key])-1]].split(Razd_simv,1)
            s3=s3.strip()
            s4=s4.strip()

            nm_ivl_2.append(s1+'-'+s4)
    return nm_ivl_2
# Список обьеденённых ВЛ
def RePer(yr_v_d,per):
    a=list(per.keys())
    sp_b={}
    for key in yr_v_d:
        ych=(a[yr_v_d[key][0]][0],a[yr_v_d[key][len(yr_v_d[key])-1]][1])
        c={}
        for i in range(len(yr_v_d[key])):
            c[a[yr_v_d[key][i]]]=''
        sp_b[ych]=c
    per1={}
    for key1 in sp_b:
        c={}
        for key2 in sp_b[key1]:
            c.update(per[key2])
        per1[key1]=c
    return sp_b, per1
# Переделываем список ЗУ
def ReZy(sp_b,zy):
    for key1 in sp_b:
       for key2 in sp_b[key1]:
           for i in range(len(zy)):
               if (int(zy[i][0]),int(zy[i][1]))==key2:
                  (zy[i][0],zy[i][1])=(str(key1[0]),str(key1[1]))
    return zy
#Формируем список отпаек
def Otpaiki(sp_b,ivl_gr,nm_ivl):
    for key1 in sp_b:
        for key2 in sp_b[key1]:
            for i in ivl_gr:
                if (i[0],i[1])==key2:
                    sp_b[key1][key2]=i[3]
    
    c=list(sp_b.keys())
    m=[]
    n=[]

    a={}
    for i in range(len(c)):
        
        b=[]
        m.append('')
        for key2 in sp_b[c[i]]:
            a[key2] = ''
            for h in ivl_gr:
                if (h[0]==key2[0] and h[1]!=key2[1]) or  (h[0]!=key2[0] and h[1]==key2[1]):
                    if (h[0],h[1]) not in a:
                        
                        if h[0] == key2[0]:
                            for g in ivl_gr:
                                if (g[0],g[1]) == key2:
                                    break
                            b.append([g[4],(h[0],h[1]),''])
                            a[(h[0],h[1])] = ''

                        elif h[0] == key2[1]:
                            for g in ivl_gr:
                                if (g[0],g[1]) == key2:
                                    break
                            b.append([g[5],(h[0],h[1]),''])
                            a[(h[0],h[1])] = ''

            m[i]=sp_b[c[i]][key2]

        for j in range(len(b)):
            g = -1
            for k in sp_b:
                g += 1
                if b[j][1] in sp_b[k]:
                    
                    s1,s2 =nm_ivl[g].split(Razd_simv,1)
                    s1=s1.strip()
                    s2=s2.strip()
                    
                    OtN=s2

                    b[j][1]=sp_b[k][b[j][1]]
                    b[j][2]=OtN
        
        Trig =True
        while Trig:
            Trig = False
            for j in range(len(b)):
                if b[j][2]=="":
                    del b[j]
                    Trig =True
                    break
            


        n.append(b)


    return m, n
def Idop(ind):
    i=Katalog.get(ind,False)
    if not i:
        return -1
    else:
        return Kat[Katalog.get(ind)+str(20)].value
# Убираем участки в которые не входит БЗ
def F2obr(key2, f):
    a = None
    b = None
    for i in range(len(f)):
        if f[i][1] == False:
            if f[i][0][0] < f[i][0][1]:
                if key2 >= f[i][0][0] and key2 <= f[i][0][1]:
                    a = f[i][0][0]
                    b = f[i][0][1]
            elif f[i][0][0] > f[i][0][1]:
                if key2 <= f[i][0][0] and key2 >= f[i][0][1]:
                    a = f[i][0][0]
                    b = f[i][0][1]
            elif f[i][0][0] == f[i][0][1] and key2 == f[i][0][0]:
                a = f[i][0][0]
                b = f[i][0][1]
    return a, b

# Переименование отпаечных опор
def Yz_p(ivl,yr):

    d = {}
    p = {}
    for i in range(len(ivl)):
        
        p[(ivl[i][0],ivl[i][1])] = {}
        if ivl[i][0] not in d:
            d[ivl[i][0]]=[[ivl[i][4],i]]
        elif ivl[i][0]  in d:
            d[ivl[i][0]].append([ivl[i][4],i])
        if ivl[i][1] not in d:
            d[ivl[i][1]]=[[ivl[i][5],i]]
        elif ivl[i][1]  in d:
            d[ivl[i][1]].append([ivl[i][5],i])
    
    if yr != False:
        p1 = {}
        a = list(yr.keys())
        b={}
        b2={}
        for i in range(len(a)):
            p1[(ivl[yr[a[i]][0]][0], ivl[yr[a[i]][len(yr[a[i]])-1]][1])] = {}
            b[a[i]] ={}
            for j in yr[a[i]]:
                for k in yr[a[i]]:
                    if ivl[j][1] == ivl[k][0]:
                         b[a[i]][ivl[k][0]] = str(ivl[k][4]) #"'"+

        a2 = list(p1.keys())
        for i in range(1,len(a)):
            for j in range(len(a)):
                for k in yr[a[j]]:
                    if ivl[yr[a[i]][0]][0] == ivl[k][1] and a2[i] not in b2:
                        p1[a2[i]][ivl[yr[a[i]][0]][4]] = b[a[j]][ivl[k][1]]
                        b2[a2[i]] = ''
        
        return p1
    else:
        return p

# Подписи окуда запитана отпайка
def PodpSz(ivl_gr,yr_v_d):
    nam1 = []
    nam2 = []
    for i in range(len(ivl_gr)):
        
        s1,s2 =ivl_gr[i][6].split(Razd_simv,1)
        s1=s1.strip()
        s2=s2.strip()
        
        nam1.append(s1)
        nam2.append(s2)

    def Napr(a,b):
        Napr={'В':{'С-В':-1,'С':-1,'С-З':-1,'Ю-В':1,'Ю':1,'Ю-З':1,'В':0,'3':0},\
              'С-В':{'З':-1,'С':-1,'С-З':-1,'Ю-В':1,'Ю':1,'В':1,'С-В':0,'Ю-З':0},\
              'С':{'Ю-З':-1,'З':-1,'С-З':-1,'С-В':1,'В':1,'Ю-В':1,'С':0,'Ю':0},\
              'С-З':{'Ю':-1,'Ю-З':-1,'З':-1,'С':1,'С-В':1,'В':1,'С-З':0,'Ю-В':0},\
              'З':{'Ю-В':-1,'Ю':-1,'Ю-З':-1,'С-З':1,'С':1,'С-В':1,'З':0,'В':0},\
              'Ю-З':{'В':-1,'Ю-В':-1,'Ю':-1,'З':1,'С-З':1,'С':1,'Ю-З':0,'С-В':0},\
              'Ю':{'С-В':-1,'В':-1,'Ю-В':-1,'Ю-З':1,'З':1,'С-З':1,'Ю':0,'С':0},\
              'Ю-В':{'С':-1,'С-В':-1,'В':-1,'Ю':1,'Ю-З':1,'З':1,'Ю-В':0,'С-З':0}}
        return Napr[a][b]
    
    sp_napr =[]
    
    for i in range(len(ivl_gr)):
        sp_napr.append([])
        for j in range(len(ivl_gr)):
            if ivl_gr[i][0] == ivl_gr[j][1]:
                sp_napr[i].append([(j,1),-1,nam1[j],Napr(ivl_gr[i][3],ivl_gr[j][3])*(1)])
            elif ivl_gr[i][1] == ivl_gr[j][0]:
                sp_napr[i].append([(j,2),1,nam2[j],Napr(ivl_gr[i][3],ivl_gr[j][3])*(-1)])
            elif ivl_gr[i][0] == ivl_gr[j][0]  and ivl_gr[i][1] != ivl_gr[j][1]:
                sp_napr[i].append([(j,2),-1,nam2[j],Napr(ivl_gr[i][3],ivl_gr[j][3])*(-1)])

    #print(sp_napr)
    sn =[]            
    if yr_v_d != False:
        k_y = list(yr_v_d.keys())
        y_nam = []
        
        j=-1
        for key in yr_v_d:
            j+=1
            sn.append([])
            for i in range(len(sp_napr[yr_v_d[key][0]])):
                if sp_napr[yr_v_d[key][0]][i][1] == -1:
                    sn[j].append(sp_napr[yr_v_d[key][0]][i])
            for i in range(len(sp_napr[yr_v_d[key][len(yr_v_d[key])-1]])):
                if sp_napr[yr_v_d[key][len(yr_v_d[key])-1]][i][1] == 1:
                    sn[j].append(sp_napr[yr_v_d[key][len(yr_v_d[key])-1]][i])
                    
    
        #print(sn)
        for i in range(len(sn)):
            for j in range(len(sn[i])):
                Trig = False
                for k in range(len(k_y)):
                    for g in yr_v_d[k_y[k]]:
                        if g == sn[i][j][0][0]:
                            Trig = True
                            if sn[i][j][0][1] == 1:
                                sn[i][j][2] = nam1[yr_v_d[k_y[k]][0]]
                            elif sn[i][j][0][1] == 2:
                                sn[i][j][2] = nam2[yr_v_d[k_y[k]][len(yr_v_d[k_y[k]])-1]]
                            break
                    if Trig:
                        break
        #print(sn)
        return sn
    else:
        return sp_napr

        
def PointGen(ivl_gr,yr_v_d,sp_vvl,marker,per,nm_ivl,sp_zy,km,per_name):
    #per_name = Yz_p(ivl_gr,yr_v_d)
    sp_pit = PodpSz(ivl_gr, yr_v_d)
    VVL_dict, nm_d = Graph(sp_vvl, ivl_gr)
    
    gr_list = []
    axi_list = []
    otp_list = []
    point_list =[]
    max_len = 0
    koef = 0.01
    
    if marker:
        sp_b, per=RePer(yr_v_d,per)
        m, n = Otpaiki(sp_b,ivl_gr,nm_ivl)
        
        n_o = [list(per[key].keys()) for key in per]
        yr_list = list(yr_v_d.keys())
        re_op_key = list(per_name.keys())

        inf, lbsz, sp_PZ = Szazeml(Kon(per),nm_ivl,ReZy(sp_b,sp_zy))

        for i in range(len(nm_ivl)):
            mn = 0
            mx = 0
            gr = {}
            point = set()
            point_sp = []
            for j in VVL_dict:
                a = []
                for k in yr_v_d[yr_list[i]]:
                    for l in range(len(VVL_dict[j])):
                        if ivl_gr[k][0] == VVL_dict[j][l][0] and ivl_gr[k][1] == VVL_dict[j][l][1]:
                            if VVL_dict[j][l][2] not in point:
                                point.add(VVL_dict[j][l][2])
                                if VVL_dict[j][l][2] in per_name[re_op_key[i]]:
                                    point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][2])],\
                                                        per_name[re_op_key[i]][VVL_dict[j][l][2]]])
                                    if len(per_name[re_op_key[i]][VVL_dict[j][l][2]]) > max_len:
                                        max_len = len(per_name[re_op_key[i]][VVL_dict[j][l][2]]) 
                                else:
                                    point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][2])],\
                                                        str(VVL_dict[j][l][2])])
                                    if len(str(VVL_dict[j][l][2])) > max_len:
                                        max_len = len(str(VVL_dict[j][l][2])) 
                            if VVL_dict[j][l][3] not in point:
                                point.add(VVL_dict[j][l][3])
                                if VVL_dict[j][l][3] in per_name[re_op_key[i]]:
                                    point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][3])],\
                                                        per_name[re_op_key[i]][VVL_dict[j][l][3]]])
                                    if len(per_name[re_op_key[i]][VVL_dict[j][l][3]]) > max_len:
                                        max_len = len(per_name[re_op_key[i]][VVL_dict[j][l][3]]) 
                                else:
                                    if len(str(VVL_dict[j][l][3])) > max_len:
                                        max_len = len(str(VVL_dict[j][l][3])) 
                                    point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][3])],\
                                                        str(VVL_dict[j][l][3])])
                            a.append([[ km[i][n_o[i].index(VVL_dict[j][l][2])]\
                                        ,km[i][n_o[i].index(VVL_dict[j][l][3])] ]\
                                        ,[VVL_dict[j][l][4], VVL_dict[j][l][5]]])
                            v1 = max(VVL_dict[j][l][4], VVL_dict[j][l][5])
                            v2 = min(VVL_dict[j][l][4], VVL_dict[j][l][5])
                            mx = v1 if v1 > mx else mx
                            mn = v2 if v2 < mn else mn
                if len(a)>0:
                    gr[j]=a
            axi=[min(km[i]),max(km[i]),mn*1.1,mx*1.1]
            otp = [[km[i][n_o[i].index(n[i][j][0])],0] for j in range(len(n[i]))]

            for j in lbsz[i]:
                if j[0] not in point:
                    if j[0] in per_name[re_op_key[i]]:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        per_name[re_op_key[i]][j[0]]])
                                        
                        if len(per_name[re_op_key[i]][j[0]]) > max_len:
                            max_len = len(per_name[re_op_key[i]][j[0]]) 
                    else:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        str(j[0])])
                        if len(str(j[0])) > max_len:
                            max_len = len(str(j[0]))
            for j in n[i]:
                if j[0] not in point:
                    if j[0] in per_name[re_op_key[i]]:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        per_name[re_op_key[i]][j[0]]])
                                        
                        if len(per_name[re_op_key[i]][j[0]]) > max_len:
                            max_len = len(per_name[re_op_key[i]][j[0]]) 
                    else:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        str(j[0])])
                        if len(str(j[0])) > max_len:
                            max_len = len(str(j[0]))
                            
                                                    
            point_sp = sorted(point_sp)    
            
            min_len_otst = abs(min(km[i])-max(km[i]))*max_len*koef
            
            while True:
                for j in range(len(point_sp)):
                    if j == 0: continue
                    elif abs(point_sp[j-1][0]-point_sp[j][0])<min_len_otst:
                        del point_sp[j]
                        break
                else: break
                
            
            gr_list.append(gr)
            axi_list.append(axi)
            otp_list.append(otp)
            point_list.append(point_sp)

            
                        
    else:

        n_o = [ list(per[key].keys()) for key in per]
        re_op_key = list(per_name.keys())
        inf, lbsz, sp_PZ = Szazeml(Kon(per),nm_ivl,sp_zy)
        for i in range(len(nm_ivl)):
            mn = 0
            mx = 0
            gr = {}
            point = set()
            point_sp = []
            for j in VVL_dict:
                a = []
                for l in range(len(VVL_dict[j])):
                    if ivl_gr[i][0] == VVL_dict[j][l][0] and ivl_gr[i][1] == VVL_dict[j][l][1]:
                        if VVL_dict[j][l][2] not in point:
                            point.add(VVL_dict[j][l][2])
                            if VVL_dict[j][l][2] in per_name[re_op_key[i]]:
                                point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][2])],\
                                                    per_name[re_op_key[i]][VVL_dict[j][l][2]]])
                                if len(per_name[re_op_key[i]][VVL_dict[j][l][2]]) > max_len:
                                        max_len = len(per_name[re_op_key[i]][VVL_dict[j][l][2]]) 
                            else:
                                point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][2])],\
                                                    str(VVL_dict[j][l][2])])
                                if len(str(VVL_dict[j][l][2])) > max_len:
                                        max_len = len(str(VVL_dict[j][l][2])) 
                        if VVL_dict[j][l][3] not in point:
                            point.add(VVL_dict[j][l][3])
                            if VVL_dict[j][l][3] in per_name[re_op_key[i]]:
                                point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][3])],\
                                                    per_name[re_op_key[i]][VVL_dict[j][l][3]]])
                                if len(per_name[re_op_key[i]][VVL_dict[j][l][3]]) > max_len:
                                        max_len = len(per_name[re_op_key[i]][VVL_dict[j][l][3]])
                            else:
                                point_sp.append([km[i][n_o[i].index(VVL_dict[j][l][3])],\
                                                    str(VVL_dict[j][l][3])])
                                if len(str(VVL_dict[j][l][3])) > max_len:
                                        max_len = len(str(VVL_dict[j][l][3])) 
                        a.append([[ km[i][n_o[i].index(VVL_dict[j][l][2])]\
                                    ,km[i][n_o[i].index(VVL_dict[j][l][3])] ]\
                                    ,[VVL_dict[j][l][4], VVL_dict[j][l][5]]])
                        
                        v1 = max(VVL_dict[j][l][4], VVL_dict[j][l][5])
                        v2 = min(VVL_dict[j][l][4], VVL_dict[j][l][5])
                        mx = v1 if v1 > mx else mx
                        mn = v2 if v2 < mn else mn
                if len(a)>0:
                    gr[j]=a
            axi=[min(km[i]),max(km[i]),mn*1.1,mx*1.1]

            for j in lbsz[i]:
                if j[0] not in point:
                    if j[0] in per_name[re_op_key[i]]:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        per_name[re_op_key[i]][j[0]]])
                                        
                        if len(per_name[re_op_key[i]][j[0]]) > max_len:
                            max_len = len(per_name[re_op_key[i]][j[0]]) 
                    else:
                        point_sp.append([km[i][n_o[i].index(j[0])],\
                                        str(j[0])])
                        if len(str(j[0])) > max_len:
                            max_len = len(str(j[0]))

                            
                                                    
            point_sp = sorted(point_sp)

            min_len_otst = abs(min(km[i])-max(km[i]))*max_len*koef
            
            while True:
                for j in range(len(point_sp)):
                    if j == 0: continue
                    elif abs(point_sp[j-1][0]-point_sp[j][0])<min_len_otst:
                        del point_sp[j]
                        break
                else: break
            
            gr_list.append(gr)
            axi_list.append(axi)
            otp_list.append([])
            point_list.append(point_sp)

    return gr_list, axi_list, otp_list, point_list

def KL_metki(sp,resize=None):
    if resize != None:
        s = []
        r = list(resize.keys())
        for i in range(len(r)):
            s.append([])
            for j in resize[r[i]]:
                s[i]+=sp[j]
    else:
        s = sp
    
    s_d = []
    
    for i in range(len(s)):
        s_d.append({})
        for j in range(len(s[i])):

            if s[i][j][0] not in s_d[i]:
                if s[i][j][2]:
                    s_d[i][s[i][j][0]] = "L"
            else:
                if s_d[i][s[i][j][0]] == "R" and s[i][j][2]:
                    s_d[i][s[i][j][0]] = "LR"

            if s[i][j][1] not in s_d[i]:
                if s[i][j][3]:
                    s_d[i][s[i][j][1]] = "R"
            else:
                if s_d[i][s[i][j][1]] == "L" and s[i][j][3]:
                    s_d[i][s[i][j][1]] = "LR"

    rez =[list(i.items()) for i in s_d]
    
    return rez


def UserReOp(sp,re,resize=None,per=None):
    if resize != None:
        s = []
        r = list(resize.keys())
        for i in range(len(r)):
            s.append([])
            for j in resize[r[i]]:
                s[i]+=sp[j]
    else:
        s = sp
    D = {}

    if per!=None:
        j=-1
        for i in per:
            j+=1
            d = list(per[i].keys())
            if i[0] not in D:
                D[i[0]]={d[0]:0}
            else:
                if d[0] not in D[i[0]]:
                    D[i[0]][d[0]]=j #len(D[i[0]])
            if i[1] not in D:
                D[i[1]]={d[len(d)-1]:0}
            else:
                if d[1] not in D[i[1]]:
                    D[i[1]][d[len(d)-1]]=j #len(D[i[1]])
        for i in per:
            D[i[0]]={v:k for k,v in D[i[0]].items()}
            D[i[1]]={v:k for k,v in D[i[1]].items()}
        y = {}
        j=-1
        for k in resize:
            j+=1
            for i in resize[k]:
                y[i]=j
        
        r = list(re.keys())
        #
        adr = {}
        for k in D:
            trig = -1
            if len(D[k])<2:continue
            for i in range(len(per)):
                if i in D[k] and trig==-1:
                    trig=i
                    continue
                elif i in D[k] and trig!=-1:
                    adr[r[y[i]]]=[r[y[trig]],D[k][trig],D[k][i]]

    re_op_key = list(re.keys())
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j][4]:
                re[re_op_key[i]][s[i][j][0]]=s[i][j][4]
            if s[i][j][5]:
                re[re_op_key[i]][s[i][j][1]]=s[i][j][5]
    if per!=None:
        for k in adr:
            if adr[k][1] in re[adr[k][0]]:
                re[k][adr[k][2]]=re[adr[k][0]][adr[k][1]]
   
    return re

def ReZaprYch(s1,s2,f,f1,f2,ind,state):
    try:
        n=int(s1)
        k=int(s2)
        if n<0 or k<0: raise Exception
        if n==k: raise Exception
    except:
        return
    gr = list(f2[ind].keys())
    if gr[0]<gr[1] and (n<gr[0] or k>gr[1] or n>k):
        return
    elif gr[0]>gr[1] and (n>gr[0] or k<gr[1] or n<k):
        return
    sp = []
    for i in range(len(f[ind])):
        if gr[0]<gr[1]:
            if f[ind][i][0][0]<=n<=f[ind][i][0][1] and not f[ind][i][0][0]<=k<=f[ind][i][0][1]:
                if f[ind][i][1] != state:
                    if n!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],n],f[ind][i][1]])
                    sp.append([[n,f[ind][i][0][1]],state])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif not f[ind][i][0][0]<=n<=f[ind][i][0][1] and f[ind][i][0][0]<=k<=f[ind][i][0][1]:
                if f[ind][i][1] !=state:
                    if k!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],k],state])
                    sp.append([[k,f[ind][i][0][1]],f[ind][i][1]])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif f[ind][i][0][0]<=n<=f[ind][i][0][1] and f[ind][i][0][0]<=k<=f[ind][i][0][1]:
                if f[ind][i][1] !=state:
                    if n!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],n],f[ind][i][1]])
                    sp.append([[n,k],state])
                    if k!=f[ind][i][0][1]:
                        sp.append([[k,f[ind][i][0][1]],f[ind][i][1]])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif not f[ind][i][0][0]<=n<=f[ind][i][0][1] and not f[ind][i][0][0]<=k<=f[ind][i][0][1]:
                sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])

        elif gr[0]>gr[1]:
            if f[ind][i][0][0]>=n>=f[ind][i][0][1] and not f[ind][i][0][0]>=k>=f[ind][i][0][1]:
                if f[ind][i][1] !=state:
                    if n!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],n],f[ind][i][1]])
                    sp.append([[n,f[ind][i][0][1]],state])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif not f[ind][i][0][0]>=n>=f[ind][i][0][1] and f[ind][i][0][0]>=k>=f[ind][i][0][1]:
                if f[ind][i][1] !=state:
                    if k!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],k],state])
                    sp.append([[k,f[ind][i][0][1]],f[ind][i][1]])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif f[ind][i][0][0]>=n>=f[ind][i][0][1] and f[ind][i][0][0]>=k>=f[ind][i][0][1]:
                if f[ind][i][1] !=state:
                    if n!=f[ind][i][0][0]:
                        sp.append([[f[ind][i][0][0],n],f[ind][i][1]])
                    sp.append([[n,k],state])
                    if k!=f[ind][i][0][1]:
                        sp.append([[k,f[ind][i][0][1]],f[ind][i][1]])
                else:
                    sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])
            elif not f[ind][i][0][0]>=n>=f[ind][i][0][1] and not f[ind][i][0][0]>=k>=f[ind][i][0][1]:
                sp.append([[f[ind][i][0][0],f[ind][i][0][1]],f[ind][i][1]])

    sp1 = []
    j=-1
    for i in range(len(sp)):
        if sp1 == []:
            sp1.append(sp[i])
            j+=1
        else:
            if sp1[j][0][1]==sp[i][0][0] and sp1[j][1]==sp[i][1]:
                sp1[j]=[[sp1[j][0][0],sp[i][0][1]],sp1[j][1]]
            else:
                sp1.append(sp[i])
                j+=1

    sp2 = [sp1[i][0] for i in range(len(sp1)) if sp1[i][1]]

    f[ind] = sp1
    f1[ind] = sp2

    return (f ,f1,f2)



def PZandZpar(inf,f2,ind,botton):
    if botton==1:
        if inf[ind][0]==1 or inf[ind][0]==2:
            inf[ind][5] = not inf[ind][5]
    elif botton==2:
        if inf[ind][0]==1 or inf[ind][0]==3:
            inf[ind][6] = not inf[ind][6]
    elif botton==3:
        if inf[ind][0]==1 or inf[ind][0]==2:
            f2[ind][inf[ind][2]] = not f2[ind][inf[ind][2]]
    elif botton==4:
        if inf[ind][0]==1 or inf[ind][0]==3:
            f2[ind][inf[ind][3]] = not f2[ind][inf[ind][3]]

    return inf, f2

    

    

    
    


