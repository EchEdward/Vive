import Kat_lists as Kl
import rnn
from openpyxl import load_workbook

Katalog=rnn.ExDict()
""" XHkat={ 'ABC': 1, 'ACB': 2, 'BCA': 3, 'BAC': 4, 'CAB': 5, 'CBA': 6,
                '-ABC': -6, '-ACB': -3, '-BCA': -2, '-BAC': -5, '-CAB': -4, '-CBA': -1} """
d_to=Kl.Sl_TipOp()
Katal = load_workbook(filename = 'Katal.xlsx')
Kat = Katal['Kat']

ex = []
ex.append("1.Не объявлена ветвь")
ex.append("2.После объявления ветви должен быть задан как минимум один участок")
ex.append("3.Таблица РВЛ пуста")
ex.append("4.Не заполнена ячейка")
ex.append("5.В название ветви записано неверное количество разделительных знаков")
ex.append("6.Введено не корректное значение")
ex.append("7.Не выбран параметр")
ex.append("8.Данная ветвь не связана с существующими")
ex.append("9.Заданы одноимённые опоры")
ex.append("10.Участок не имеет общей опоры с предыдущим участком")
ex.append("11.Не совпадает последовательность опор на участках")
ex.append("12.Не везде установлены уровни ветвей")
ex.append("13.Не соблюдён порядок ветвей")
ex.append("14.В уровне не может быть больше одной ветви начинающейся с одного узла")
ex.append("15.Ветвь с идентичными узлами уже задана")
ex.append("16.Ветвь направлена в занятую сторону")
ex.append("17.Таблица ВВЛ пуста")
ex.append("18.Не обьявлена влияющая ВЛ")
ex.append("19.После объявления влияющей ВЛ должен быть задан как минимум один участок")
ex.append("20.Ссылка на несуществующую ветвь РВЛ")
ex.append("21.Ссылка на несуществующий участок РВЛ")
ex.append("22.ЗУ на данной опоре уже включено")
ex.append("23.ПЗ установлено не на краю ветви")
ex.append("24.Ссылка на несущестующую опору РВЛ")
ex.append("25.Строка с такими параметрами уже введена")
ex.append("26.Не может при не нулевой длинне быть нулевое количество опор и наоборот")
ex.append("27.Введенно заземлений тросов ВВЛ больше чем самих ВВЛ")
ex.append("28.Данный участок пересекается с ранее заданным")
ex.append("29.Включен трос, для опоры у которой нету троса")
ex.append("30.На взаимном участке сближения на нулевом растоянии друг от друга не может быть одинаковые не двухцепные опоры")
ex.append("31.На данном участке провода выбранных опор расположены недопустимо близко")
ex.append("32.На двухцепной опоре тросы задаются только на РВЛ")


def ColOp(s,Text=True,V=True,Otr=False):
    n=""
    m=""
    s = s.strip()
    if s == "":
        return (ex[3],n,m)

    a = s.find("(")
    b = s.rfind(")")

    if a!=-1 and b!=-1 and V:
        if a != 0:
            return (ex[5],n,m)
        s1 = s[a+1:b]
        if s1=="":
            return (ex[5],n,m)
        else:
            if not Text:
                if s1.find('.') ==-1 and (s1.find('-') ==-1  or (s.find("-")==s.rfind("-") and Otr)):
                    try:
                        m = int(s1)
                    except Exception:
                        return (ex[5],n,m)
                else:
                    return (ex[5],n,m)
            else:
                m = s1
        s2 = s[b+1:]
        if s2.find('.') ==-1 and s2.find('-') ==-1:
            try:
                n = int(s2)
            except Exception:
                return (ex[5],n,m)
        else:
            return (ex[5],n,m)
        
                
    else:
        if s.find('.') ==-1 and s.find("-")==-1: 
            try:
                n = int(s)
            except Exception:
                return (ex[5],n,m)
        else:
            return (ex[5],n,m)
    return ("",n,m)

def DlPQ(s,col=1,Mn=False, notNul=False):
    s = s.strip()
    if s == "":
        return ex[3]
    sp = s.split(";")

    if col==0:
        try:
            if s.find("-")!=-1 and Mn: raise Exception
            a=float(s.replace(",","."))
            if a == 0 and notNul==True: raise Exception
        except Exception:
            return ex[5]

    elif col==1:
        if len(sp)<1 or len(sp)>2:
            return ex[5]
        else:
            try:
                for el in sp:
                    if el.find("-")!=-1 and Mn: raise Exception
                    float(el.replace(",","."))
            except Exception:
                return ex[5]

    elif col == 2:
        if len(sp)<1 or len(sp)>3:
            return ex[5]
        else:
            try:
                for el in sp:
                    if el.find("-")!=-1 and Mn: raise Exception
                    a=float(el.replace(",","."))
                    if a == 0 and notNul==True: raise Exception
            except Exception:
                return ex[5]
    
    return ""

def OchrVetv(sp,kompas=None,Trig=False):
    komp = {"В":set(["С","Ю","В"]),"З":set(["С","Ю","З"]),"С":set(["В","З","С"]),"Ю":set(["В","З","Ю"])}
    d_n = set()
    for i in range(len(sp)):
        a=[]
        b=[]
        #Перед
        for m in range(len(sp)):
            if i==m: continue
            if sp[i][0]==sp[m][0] and sp[i][1]==sp[m][1]:
                return (ex[14],m)
            if sp[i][0]==sp[m][1]:
                a.append(m)
        #После
        for n in range(len(sp)):
            if i==n: continue
            if sp[i][1]==sp[n][0]:
                b.append(n)
                if kompas != None:
                    if kompas[n] in komp[kompas[i]] and (sp[n][0],kompas[n]) not in d_n:
                        d_n.add((sp[n][0],kompas[n]))
                    else: return (ex[15],n)

        
        if len(sp)>1 and len(a)==0 and len(b)==0:
            return (ex[7],i)
        if i==0 and len(a)!=0:
            return (ex[12],a[0])
        tr1=False
        for n in range(len(b)):
            if b[n]-1==i:
                tr1=True
        if (not tr1 or (Trig and len(b)>1)) and len(b)!=0:
            return (ex[13],b[1]) if (Trig and len(b)>1) else (ex[12],b[0])

    return ("",-1)
#print(OchrVetv([(1,2),(2,3),(3,4),(2,5),(5,6),(5,7)],Trig=False))
                
           

def Posled(a,b,m,n):
    if m==n:
        return ex[8]
    if a==None and b==None:
        return ""
    elif a>b and m>n and b!=m:
        return ex[9]
    elif a>b and m<n:
        return ex[10]
    elif a<b and m<n and b!=m:
        return ex[9]
    elif a<b and m>n:
        return ex[10]
    return ""


def Sblizh(ych,kord,d_kord_ivl,l):
    l = min([float(i) for i in l.replace(",",".").split(";")])
    for key in d_kord_ivl:
        if key[:2]==ych[:2]:
            Trig = False
            if key[2]<key[3]:
                if (ych[3]>key[2] and key[3]>ych[2]) or (key[3]>ych[2] and ych[3]>key[2]):
                    Trig = True
            elif key[2]>key[3]:
                if (ych[3]<key[2] and key[3]<ych[2]) or (key[3]<ych[2] and ych[3]<key[2]):
                    Trig = True
            
            if Trig:
                if l==0 and d_kord_ivl[key][12]==kord[12]:
                    return ex[29]

            h=[kord[3]-kord[6],kord[4]-kord[6],kord[5]-kord[6],kord[9],kord[10],\
                d_kord_ivl[key][3]-d_kord_ivl[key][6],d_kord_ivl[key][4]-d_kord_ivl[key][6],\
                d_kord_ivl[key][5]-d_kord_ivl[key][6],d_kord_ivl[key][9],d_kord_ivl[key][10]]

            x=[kord[0],kord[1],kord[2],kord[7],kord[8],\
                d_kord_ivl[key][0]+l,d_kord_ivl[key][1]+l,\
                d_kord_ivl[key][2]+l,d_kord_ivl[key][7]+l,d_kord_ivl[key][8]+l]
            
            h1=[]
            x1=[]
            
            for i in range(len(h)):
                if (i==8 or i==9) and abs(l)<0.5 and ((d_kord_ivl[key][11] =="Л" and kord[11]=="П") or (d_kord_ivl[key][11] =="П" and kord[11]=="Л")):
                    continue
                if h[i]!=0:
                    x1.append(x[i])
                    h1.append(h[i])

            if abs(l)<0.5 and ((d_kord_ivl[key][11] =="Л" and kord[11]=="П") or (d_kord_ivl[key][11] =="П" and kord[11]=="Л")):
                if kord[14] != "Не выбран" or kord[15] != "Не выбран": #d_kord_ivl[key][14] != "Не выбран" and
                    return ex[31]
            
            for i in range(len(h1)):
                for j in range(len(h1)):
                    if i!=j and ((x1[i]-x1[j])**2+(h1[i]-h1[j])**2)**0.5<0.1:
                        return ex[30]
 
    return ""

                    
            




def ScanId(ivl,vvl,zy,zytr,zvl,r_s,use):
    if not use:
        return
    l_vetvi =[]
    l_ind=[]
    op1_1 = None
    op1_2 = None
    Trig = True
    Yrovn = None
    d_Yrovn ={}
    d_Yrovn2 ={}
    kompas = []
    d_ych={}
    d_kord_ivl={}
    #d_kord_vvl={}


    #3
    if len(ivl)==0: 
        return (1,-1,-1,ex[2])
    for i in range(len(ivl)):
        #1
        if i == 0 and ivl[i][0] == "Конфигурация опоры":
            return (1,i,9,ex[0])
        #2
        if i == len(ivl)-1 and ivl[i][0] != "Конфигурация опоры":
            return (1,i,9,ex[1])
        elif ivl[i][0] != "Конфигурация опоры" and ivl[i+1][0] != "Конфигурация опоры":
            return (1,i,9,ex[1])

        # Проверка строки ветви
        if ivl[i][0] != "Конфигурация опоры":
            # Название ветви
            if ivl[i][0] == "":
                return (1,i,[0,0],ex[3])
            rez = [i for i in ivl[i][0].split(r_s) if i.strip()!=""]
            if ivl[i][0].count(r_s) !=1 or len(rez)!=2:
                return (1,i,[0,0],ex[4])
            
            # Первый узел
            rez = ColOp(ivl[i][2],Text=False,V=False)
            if rez[0] == "": n = rez[1]
            else: return(1,i,[2,2],rez[0])
                
            # Второй узел
            rez = ColOp(ivl[i][3],Text=False,V=False)
            if rez[0] == "": k = rez[1]
            else: return(1,i,[3,3],rez[0])

            l_vetvi.append((n,k))
            l_ind.append(i)

            op1_1 = None
            op1_2 = None
            Trig = True


            #12
            if Yrovn == None:
                Yrovn = False if ivl[i][4]=="Нет" else True
            else:
                if Yrovn != (False if ivl[i][4]=="Нет" else True):
                    return(1,i,9,ex[11])
            
            #14
            if ivl[i][4]!="Нет" and ivl[i][4] not in d_Yrovn:
                d_Yrovn[ivl[i][4]] = [(n,k)]
                d_Yrovn2[ivl[i][4]] = [i]
            elif ivl[i][4]!="Нет" and ivl[i][4] in d_Yrovn:
                d_Yrovn[ivl[i][4]].append((n,k))
                d_Yrovn2[ivl[i][4]].append(i)

            
            kompas.append(ivl[i][1])


        
        else:
            # Длинна участка
            rez = DlPQ(ivl[i][1],col=1,Mn=True)
            if rez != "": return(1,i,[1,1],rez)

            # Первая опора
            rez = ColOp(ivl[i][2],Text=True,V=True)
            if rez[0] == "": op1 = rez[1]
            else: return(1,i,[2,2],rez[0])
                
            # Последняя опора
            rez = ColOp(ivl[i][3],Text=True,V=True)
            if rez[0] == "": op2 = rez[1]
            else: return(1,i,[3,3],rez[0])

            # Тип опоры
            if ivl[i][5] == "Не выбран":
                return(1,i,9,ex[6]+": Тип опоры")
            
            # Марка провода
            if ivl[i][6] == "Не выбран":
                return(1,i,9,ex[6]+": Марка провода")

            #10, 11
            rez = Posled(op1_1,op1_2,op1,op2)
            if rez!="":
                return(1,i,[2,3],rez)
            else:
                op1_1=op1
                op1_2=op2

            if Trig:
                d_ych[(n,k)]=[op1,op2]
                Trig = False
            else:
                d_ych[(n,k)][1]=op2

            kord = rnn.VF(d_to[ivl[i][5]],1,'OpFig',Katalog,Kat)
            if ivl[i][7] != "Не выбран"  and kord[9]==0: #and kord[7]==0
                return(1,i,9,ex[28]+" №1")
            if ivl[i][8] != "Не выбран"  and kord[10]==0: #and kord[8]==0
                return(1,i,9,ex[28]+" №2")

            d_kord_ivl[(n,k,op1,op2)]=list(kord)+ivl[i][5:9]
                
    #print(d_ych)
    #print(d_kord_ivl)
    #13,15
    rez1 = OchrVetv(l_vetvi,kompas=kompas,Trig=False)
    if rez1[0]!="":
        return (1,l_ind[rez1[1]],[2,3],rez1[0])
    #14
    for key in d_Yrovn:
        rez1 = OchrVetv(d_Yrovn[key],Trig=True)
        if rez1[0]!="":
            return (1,d_Yrovn2[key][rez1[1]],[2,3],rez1[0])


    #17
    if len(vvl)==0: 
        return (2,-1,-1,ex[16])

    sch_vvl=-1
    d_vvl = set()
    for i in range(len(vvl)):
        #18
        if i == 0 and vvl[i][0] == "Конфигурация опоры":
            return (2,i,9,ex[17])
        #19
        if i == len(vvl)-1 and vvl[i][0] != "Конфигурация опоры":
            return (2,i,9,ex[18])
        elif vvl[i][0] != "Конфигурация опоры" and vvl[i+1][0] != "Конфигурация опоры":
            return (2,i,9,ex[18])

        # Проверка строки ветви
        if vvl[i][0] != "Конфигурация опоры":
            # Название ветви
            if vvl[i][0] == "":
                return (2,i,[0,0],ex[3])
             
            # Первый узел
            rez = ColOp(vvl[i][1],Text=False,V=False)
            if rez[0] == "": n1 = rez[1]
            else: return(2,i,[1,1],rez[0])
                
            # Второй узел
            rez = ColOp(vvl[i][2],Text=False,V=False)
            if rez[0] == "": k1 = rez[1]
            else: return(2,i,[2,2],rez[0])

            # Номинальное напряжение
            rez = DlPQ(vvl[i][3],col=0,Mn=True)
            if rez != "": return(2,i,[3,3],rez)

            # Активная мощность
            rez = DlPQ(vvl[i][4],col=2,Mn=True,notNul=True)
            if rez != "": return(2,i,[4,4],rez)

            # Реактивная мощность
            rez = DlPQ(vvl[i][5],col=2,Mn=False)
            if rez != "": return(2,i,[5,5],rez)

            # Направление мощности
            rez = DlPQ(vvl[i][6],col=0,Mn=False)
            if rez != "": return(2,i,[6,6],rez)

            sch_vvl+=1
            d_vvl = set()

        else:
            # Первая опора
            rez = ColOp(vvl[i][1],Text=False,V=True,Otr=True)
            if rez[0] == "": 
                op1 = rez[1]
                n2 = rez[2]
            else: return(2,i,[1,1],rez[0])
              
            # Последняя опора
            rez = ColOp(vvl[i][2],Text=False,V=True,Otr=True)
            if rez[0] == "": 
                op2 = rez[1]
                k2 = rez[2]
            else: return(2,i,[2,2],rez[0])
            
            # Длинна участка
            rez = DlPQ(vvl[i][3],col=1,Mn=False)
            if rez != "": return(2,i,[3,3],rez)

            # Тип опоры
            if vvl[i][5] == "Не выбран":
                return(2,i,9,ex[6]+": Тип опоры")
            
            # Марка провода
            if vvl[i][6] == "Не выбран":
                return(2,i,9,ex[6]+": Марка провода")

            if n2=="" and k2=="":
                if (n1,k1) not in d_ych:
                    return(2,i,[1,2],ex[19])
                else:
                    if d_ych[(n1,k1)][0]<d_ych[(n1,k1)][1]:
                        if op1==op2 or op1>op2 or op1<d_ych[(n1,k1)][0] or op2>d_ych[(n1,k1)][1]:
                            return(2,i,[1,2],ex[20])
                    elif d_ych[(n1,k1)][0]>d_ych[(n1,k1)][1]:
                        if op1==op2 or op1<op2 or op1>d_ych[(n1,k1)][0] or op2<d_ych[(n1,k1)][1]:
                            return(2,i,[1,2],ex[20])

            elif n2!="" and k2!="":
                n2=abs(n2)
                k2=abs(k2)
                if (n2,k2) not in d_ych:
                    return(2,i,[1,2],ex[19])
                else:
                    if d_ych[(n2,k2)][0]<d_ych[(n2,k2)][1]:
                        if op1==op2 or op1>op2 or op1<d_ych[(n2,k2)][0] or op2>d_ych[(n2,k2)][1]:
                            return(2,i,[1,2],ex[20])
                    elif d_ych[(n2,k2)][0]>d_ych[(n2,k2)][1]:
                        if op1==op2 or op1<op2 or op1>d_ych[(n2,k2)][0] or op2<d_ych[(n2,k2)][1]:
                            return(2,i,[1,2],ex[20])
            else:
                return(2,i,[1,2],ex[5])

            n2 = n1 if n2=="" else n2
            k2 = k1 if k2=="" else k2

            if (n2,k2,op1,op2) not in d_vvl:
                for j in d_vvl:
                    if j[0:2]==(n2,k2):
                        if j[2]<j[3]:
                            if (op2>j[2] and j[3]>op1) or (j[3]>op1 and op2>j[2]):
                                return (2,i,[1,2],ex[27])
                        elif j[2]>j[3]:
                            if (op2<j[2] and j[3]<op1) or (j[3]<op1 and op2<j[2]):
                                return (2,i,[1,2],ex[27])
                d_vvl.add((n2,k2,op1,op2))
            else:
                return(2,i,9,ex[24])

            kord = rnn.VF(d_to[vvl[i][5]],1,'OpFig',Katalog,Kat)
            if vvl[i][7] != "Не выбран"  and kord[9]==0: #and kord[7]==0
                return(2,i,9,ex[28]+" №1")
            if vvl[i][8] != "Не выбран"  and kord[10]==0: #and kord[8]==0
                return(2,i,9,ex[28]+" №2")
            try:
                rez = Sblizh((n2,k2,op1,op2),list(kord)+vvl[i][5:9],d_kord_ivl,vvl[i][3])
                if rez!="": return (2,i,[1,2],rez)
            except Exception as error:
                print(error)
            
    d_zy = set()

    for i in range(len(zy)):
        # Первый узел
        rez = ColOp(zy[i][0],Text=False,V=False)
        if rez[0] == "": n3 = rez[1]
        else: return(3,i,[0,0],rez[0])
            
        # Второй узел
        rez = ColOp(zy[i][1],Text=False,V=False)
        if rez[0] == "": k3 = rez[1]
        else: return(3,i,[1,1],rez[0])

        # Опора
        rez = ColOp(zy[i][2],Text=False,V=False)
        if rez[0] == "": op = rez[1]
        else: return(3,i,[2,2],rez[0])

        # Сопротивление заземленичя
        rez = DlPQ(zy[i][3],col=0,Mn=True,notNul=True)
        if rez != "": return(3,i,[3,3],rez)

        # Тип заземления
        if zy[i][7].strip() == "":
            return(3,i,9,ex[6]+": Тип заземления")

        if (n3,k3) not in d_ych:
            return(3,i,[0,1],ex[19])
        else:
            if (n3,k3,op) not in d_zy and zy[i][4]!="Разземлен":
                if d_ych[(n3,k3)][0]<d_ych[(n3,k3)][1]:
                    if op>d_ych[(n3,k3)][1] or op<d_ych[(n3,k3)][0]:
                        return(3,i,[2,2],ex[23])
                    elif zy[i][7]=="ПЗ" and (op!=d_ych[(n3,k3)][0] and op!=d_ych[(n3,k3)][1]):
                        return(3,i,9,ex[22])
                elif d_ych[(n3,k3)][0]>d_ych[(n3,k3)][1]:
                    if op<d_ych[(n3,k3)][1] or op>d_ych[(n3,k3)][0]:
                        return(3,i,[2,2],ex[23])  
                    elif zy[i][7]=="ПЗ" and (op!=d_ych[(n3,k3)][0] and op!=d_ych[(n3,k3)][1]):
                        return(3,i,9,ex[22])
                d_zy.add((n3,k3,op))
            elif (n3,k3,op) in d_zy and zy[i][4]!="Разземлен":
                return(3,i,9,ex[21])

    d_zytr=set()

    for i in range(len(zytr)):
        # Первый узел
        rez = ColOp(zytr[i][0],Text=False,V=False)
        if rez[0] == "": n4 = rez[1]
        else: return(4,i,[0,0],rez[0])
            
        # Второй узел
        rez = ColOp(zytr[i][1],Text=False,V=False)
        if rez[0] == "": k4 = rez[1]
        else: return(4,i,[1,1],rez[0])

        # Первая опора
        rez = ColOp(zytr[i][2],Text=False,V=False)
        if rez[0] == "": op1 = rez[1]
        else: return(4,i,[2,2],rez[0])

        # Последняя опора
        rez = ColOp(zytr[i][3],Text=False,V=False)
        if rez[0] == "": op2 = rez[1]
        else: return(4,i,[3,3],rez[0])

        # Сопротивление заземленичя
        rez = DlPQ(zytr[i][4],col=0,Mn=True,notNul=True)
        if rez != "": return(4,i,[4,4],rez)


        if (n4,k4) not in d_ych:
            return(4,i,[0,1],ex[19])
        else:
            if d_ych[(n4,k4)][0]<d_ych[(n4,k4)][1]:
                if op1>op2 or op1<d_ych[(n4,k4)][0] or op2>d_ych[(n4,k4)][1]:
                    return(4,i,[2,3],ex[20])
            elif d_ych[(n4,k4)][0]>d_ych[(n4,k4)][1]:
                if  op1<op2 or op1>d_ych[(n4,k4)][0] or op2<d_ych[(n4,k4)][1]:
                    return(4,i,[2,3],ex[20])

        if (n4,k4,op1,op2) not in d_zytr:
            for j in d_zytr:
                if j[0:2]==(n4,k4):
                    if j[2]<j[3]:
                        if (op2>j[2] and j[3]>op1) or (j[3]>op1 and op2>j[2]) or (op1==op2 and (op1==j[2] or op1==j[3]) ):
                            return (4,i,[2,3],ex[27])
                    elif j[2]>j[3]:
                        if (op2<j[2] and j[3]<op1) or (j[3]<op1 and op2<j[2]) or (op1==op2 and (op1==j[2] or op1==j[3]) ):
                            return (4,i,[2,3],ex[27])
            d_zytr.add((n4,k4,op1,op2))
        else:
            return(4,i,9,ex[24])


    for i in range(len(zvl)):
        # Сопротивление заземленичя
        rez = DlPQ(zvl[i][0],col=0,Mn=True,notNul=True)
        if rez != "": return(5,i,[0,0],rez)

        # Длинна предыдущего участка
        rez = DlPQ(zvl[i][1],col=0,Mn=True)
        if rez != "": return(5,i,[1,1],rez)

        # Количество опор предыдущего участка
        rez = ColOp(zvl[i][2],Text=False,V=False)
        if rez[0] == "": op1 = rez[1]
        else: return(5,i,[2,2],rez[0])

        # Длинна последующего участка
        rez = DlPQ(zvl[i][3],col=0,Mn=True)
        if rez != "": return(5,i,[3,3],rez)

        # Количество опор последующего участка
        rez = ColOp(zvl[i][4],Text=False,V=False)
        if rez[0] == "": op2 = rez[1]
        else: return(5,i,[4,4],rez[0])
        

        if (op1!=0 and float(zvl[i][1])!=0) or (op2!=0 and float(zvl[i][3])!=0):
            # Тип опоры
            if zvl[i][6] == "Не выбран":
                return(5,i,9,ex[6]+": Тип опоры")
            # Марка троса №1
            if zvl[i][7] == "Не выбран":
                return(5,i,9,ex[6]+": Марка троса №1")

        elif (op1!=0 and float(zvl[i][1])==0) or (op1==0 and float(zvl[i][1])!=0):
            return(5,i,[1,2],ex[25])
        elif (op2!=0 and float(zvl[i][3])==0) or (op2==0 and float(zvl[i][3])!=0):
            return(5,i,[3,4],ex[25])

        if i>sch_vvl:
            return(5,i,9,ex[26])
    



    
    return None
                
