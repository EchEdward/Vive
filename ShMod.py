from PIL import Image, ImageDraw, ImageFont
Probel = 10
Probel_h = 4



def RazdYch(ivl, vvl, per, km, N_op, font_size,per_name):
    """ Функция для определения элементарных участков ветви,
     длин участков, растояний между ВЛ"""
    VVL=[]
    Hor_op = []
    for i in range(len(ivl)):
        VVL.append([])
        Hor_op.append(set())
        for j in vvl:
            for k in vvl[j]:
                if k[0] == ivl[i][0] and k[1] == ivl[i][1]:
                    k[6] = j
                    VVL[i].append(k)
                    if k[2] not in Hor_op[i]:
                        Hor_op[i].add(k[2])
                    if k[3] not in Hor_op[i]:
                        Hor_op[i].add(k[3])
    
    for i in range(len(Hor_op)):
        if ivl[i][4] < ivl[i][5]:
            Hor_op[i] = sorted(Hor_op[i])
        elif ivl[i][4] > ivl[i][5]:
            Hor_op[i] = sorted(Hor_op[i], reverse = True)

    image = Image.new('RGB',(1000,1000), 'white')
    draw = ImageDraw.Draw(image)
    Ar = ImageFont.truetype ( 'Fonts/arial.ttf', font_size)

    Razm_dlin = []
    x,y = 0,0
    for i in range(len(ivl)):
        Razm_dlin.append({})
        for j in range(len(Hor_op[i])-1):
            if j == 0 and Hor_op[i][j] != ivl[i][4]:
                dl = round(abs(km[i][per[i].index(ivl[i][4])] - km[i][per[i].index(Hor_op[i][j])]),3)
                (x,y) = draw.textsize(str(dl), font=Ar)
                Razm_dlin[i][(ivl[i][4],Hor_op[i][j])] = [dl,x]
                    
            dl = round(abs(km[i][per[i].index(Hor_op[i][j])] - km[i][per[i].index(Hor_op[i][j+1])]),3)
            (x,y) = draw.textsize(str(dl), font=Ar)
            Razm_dlin[i][(Hor_op[i][j],Hor_op[i][j+1])] = [dl,x]
                
            
            if j == len(Hor_op[i])-2 and Hor_op[i][j+1] != ivl[i][5]:
                dl = round(abs(km[i][per[i].index(ivl[i][5])] - km[i][per[i].index(Hor_op[i][j+1])]),3)
                (x,y) = draw.textsize(str(dl), font=Ar)
                Razm_dlin[i][(Hor_op[i][j+1],ivl[i][5])] = [dl,x]

        if  len(Hor_op[i])-1<=0:
            dl = round(abs(km[i][per[i].index(ivl[i][4])] - km[i][per[i].index(ivl[i][5])]),3)
            (x,y) = draw.textsize(str(dl), font=Ar)
            Razm_dlin[i][(ivl[i][4],ivl[i][5])] = [dl,x]                 

    VVL_ych = []

    line_left = {}
    line_right = {}
    line_X = {}
    sp = [line_left,line_right,line_X]
    ych_sb = [list(i.keys()) for i in Razm_dlin]
    for i in range(len(ivl)):
        VVL_ych.append([])
        for j in range(len(ych_sb[i])):
            VVL_ych[i].append([[],[],[]])
            c = [-1, -1, -1]
            for k in range(len(VVL[i])):
                if ych_sb[i][j][0] >= VVL[i][k][2] and ych_sb[i][j][1] <= VVL[i][k][3] and ivl[i][4] < ivl[i][5] or\
                   ych_sb[i][j][0] <= VVL[i][k][2] and ych_sb[i][j][1] >= VVL[i][k][3] and ivl[i][4] > ivl[i][5]:
                    d_l=0
                    #d_l0=0
                    if VVL[i][k][4] <= 0 and VVL[i][k][5] <= 0:
                        a = 0
                        c[0]+=1
                    elif VVL[i][k][4] > 0 and VVL[i][k][5] > 0:
                        a = 1
                        c[1]+=1
                    else:
                        a = 2
                        c[2]+=1
                    if VVL[i][k][2] < VVL[i][k][3]:
                        for o in ych_sb[i]:
                            if o[0] >= VVL[i][k][2] and o[1] <= VVL[i][k][3]:
                                if o == ych_sb[i][j]: d_l0 = d_l
                                d_l+=Razm_dlin[i][o][0]

                    elif VVL[i][k][2] > VVL[i][k][3]:
                        for o in ych_sb[i]:
                            if o[0] <= VVL[i][k][2] and o[1] >= VVL[i][k][3]:
                                if o == ych_sb[i][j]: d_l0 = d_l
                                d_l+=Razm_dlin[i][o][0]
                    f1 = VVL[i][k][4]
                    f2 = VVL[i][k][5]
                    x = Razm_dlin[i][ych_sb[i][j]][0]
                    if f1<f2:
                        ft1 = f1+(f2-f1)*d_l0/d_l
                        ft2 = f1+(f2-f1)*(d_l0+x)/d_l
                    elif f1>f2:
                        ft1 = f1-(f1-f2)*d_l0/d_l
                        ft2 = f1-(f1-f2)*(d_l0+x)/d_l
                    else:
                        ft1 = f1
                        ft2 = f2
                    
                    VVL_ych[i][j][a].append([VVL[i][k][0],
                                             VVL[i][k][1],
                                             ych_sb[i][j][0],
                                             ych_sb[i][j][1],
                                             ft1,
                                             ft2,
                                             VVL[i][k][6]])
                    if VVL[i][k][6] not in sp[a]:
                        sp[a][VVL[i][k][6]] = [[VVL[i][k][0],
                                                VVL[i][k][1],
                                                ych_sb[i][j][0],
                                                ych_sb[i][j][1],
                                                (i,j,a,c[a])]]
                    else:
                        sp[a][VVL[i][k][6]].append([VVL[i][k][0],
                                                    VVL[i][k][1],
                                                    ych_sb[i][j][0],
                                                    ych_sb[i][j][1],
                                                    (i,j,a,c[a])])

    #print(VVL_ych)
    #print(line_left)
    K_dict = {'С':'Ю','С-В':'Ю-З','В':'3','Ю-В':'С-З','Ю':'С','Ю-З':'С-В','З':'В','С-З':'Ю-В'}
    Check_list = [True for i in ivl]
    Posled_Ych =[]
    k = -1
    for i in range(len(ivl)):
        if Check_list[i]:
            Posled_Ych.append([[ivl[i][0],ivl[i][1],i]])
            k+=1
            Check_list[i] = False
            a,b,c = ivl[i][0],ivl[i][1],ivl[i][3]
            for j in range(len(ivl)):
                if Check_list[j] and ((b == ivl[j][0] and c == ivl[j][3]) or\
                   (a == ivl[j][0] and K_dict[c] == ivl[j][3])):
                    Posled_Ych[k].append([ivl[j][0],ivl[j][1],j])
                    Check_list[j] = False
                    a,b,c = ivl[j][0],ivl[j][1],ivl[j][3]
    

    Posled_list =[]
    for i in range(len(Posled_Ych)):
        Posled_list.append([])
        for j in range(len(Posled_Ych[i])):
            for k in range(len(ych_sb[Posled_Ych[i][j][2]])):
                Posled_list[i].append([Posled_Ych[i][j][0],
                                       Posled_Ych[i][j][1],
                                       ych_sb[Posled_Ych[i][j][2]][k][0],
                                       ych_sb[Posled_Ych[i][j][2]][k][1]])

    #print(Posled_Ych)
    def Line_Posled(line,Posled_list):
        line_posled = []
        d_lin = {}
        c = -1
        for key in line:
            Check_list = [True for i in line[key]]
            for i in range(len(line[key])):
                if Check_list[i]:
                    Check_list[i] = False
                    c+=1
                    line_posled.append(c)
                    d_lin[line[key][i][4]] = c
                    Trig = False
                    for j in range(len(Posled_list)):
                        for k in range(len(Posled_list[j])):
                            if line[key][i][:4] == Posled_list[j][k][:4]:
                                a,b = j,k
                                Trig = True
                                break
                        if Trig: break
                    d = 0
                    for j in range(i+1,len(line[key])):
                        d+=1
                        if b+d >= len(Posled_list[a]): break
                        if line[key][j][:4] == Posled_list[a][b+d][:4] and Check_list[j]:
                            Check_list[j] = False
                            d_lin[line[key][j][4]] = c
                            
        return line_posled, d_lin

    
    line_posled0, d_lin0 = Line_Posled(line_left,Posled_list)
    line_posled1, d_lin1 = Line_Posled(line_right,Posled_list)
    line_posled2, d_lin2 = Line_Posled(line_X,Posled_list)

    #print(line_posled0)
    #print("*"*5)
    #print(d_lin0)
    #print("*"*5)

    def SearchPosition(line_posled,d_lin,a):
        Yr_ind = [0 for i in line_posled]
        Sort_index = []
        for i in range(len(VVL_ych)):
            Sort_index.append([])
            for j in range(len(VVL_ych[i])):
                Sort_index[i].append([[],[],[]])
                c = 0
                Check_list = [True for i in VVL_ych[i][j][a]]
                while True:
                    n, m = float('inf'), float('inf')
                    c+=1
                    Trig = False
                    k_s = -1
                    for k in range(len(VVL_ych[i][j][a])):
                        if abs(VVL_ych[i][j][a][k][4]) <= m and abs(VVL_ych[i][j][a][k][5]) <= n and Check_list[k]:
                            m = abs(VVL_ych[i][j][a][k][4])
                            n = abs(VVL_ych[i][j][a][k][5])
                            Trig = True
                            k_s=k        
                    if Trig:
                        Check_list[k_s] = False
                        Sort_index[i][j][a].append([c,k_s])
                        if Yr_ind[d_lin[(i,j,a,k_s)]] < c:
                            Yr_ind[d_lin[(i,j,a,k_s)]] = c
                    else:
                        break
        return Sort_index, Yr_ind

    Sort_index0, Yr_ind0 = SearchPosition(line_posled0,d_lin0,0)
    Sort_index1, Yr_ind1 = SearchPosition(line_posled1,d_lin1,1)
    #Sp_dl = [d_lin0,d_lin1]
    
    #print("*"*5)
    #print(Yr_ind0)
    #print("*"*5)
    VVL_sort = []
    def SetLinePosition(Sort_index,Yr_ind,d_lin,a,key=False):
        for i in range(len(Sort_index)):
            if key: VVL_sort.append([])
            for j in range(len(Sort_index[i])):
                if key: VVL_sort[i].append([[],[],[]])
                t=1
                for k in range(len(Sort_index[i][j][a])):
                    ind = Sort_index[i][j][a][k][1]
                    #c = Sort_index[i][j][a][k][0]
                    mn_yr = Yr_ind[d_lin[(i,j,a,ind)]]
                    if t < mn_yr:
                        for n in range(t,mn_yr):
                            VVL_sort[i][j][a].append([])
                        t = n+1
                    VVL_sort[i][j][a].append(VVL_ych[i][j][a][ind]+[d_lin[(i,j,a,ind)]])

                    t+=1
    
    SetLinePosition(Sort_index0,Yr_ind0,d_lin0,0,key=True)
    SetLinePosition(Sort_index1,Yr_ind1,d_lin1,1)

    #print("*"*5)
    #draw.line([10,10,20,20] ,fill="black", width=1)

    Line_width = []
    Min_len =[]
    Probel = 2
    per_key = list(per_name.keys())
    for i in range(len(VVL_sort)):
        Line_width.append([])
        Min_len.append([])
        for j in range(len(VVL_sort[i])):
            x5,x6,x7, y = 0, 0, 0, 0
            left, right, center = 0,0,0
            Line_width[i].append([[],[],[]])
            for a in range(len(VVL_sort[i][j])):
                point, f1, f2 = 0,0,0
                l, r, c = 0,0,0
                x0,x1,x2,x3,x4 = 0,0,0,0,0
                for k in range(len(VVL_sort[i][j][a])):
                    if len(VVL_sort[i][j][a][k]) != 0:
                        N = abs(VVL_sort[i][j][a][k][4] - f1)
                        K = abs(VVL_sort[i][j][a][k][5] - f2)
                        (x0,y)=draw.textsize(str(VVL_sort[i][j][a][k][6]), font=Ar)
                        (x1,y)=draw.textsize(str(per_name[per_key[i]].get(VVL_sort[i][j][a][k][2],VVL_sort[i][j][a][k][2])), font=Ar)
                        (x2,y)=draw.textsize(str(per_name[per_key[i]].get(VVL_sort[i][j][a][k][3],VVL_sort[i][j][a][k][3])), font=Ar)
                        #print("x1+"+str(VVL_sort[i][j][a][k][2]))
                        #print("x2+"+str(VVL_sort[i][j][a][k][3]))
                        c = int((x1+x2)/2) + 2*Probel
                        l = int(x1/2)
                        r = int(x2/2)
                        if N < 1 and K < 1:
                            Line_width[i][j][a].append([point,k+1,[0],[0],x0])
                            point = k+1
                            f1 = VVL_sort[i][j][a][k][4]
                            f2 = VVL_sort[i][j][a][k][5]
                        elif N == K and f1 == f2:
                            (x3,y)=draw.textsize(str(round(N,1)), font=Ar)
                            Line_width[i][j][a].append([point,k+1,[round(N,1)],[x3],x0])
                            point = k+1
                            f1 = VVL_sort[i][j][a][k][4]
                            f2 = VVL_sort[i][j][a][k][5]
                            c += x3+Probel
                        elif (N != K and f1 == f2) or (N != K and f1 != f2):
                            (x3,y)=draw.textsize(str(round(N,1)), font=Ar)
                            (x4,y)=draw.textsize(str(round(K,1)), font=Ar)
                            Line_width[i][j][a].append([point,k+1,[round(N,1),round(K,1)],[x3,x4],x0])
                            point = k+1
                            f1 = VVL_sort[i][j][a][k][4]
                            f2 = VVL_sort[i][j][a][k][5]
                            c += x3+x4+Probel*2
                        elif N == K and f1 != f2:
                            (x3,y)=draw.textsize(str(round(N,1)), font=Ar)
                            Line_width[i][j][a].append([point,k+1,[round(N,1),0],[x3,0],x0])
                            point = k+1
                            f1 = VVL_sort[i][j][a][k][4]
                            f2 = VVL_sort[i][j][a][k][5]
                            c += x3+Probel
                    else:
                        Line_width[i][j][a].append([])
                    left = l if l>left else left
                    right = r if r>right else right
                    center = c if c>center else center
            x5 = Razm_dlin[i][ych_sb[i][j]][1]
            #(x6,y) = draw.textsize(str(ych_sb[i][j][0]), font=Ar)
            #(x7,y) = draw.textsize(str(ych_sb[i][j][1]), font=Ar)
            (x6,y) = draw.textsize(str(per_name[per_key[i]].get(ych_sb[i][j][0],ych_sb[i][j][0])), font=Ar)
            (x7,y) = draw.textsize(str(per_name[per_key[i]].get(ych_sb[i][j][1],ych_sb[i][j][1])), font=Ar)
            #print("x6+"+str(ych_sb[i][j][0]))
            #print("x7+"+str(ych_sb[i][j][1]))
            left = int(x6/2) if x6/2>left else left
            right = int(x7/2) if x7/2>right else right
            center = max(x5+Probel,int(x6/2+x6/2+Probel)) if max(x5+Probel,int(x6/2+x6/2+Probel))>center else center
            Min_len[i].append([left,center,right])    
    
    PS = []
    for i in range(len(ivl)):
        try: (x1,y1) = draw.textsize(ivl[i][8], font=Ar)
        except Exception: x1,y1=0,0
        try: (x2,y2) = draw.textsize(ivl[i][10], font=Ar)
        except Exception: x2,y2=0,0
        PS.append([x1,y1,x2,y2])

    for i in N_op:
        if N_op[i] !=None:
            (x1,y1) = draw.textsize(N_op[i], font=Ar)
            N_op[i] = [N_op[i],(x1,y1)]


        
    return VVL_sort,Line_width,Min_len,Razm_dlin,ych_sb, y,PS,N_op

def Vetvi_Ris(ivl,VVL_sort, Line_width, Min_len, Razm_dlin, ych_sb, text_height,font_size,PS,podp,per_name,size=0):
    """ Рисуем ветвь, определяем её размеры """
    Text_kord =[]
    Line_kord = []
    x,y = 0, 0
    y_min, y_max = 0,0
    if ivl[3]=='В' or  ivl[3]=='С' or ivl[3]=='С-В' or ivl[3]=='Ю-В':
        napr = 1
    else:
        napr = -1
    Name_vl = set()
    ps1 = 0
    ps2 = 0

    dl = 0
    Per_Check = []
    for i in range(len(ych_sb)):
        Trig = int((1-napr)/2)
        if (i == 0 and ivl[8] != '') or (podp[0] and i == 0):
            if i == 0 and ivl[8] != '':
                x = PS[1]*napr
                ps1=[0,x,int(PS[0]/2)]
                y_min = -int(PS[0]/2) if -int(PS[0]/2)<y_min else y_min
                y_max = int(PS[0]/2) if int(PS[0]/2)>y_max else y_max
            xn = x + (Min_len[i][0]+ int(Probel/2))*napr
            xt = x + int(Probel/2)*napr - int(Trig*Min_len[i][0]*2)
            yt = y - text_height - Probel_h 
            y_min = yt if yt<y_min else y_min
            Line_kord.append([[x,y,xn,y],3])
            Text_kord.append([[xt,yt],str(per_name.get(ych_sb[i][0],ych_sb[i][0]))])
            #print(ych_sb[i][0])
            if i == 0 and ivl[8] != '':
                Line_kord.append([[x,0,x,-text_height-Probel_h],3])
                Line_kord.append([[x,0,x,text_height+Probel_h],3])
            x = xn

        xn = x + (Min_len[i][1]+ int(Razm_dlin[ych_sb[i]][0]*size))*napr
        xt = xn - Min_len[i][2] 
        yt = y - text_height - Probel_h
        y_min = yt if yt<y_min else y_min
        Line_kord.append([[x,y,xn,y],3])
        if not (i == len(ych_sb)-1 and ivl[10] == ''):
            Text_kord.append([[xt,yt],str(per_name.get(ych_sb[i][1],ych_sb[i][1]))])

        if i == len(ych_sb)-1 and podp[1] and ivl[10] == '':
            Text_kord.append([[xt,yt],str(per_name.get(ych_sb[i][1],ych_sb[i][1]))])
        #print(ych_sb[i][1])
        yr = y + text_height + Probel_h
        y_max = yr if yr>y_max else y_max
        Line_kord.append([[x,yr,xn,yr],1])
        Line_kord.append([[x,y,x,yr],1])
        Line_kord.append([[xn,y,xn,yr],1])

        xt = x + int((xn-x)/2 -Razm_dlin[ych_sb[i]][1]/2)
        Text_kord.append([[xt,y+1],str(Razm_dlin[ych_sb[i]][0])])

        for j in Arrow(x,yr,'left',napr):
            Line_kord.append(j)
        for j in Arrow(xn,yr,'right',napr):
            Line_kord.append(j)

        y_pc1 = Probel_h+text_height
        y_pc2 = Probel_h+text_height
        for m in [0,1]:
            a1 = 1 if m==0 else -1
            a2 = -1 if m==1 else 0
            h = text_height*2+Probel_h*2
            HV = [-a1*napr * h*i for i in range(len(Line_width[i][m])+1)]
            
            if m==0 and len(HV)>0:
                y_pc1+=abs(HV[len(HV)-1])
            if m==1 and len(HV)>0:
                y_pc2+=abs(HV[len(HV)-1])
            for j in range(len(Line_width[i][m])):
                if len(Line_width[i][m][j]) != 0:
                    p1 = Line_width[i][m][j][1]
                    p0 = Line_width[i][m][j][0]
                    Line_kord.append([[x,HV[p1],xn,HV[p1]],3])
                    if napr*a1>0:
                        y_min = HV[p1]-Probel_h-text_height if HV[p1]-Probel_h-text_height<y_min else y_min
                    else:
                        HV[0] = yr 
                        y_max = HV[p1]+Probel_h+text_height if HV[p1]+Probel_h+text_height>y_max else y_max

                    #if True: #(VVL_sort[i][m][j][7],m) not in Name_vl
                        #Text_kord.append([[x-Trig*Line_width[i][m][j][4],HV[p1]-Probel_h*napr*a1-text_height*(1-(a1*Trig-a2))],str(VVL_sort[i][m][j][6])])
                        #Name_vl.add((VVL_sort[i][m][j][7],m))
                    if (VVL_sort[i][m][j][6],m,j,ych_sb[i][0],ych_sb[i][1]) not in Name_vl:
                        if i!=0:
                            if (VVL_sort[i][m][j][6],m,j,ych_sb[i-1][0],ych_sb[i-1][1]) not in Name_vl: 
                                Text_kord.append([[x-Trig*Line_width[i][m][j][4],HV[p1]-Probel_h*napr*a1-text_height*(1-(a1*Trig-a2))],str(VVL_sort[i][m][j][6])])
                                Name_vl.add((VVL_sort[i][m][j][6],m,j,ych_sb[i][0],ych_sb[i][1]))
                            else:
                                Name_vl.add((VVL_sort[i][m][j][6],m,j,ych_sb[i][0],ych_sb[i][1]))
                        else:
                            Text_kord.append([[x-Trig*Line_width[i][m][j][4],HV[p1]-Probel_h*napr*a1-text_height*(1-(a1*Trig-a2))],str(VVL_sort[i][m][j][6])])
                            Name_vl.add((VVL_sort[i][m][j][6],m,j,ych_sb[i][0],ych_sb[i][1]))
        
                    if j+1 == len(Line_width[i][m]):
                        Line_kord.append([[x,HV[0]-(text_height+Probel_h)*(1-(a1*Trig-a2)),x,HV[p1]],1])
                        Line_kord.append([[xn,HV[0]-(text_height+Probel_h)*(1-(a1*Trig-a2)),xn,HV[p1]],1])

                    if i == 0 and ivl[8] != '':
                        Line_kord.append([[x-(Min_len[i][0]+ int(Probel/2))*napr,HV[p1],x,HV[p1]],3])
                        if len(Line_width[i][m]) - 1 == j:
                            Line_kord.append([[x-(Min_len[i][0]+ int(Probel/2))*napr,HV[p1]-text_height*napr*a1,x-(Min_len[i][0]+ int(Probel/2))*napr,HV[0]-yr*(a1*Trig-a2)],3])

                    if i == len(ych_sb)-1 and ivl[10] != '':
                        Line_kord.append([[xn,HV[p1],xn+(Min_len[i][2]+ int(Probel/2))*napr,HV[p1]],3])
                        if len(Line_width[i][m]) - 1 == j:
                            Line_kord.append([[xn+(Min_len[i][2]+ int(Probel/2))*napr,HV[p1]-text_height*napr*a1,xn+(Min_len[i][2]+ int(Probel/2))*napr,HV[0]-yr*(a1*Trig-a2)],3])

                    if len(Line_width[i][m][j][2])==1:
                        if Line_width[i][m][j][2][0] !=0:
                            xt = x + int((xn-x)/2 - Line_width[i][m][j][3][0]/2)
                            xl1 = x + int((xn-x)/2)
                            yt = HV[(p1-p0)//2+1+p0]
                            Text_kord.append([[xt,yt+Probel_h*napr*a1-text_height*(a1*Trig-a2)],str(Line_width[i][m][j][2][0])])
                            
                            Line_kord.append([[xl1,HV[p1],xl1,yt+Probel_h*napr*a1],1])
                            Line_kord.append([[xl1,yt+text_height*napr*a1+Probel_h*napr*a1,xl1,HV[p0]],1])

                            for j in Arrow(xl1,HV[p1],'top',napr*a1):
                                Line_kord.append(j)
                            for j in Arrow(xl1,HV[p0],'botton',napr*a1):
                                Line_kord.append(j)
                        else:
                            if napr>0:
                                for k in range(x+max(Min_len[i][0],Line_width[i][m][j][4]),xn-Min_len[i][2],10):
                                    Line_kord.append([[k,HV[p1],k,HV[p0]],1])
                            else:
                                for k in range(xn+Min_len[i][2],x-max(Min_len[i][0],Line_width[i][m][j][4]),10):
                                    Line_kord.append([[k,HV[p1],k,HV[p0]],1])
                    elif len(Line_width[i][m][j][2])==2:
                        if Line_width[i][m][j][2][1] !=0:
                            ts1 = max(Min_len[i][0],Line_width[i][m][j][4])
                            ts2 = Min_len[i][2]
                            if Line_width[i][m][j][3][0]/2<ts1:
                                xt1 = x+(ts1-int(Line_width[i][m][j][3][0]/2))*napr-Trig*Line_width[i][m][j][3][0]
                            else:
                                xt1 =x - Trig*Line_width[i][m][j][3][0]
                            xl1 = xt1+int(Line_width[i][m][j][3][0]/2)
                            if Line_width[i][m][j][3][1]/2<ts2:
                                xt2 = xn - ts2*napr - int(Line_width[i][m][j][3][1]/2)
                            else:
                                xt2 = xn - Line_width[i][m][j][3][1]*(1-Trig)
                            xl2 = xt2 + int(Line_width[i][m][j][3][1]/2)
                            
                            yt = HV[(p1-p0)//2+1+p0]
                            Text_kord.append([[xt1,yt+Probel_h*napr*a1-text_height*(a1*Trig-a2)],str(Line_width[i][m][j][2][0])])
                            Text_kord.append([[xt2,yt+Probel_h*napr*a1-text_height*(a1*Trig-a2)],str(Line_width[i][m][j][2][1])])
                            Line_kord.append([[xl1,HV[p1],xl1,yt+Probel_h*napr*a1],1])
                            Line_kord.append([[xl1,yt+text_height*napr*a1+Probel_h*napr*a1,xl1,HV[p0]],1])
                            Line_kord.append([[xl2,HV[p1],xl2,yt+Probel_h*napr*a1],1])
                            Line_kord.append([[xl2,yt+text_height*napr*a1+Probel_h*napr*a1,xl2,HV[p0]],1])

                            for j in Arrow(xl1,HV[p1],'top',napr*a1):
                                Line_kord.append(j)
                            for j in Arrow(xl1,HV[p0],'botton',napr*a1):
                                Line_kord.append(j) 
                            for j in Arrow(xl2,HV[p1],'top',napr*a1):
                                Line_kord.append(j)
                            for j in Arrow(xl2,HV[p0],'botton',napr*a1):
                                Line_kord.append(j)
                        else:
                            ts1 = max(Min_len[i][0],Line_width[i][m][j][4])                       
                            if Line_width[i][m][j][3][0]/2<ts1:
                                xt1 = x+(ts1-int(Line_width[i][m][j][3][0]/2))*napr-Trig*Line_width[i][m][j][3][0]
                            else:
                                xt1 =x - Trig*Line_width[i][m][j][3][0]
                            xl1 = xt1+int(Line_width[i][m][j][3][0]/2)
                            yt = HV[(p1-p0)//2+1+p0]
                            Text_kord.append([[xt1,yt+Probel_h*napr*a1-text_height*(a1*Trig-a2)],str(Line_width[i][m][j][2][0])])
                            Line_kord.append([[xl1,HV[p1],xl1,yt+Probel_h*napr*a1],1])
                            Line_kord.append([[xl1,yt+text_height*napr*a1+Probel_h*napr*a1,xl1,HV[p0]],1])
                            for j in Arrow(xl1,HV[p1],'top',napr*a1):
                                Line_kord.append(j)
                            for j in Arrow(xl1,HV[p0],'botton',napr*a1):
                                Line_kord.append(j)

        if i == 0 and ivl[8] != '':
            Per_Check.append([0,xn,max(y_pc1+2,ps1[2]+2),max(y_pc2+2,ps1[2]+2),dl,Razm_dlin[ych_sb[i]][0]])
        elif podp[0] and i == 0:
            Per_Check.append([0,xn,y_pc1+2,y_pc2+2,dl,Razm_dlin[ych_sb[i]][0]])

        if not (i == len(ych_sb)-1 and ivl[10] != '') and not (i == 0 and ivl[8] != ''):
            Per_Check.append([x,xn,y_pc1+2,y_pc2+2,dl,Razm_dlin[ych_sb[i]][0]])
        endgr = x        
        x=xn

        if (i == len(ych_sb)-1 and ivl[10] != '') or (podp[1] and i == len(ych_sb)-1):
            xn = x + (Min_len[i][2]+ int(Probel/2))*napr 
            Line_kord.append([[x,y,xn,y],3])
            x=xn
            if podp[1] and not (i == len(ych_sb)-1 and ivl[10] != ''):
                Per_Check.append([endgr,xn,y_pc1+2,y_pc2+2,dl,Razm_dlin[ych_sb[i]][0]])
            if (i == len(ych_sb)-1 and ivl[10] != ''):
                Line_kord.append([[xn,0,xn,-text_height-Probel_h],3])
                Line_kord.append([[xn,0,xn,text_height+Probel_h],3])
                xn = x + PS[3]*napr
                ps2=[x,xn,int(PS[2]/2)]
                y_min = -int(PS[2]/2) if -int(PS[2]/2)<y_min else y_min
                y_max = int(PS[2]/2) if int(PS[2]/2)>y_max else y_max
                x=xn
                Per_Check.append([endgr,xn,max(y_pc1+2,ps2[2]+2),max(y_pc2+2,ps2[2]+2),dl,Razm_dlin[ych_sb[i]][0]])

        dl+=Razm_dlin[ych_sb[i]][0]

    y_max+=2
    y_min-=2
    x = x+1 if x>0 else x-1
    image = Image.new('RGBA',(abs(x),abs(y_min)+y_max), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    Ar = ImageFont.truetype ( 'Fonts/arial.ttf', font_size)

    if ps1 != 0:
        Ips = Image.new('RGBA',(PS[0],PS[1]), (0,0,0,0))
        dr = ImageDraw.Draw(Ips)
        dr.text((0,0),ivl[8], fill="black", font=Ar)
        if ivl[3]=="В":
            Ips=Ips.transpose(Image.ROTATE_90)
            image.paste(Ips.convert('RGB'), (-2,abs(y_min)-ps1[2]), Ips)
        elif ivl[3]=="З":
            Ips=Ips.transpose(Image.ROTATE_90)
            image.paste(Ips.convert('RGB'), (abs(x)+ps1[1],abs(y_min)-ps1[2]), Ips)
        elif ivl[3]=="С":
            Ips=Ips.transpose(Image.ROTATE_270)
            image.paste(Ips.convert('RGB'), (0,abs(y_min)-ps1[2]), Ips)
        elif ivl[3]=="Ю":
            Ips=Ips.transpose(Image.ROTATE_270)
            image.paste(Ips.convert('RGB'), (abs(x)+ps1[1]+2,abs(y_min)-ps1[2]), Ips)

    if ps2 != 0:
        Ips = Image.new('RGBA',(PS[2],PS[3]), (0,0,0,0))
        dr = ImageDraw.Draw(Ips)
        dr.text((0,0),ivl[10], fill="black", font=Ar)
        if ivl[3]=="В":
            Ips=Ips.transpose(Image.ROTATE_90)
            image.paste(Ips.convert('RGB'), (ps2[0]+1,abs(y_min)-ps2[2]), Ips)
        elif ivl[3]=="З":
            Ips=Ips.transpose(Image.ROTATE_90)
            image.paste(Ips.convert('RGB'), (abs(x)+ps2[1]-3,abs(y_min)-ps2[2]), Ips)
        elif ivl[3]=="С":
            Ips=Ips.transpose(Image.ROTATE_270)
            image.paste(Ips.convert('RGB'), (ps2[0]+3,abs(y_min)-ps2[2]), Ips)
        elif ivl[3]=="Ю":
            Ips=Ips.transpose(Image.ROTATE_270)
            image.paste(Ips.convert('RGB'), (abs(x)+ps2[1]-1,abs(y_min)-ps2[2]), Ips)

    
    for i in Text_kord:
        if x<0: i[0][0]+=abs(x)
        i[0][1]+=abs(y_min)
        draw.text(i[0], i[1], fill="black", font=Ar)
        
    
    for i in Line_kord:
        if x<0: i[0][0]+=abs(x+1)
        i[0][1]+=abs(y_min)
        if x<0: i[0][2]+=abs(x+1)
        i[0][3]+=abs(y_min)
        draw.line(i[0] ,fill="black", width=i[1])
        
    
    del draw
    
    #image.save('test.png')
    

    return [0,x,y_min,y_max],Per_Check,dl, image

def Arrow(x,y,position,napr):
    """ Функция для рисования стрелочек размеров """
    d=4
    h=2
    if position =="left":
        l = [[[x,y,x+d*napr,y-h],1],[[x,y,x+d*napr,y+h],1]]
    if position == "right":
        l = [[[x,y,x-d*napr,y-h],1],[[x,y,x-d*napr,y+h],1]]
    if position == "top":
        l = [[[x,y,x-h,y+d*napr],1],[[x,y,x+h,y+d*napr],1]]
    if position == "botton":
        l = [[[x,y,x-h,y-d*napr],1],[[x,y,x+h,y-d*napr],1]]
    return l 

def Yzl(ivl):
    """ Определяем какие узлы к каким ветвям относятся """
    d = {}
    for i in range(len(ivl)):
        if ivl[i][0] not in d:
            d[ivl[i][0]]=[i]
        else: d[ivl[i][0]].append(i)
        if ivl[i][1] not in d:
            d[ivl[i][1]]=[i]
        else: d[ivl[i][1]].append(i)
    return d

def Rasp(ivl,d_y,xy,Per_Check,N_op):
    """ Функция маштабирования узла """

    D_Otv = {}
    for k in d_y:
        Otv = []
        if len(d_y[k]) > 1:
            for i in range(len(d_y[k])):
                if ivl[d_y[k][i]][1] == k:
                    if ivl[d_y[k][i]][3] == "В":
                        Otv.append([-10,'x-',-1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "З":
                        Otv.append([10,'x+',-1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "С":
                        Otv.append([+10,'y+',-1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "Ю":
                        Otv.append([-10,'y-',-1,d_y[k][i]])
                elif ivl[d_y[k][i]][0] == k:
                    if ivl[d_y[k][i]][3] == "В":
                        Otv.append([10,'x+',1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "З":
                        Otv.append([-10,'x-',1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "С":
                        Otv.append([-10,'y-',1,d_y[k][i]])
                    elif ivl[d_y[k][i]][3] == "Ю":
                        Otv.append([10,'y+',1,d_y[k][i]])
            pars={"x-":"x+","x+":"x-","y-":"y+","y+":"y-",}
            #Будем искать минимальный неконфликтный радиус
            rez = 1
            ln = 0

            while rez > 0 and ln<1000:
                ln+=1
                d_rez = {}
                rez = 0
                rez_name = None
                
                for i in range(len(Otv)):
                    rez = 0

                    for j in range(len(Otv)):
                        if i==j or Otv[i][1] == pars[Otv[j][1]]: continue
    
                        if Otv[i][2]==-1: 
                            r1 = (-1,-len(Per_Check[Otv[i][3]])-1,-1)
                        else:
                            r1 = (0,len(Per_Check[Otv[i][3]]),1)
                        if Otv[j][2]==-1: 
                            r2 = (-1,-len(Per_Check[Otv[j][3]])-1,-1)
                        else:
                            r2 = (0,len(Per_Check[Otv[j][3]]),1)

                        x1 = Otv[i][0]
                         
                        for m in range(r1[0],r1[1],r1[2]):
                            d1 = abs(Per_Check[Otv[i][3]][m][0]-Per_Check[Otv[i][3]][m][1])
                            #x1_n= x1+d1 if x1>0 else x1-d1
                            x2 = Otv[j][0]
                            for n in range(r2[0],r2[1],r2[2]):
                                d2 = abs(Per_Check[Otv[j][3]][n][0]-Per_Check[Otv[j][3]][n][1])
                                #x2_n= x2+d2 if x2>0 else x2-d2
                                if Otv[i][1] == "x-":
                                    rez_name = "x-"
                                    if Otv[j][1] == "y-":
                                        if x1>-abs(Per_Check[Otv[j][3]][n][2]) and x2>-abs(Per_Check[Otv[i][3]][m][2]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][2]))
                                            if rez>0: break
                                    elif Otv[j][1] == "y+":
                                        if x1>-abs(Per_Check[Otv[j][3]][n][3]) and x2<abs(Per_Check[Otv[i][3]][m][3]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][3]))
                                            if rez>0: break
                                elif Otv[i][1] == "x+":
                                    rez_name = "x+"
                                    if Otv[j][1] == "y-":
                                        if x1<abs(Per_Check[Otv[j][3]][n][3]) and x2>-abs(Per_Check[Otv[i][3]][m][2]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][3]))
                                            if rez>0: break
                                    elif Otv[j][1] == "y+":
                                        if x1<abs(Per_Check[Otv[j][3]][n][2]) and x2<abs(Per_Check[Otv[i][3]][m][3]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][2]))
                                            if rez>0: break
                                elif Otv[i][1] == 'y-':
                                    rez_name = 'y-'
                                    if Otv[j][1] == "x-":
                                        if x1>-abs(Per_Check[Otv[j][3]][n][2]) and x2>-abs(Per_Check[Otv[i][3]][m][2]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][2]))
                                            if rez>0: break
                                    elif Otv[j][1] == "x+":
                                        if x2<abs(Per_Check[Otv[i][3]][m][3]) and x1>-abs(Per_Check[Otv[j][3]][n][2]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][2]))
                                            if rez>0: break
                                elif Otv[i][1] == "y+":
                                    rez_name = "y+"
                                    if Otv[j][1] == "x-":
                                        if x2>-abs(Per_Check[Otv[i][3]][m][3]) and x1<abs(Per_Check[Otv[j][3]][n][3]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][3]))
                                            if rez>0: break
                                    elif Otv[j][1] == "x+":
                                        if x1<abs(Per_Check[Otv[j][3]][n][3]) and x2<abs(Per_Check[Otv[i][3]][m][2]):
                                            rez = abs(abs(x1)-abs(Per_Check[Otv[j][3]][n][3]))
                                            if rez>0: break
                                x2+= d2 if x2>0 else -d2
                                if rez>0: break
                            x1+= d1 if x1>0 else -d1
                            if rez>0: break
                        if rez>0: break
                    d_rez[rez_name]=rez
                #rez = 1

                if d_rez.get('x-',0)+d_rez.get('x+',0) !=0 and d_rez.get('y-',0)+d_rez.get('y+',0) !=0:
                    if d_rez.get('x-',0)+d_rez.get('x+',0)<=d_rez.get('y-',0)+d_rez.get('y+',0):
                        d_rez.pop("y-",None)
                        d_rez.pop("y+",None)
                    else:
                        d_rez.pop("x-",None)
                        d_rez.pop("x+",None)
                else:
                    if d_rez.get('x-',0)+d_rez.get('x+',0) !=0:  
                        d_rez.pop("y-",None)
                        d_rez.pop("y+",None)
                    elif d_rez.get('y-',0)+d_rez.get('y+',0) !=0: 
                        d_rez.pop("x-",None)
                        d_rez.pop("x+",None)   

                for d_k in d_rez:
                    for ii in range(len(Otv)):
                        if d_k == Otv[ii][1]:
                            Otv[ii][0]+= d_rez[d_k]  if Otv[ii][0]>0  else -d_rez[d_k]

        D_Otv[k] = Otv

    for k in D_Otv:
        if N_op[k] !=None:
            s = set()
            d = {}
            for i in range(len(D_Otv[k])):
                s.add(D_Otv[k][i][1])
                d[D_Otv[k][i][1]]=i
            if s==set(["x-","x+","y-"]):
                if abs(D_Otv[k][d["x-"]][0])+abs(D_Otv[k][d["x+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0])-abs(D_Otv[k][d["x+"]][0]))/2)
                    D_Otv[k][d["x-"]][0] -=(a+2)
                    D_Otv[k][d["x+"]][0] +=(a+2)
                c = int((D_Otv[k][d["x-"]][0]+D_Otv[k][d["x+"]][0])/2)
                N_op[k]=[N_op[k][0],1,(c-int(N_op[k][1][0]/2),1),N_op[k][1]]
            
            elif s==set(["x-","x+","y+"]):
                if abs(D_Otv[k][d["x-"]][0])+abs(D_Otv[k][d["x+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0])-abs(D_Otv[k][d["x+"]][0]))/2)
                    D_Otv[k][d["x-"]][0] -=(a+2)
                    D_Otv[k][d["x+"]][0] +=(a+2)
                c = int((D_Otv[k][d["x-"]][0]+D_Otv[k][d["x+"]][0])/2)
                N_op[k]=[N_op[k][0],2,(c-int(N_op[k][1][0]/2),-N_op[k][1][1]-1),N_op[k][1]]
            
            elif s==set(["x-","x+"]):
                if abs(D_Otv[k][d["x-"]][0])+abs(D_Otv[k][d["x+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0])-abs(D_Otv[k][d["x+"]][0]))/2)
                    D_Otv[k][d["x-"]][0] -=(a+2)
                    D_Otv[k][d["x+"]][0] +=(a+2)
                c = int((D_Otv[k][d["x-"]][0]+D_Otv[k][d["x+"]][0])/2)
                N_op[k]=[N_op[k][0],3,(c-int(N_op[k][1][0]/2),-N_op[k][1][1]-1),N_op[k][1]]
            
            elif s==set(["x-","y+"]):
                if abs(D_Otv[k][d["x-"]][0])<N_op[k][1][0]:
                    a = int(N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0]))
                    D_Otv[k][d["x-"]][0] -=(a+2)
                N_op[k]=[N_op[k][0],4,(-int(N_op[k][1][0]),-N_op[k][1][1]-1),N_op[k][1]]
            
            elif s==set(["y-","y+"]):
                if abs(D_Otv[k][d["y-"]][0])+abs(D_Otv[k][d["y+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["y-"]][0])-abs(D_Otv[k][d["y+"]][0]))/2)
                    D_Otv[k][d["y-"]][0] -=(a+2)
                    D_Otv[k][d["y+"]][0] +=(a+2)
                c = int((D_Otv[k][d["y-"]][0]+D_Otv[k][d["y+"]][0])/2)
                N_op[k]=[N_op[k][0],5,(-N_op[k][1][1]-1,c-int(N_op[k][1][0]/2)),N_op[k][1]]
            
            elif s==set(["y-","y+","x+"]):
                if abs(D_Otv[k][d["y-"]][0])+abs(D_Otv[k][d["y+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["y-"]][0])-abs(D_Otv[k][d["y+"]][0]))/2)
                    D_Otv[k][d["y-"]][0] -=(a+2)
                    D_Otv[k][d["y+"]][0] +=(a+2)
                c = int((D_Otv[k][d["y-"]][0]+D_Otv[k][d["y+"]][0])/2)
                N_op[k]=[N_op[k][0],6,(-N_op[k][1][1]-1,c-int(N_op[k][1][0]/2)),N_op[k][1]]
            
            elif s==set(["y-","y+","x-"]):
                if abs(D_Otv[k][d["y-"]][0])+abs(D_Otv[k][d["y+"]][0])<N_op[k][1][0]:
                    a = int((N_op[k][1][0]-abs(D_Otv[k][d["y-"]][0])-abs(D_Otv[k][d["y+"]][0]))/2)
                    D_Otv[k][d["y-"]][0] -=(a+2)
                    D_Otv[k][d["y+"]][0] +=(a+2)
                c = int((D_Otv[k][d["y-"]][0]+D_Otv[k][d["y+"]][0])/2)
                N_op[k]=[N_op[k][0],7,(1,c-int(N_op[k][1][0]/2)),N_op[k][1]]

            elif s==set(["y-","y+","x-","x+"]):
                if abs(D_Otv[k][d["x-"]][0])>abs(D_Otv[k][d["x+"]][0]):
                    if N_op[k][1][0]>abs(D_Otv[k][d["x-"]][0]):
                        a = int(N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0]))
                        D_Otv[k][d["x-"]][0] -=(a+2)
                    if N_op[k][1][1]>abs(D_Otv[k][d["y-"]][0]):
                        b = int(N_op[k][1][1]-abs(D_Otv[k][d["y-"]][0]))
                        D_Otv[k][d["y-"]][0] -=(b+2)
                    c = int((D_Otv[k][d["x-"]][0])/2)
                    N_op[k]=[N_op[k][0],8,(c-int(N_op[k][1][0]/2),-N_op[k][1][1]-1),N_op[k][1]]
                elif abs(D_Otv[k][d["x-"]][0])<abs(D_Otv[k][d["x+"]][0]):
                    if N_op[k][1][0]>abs(D_Otv[k][d["x+"]][0]):
                        a = int(N_op[k][1][0]-abs(D_Otv[k][d["x+"]][0]))
                        D_Otv[k][d["x+"]][0] +=(a+2)
                    if N_op[k][1][1]>abs(D_Otv[k][d["y-"]][0]):
                        b = int(N_op[k][1][1]-abs(D_Otv[k][d["y-"]][0]))
                        D_Otv[k][d["y-"]][0] -=(b+2)
                    c = int((D_Otv[k][d["x+"]][0])/2)
                    N_op[k]=[N_op[k][0],8,(c-int(N_op[k][1][0]/2),-N_op[k][1][1]-1),N_op[k][1]]

            elif s==set(["y-","x-"]):
                if abs(D_Otv[k][d["x-"]][0])<N_op[k][1][0]:
                    a = int(N_op[k][1][0]-abs(D_Otv[k][d["x-"]][0]))
                    D_Otv[k][d["x-"]][0] -=(a+2)
                N_op[k]=[N_op[k][0],9,(-int(N_op[k][1][0]),1),N_op[k][1]]
            
            elif s==set(["y-","x+"]):
                if abs(D_Otv[k][d["x+"]][0])<N_op[k][1][0]:
                    a = int(N_op[k][1][0]-abs(D_Otv[k][d["x+"]][0]))
                    D_Otv[k][d["x+"]][0] +=(a+2)
                N_op[k]=[N_op[k][0],10,(0,1),N_op[k][1]]

            elif s==set(["y+","x+"]):
                if abs(D_Otv[k][d["x+"]][0])<N_op[k][1][0]:
                    a = int(N_op[k][1][0]-abs(D_Otv[k][d["x+"]][0]))
                    D_Otv[k][d["x+"]][0] +=(a+2)
                N_op[k]=[N_op[k][0],11,(0,-N_op[k][1][1]-1),N_op[k][1]]
            

    return D_Otv, N_op

def Paralel(i,ivl,left_line,center_line,right_line,Sp_zav):
    """ Проверяем налагаются ли паралельные линии """
    K_dict = {'С':'Ю','В':'3','Ю':'С','З':'В'}
    for j in range(i):
        if ivl[i][3] == ivl[j][3]:
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if ivl[i][3]=="В":
                        if (left_line[i][m][0]<=left_line[j][n][0] and left_line[i][m][2]>=left_line[j][n][2]) or\
                            (left_line[i][m][0]>=left_line[j][n][0] and left_line[i][m][2]<=left_line[j][n][2]) or\
                            (left_line[i][m][0]<left_line[j][n][0]<left_line[i][m][2] and left_line[j][n][0]<left_line[i][m][2]<left_line[j][n][2]) or\
                            (left_line[j][n][0]<left_line[i][m][0]<left_line[j][n][2] and left_line[i][m][0]<left_line[j][n][2]<left_line[i][m][2]):
                            if center_line[i][0][1]<center_line[j][0][1]:
                                if right_line[i][m][1]>left_line[j][n][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(right_line[i][m][1]-left_line[j][n][1])                           
                            elif center_line[i][0][1]>center_line[j][0][1]:
                                if right_line[j][n][1]>left_line[i][m][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(right_line[j][n][1]-left_line[i][m][1])
                    elif ivl[i][3]=="З":
                        if (left_line[i][m][0]>=left_line[j][n][0] and left_line[i][m][2]<=left_line[j][n][2]) or\
                            (left_line[i][m][0]<=left_line[j][n][0] and left_line[i][m][2]>=left_line[j][n][2]) or\
                            (left_line[i][m][0]>left_line[j][n][0]>left_line[i][m][2] and left_line[j][n][0]>left_line[i][m][2]>left_line[j][n][2]) or\
                            (left_line[j][n][0]>left_line[i][m][0]>left_line[j][n][2] and left_line[i][m][0]>left_line[j][n][2]>left_line[i][m][2]):
                            if center_line[i][0][1]<center_line[j][0][1]:
                                if right_line[j][n][1]<left_line[i][m][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(left_line[i][m][1]-right_line[j][n][1])
                            elif center_line[i][0][1]>center_line[j][0][1]:
                                if right_line[i][m][1]<left_line[j][n][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(left_line[j][n][1]-right_line[i][m][1])
                    elif ivl[i][3]=="Ю":
                        if (left_line[i][m][1]<=left_line[j][n][1] and left_line[i][m][3]>=left_line[j][n][3]) or\
                            (left_line[i][m][1]>=left_line[j][n][1] and left_line[i][m][3]<=left_line[j][n][3]) or\
                            (left_line[i][m][1]<left_line[j][n][1]<left_line[i][m][3] and left_line[j][n][1]<left_line[i][m][3]<left_line[j][n][3]) or\
                            (left_line[j][n][1]<left_line[i][m][1]<left_line[j][n][3] and left_line[i][m][1]<left_line[j][n][3]<left_line[i][m][3]):
                            if center_line[i][0][0]<center_line[j][0][0]:
                                if right_line[i][m][0]>left_line[j][n][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "З":
                                            return Sp_zav[i][a][0], abs(right_line[i][m][0]-left_line[j][n][0])                           
                            elif center_line[i][0][0]>center_line[j][0][0]:
                                if right_line[j][n][0]>left_line[i][m][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "В":
                                            return Sp_zav[i][a][0], abs(right_line[j][n][0]-left_line[i][m][0])
                    elif ivl[i][3]=="С":
                        if (left_line[i][m][1]>=left_line[j][n][1] and left_line[i][m][3]<=left_line[j][n][3]) or\
                            (left_line[i][m][1]<=left_line[j][n][1] and left_line[i][m][3]>=left_line[j][n][3]) or\
                            (left_line[i][m][1]>left_line[j][n][1]>left_line[i][m][3] and left_line[j][n][1]>left_line[i][m][3]>left_line[j][n][3]) or\
                            (left_line[j][n][1]>left_line[i][m][1]>left_line[j][n][3] and left_line[i][m][1]>left_line[j][n][3]>left_line[i][m][3]):
                            if center_line[i][0][0]<center_line[j][0][0]:
                                if right_line[j][n][0]<left_line[i][m][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "З":
                                            return Sp_zav[i][a][0], abs(left_line[i][m][0]-right_line[j][n][0])
                            elif center_line[i][0][0]>center_line[j][0][0]:
                                if right_line[i][m][0]<left_line[j][n][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "В":
                                            return Sp_zav[i][a][0], abs(left_line[j][n][0]-right_line[i][m][0])

        elif ivl[i][3] == K_dict[ivl[j][3]]:
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if ivl[i][3]=="В":
                        if (left_line[i][m][0]<=left_line[j][n][2] and left_line[i][m][2]>=left_line[j][n][0]) or\
                            (left_line[i][m][0]>=left_line[j][n][2] and left_line[i][m][2]<=left_line[j][n][0]) or\
                            (left_line[i][m][0]<left_line[j][n][2]<left_line[i][m][2] and left_line[j][n][2]<left_line[i][m][2]<left_line[j][n][0]) or\
                            (left_line[j][n][2]<left_line[i][m][0]<left_line[j][n][0] and left_line[i][m][0]<left_line[j][n][0]<left_line[i][m][2]):
                            if center_line[i][0][1]<center_line[j][0][1]:
                                if right_line[i][m][1]>right_line[j][n][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(right_line[i][m][1]-right_line[j][n][1])
                            elif center_line[i][0][1]>center_line[j][0][1]:
                                if left_line[j][n][1]>left_line[i][m][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(left_line[j][n][1]-left_line[i][m][1])
                    elif ivl[i][3]=="З":
                        if (left_line[i][m][0]>=left_line[j][n][2] and left_line[i][m][2]<=left_line[j][n][0]) or\
                            (left_line[i][m][0]<=left_line[j][n][2] and left_line[i][m][2]>=left_line[j][n][0]) or\
                            (left_line[i][m][0]>left_line[j][n][2]>left_line[i][m][2] and left_line[j][n][2]>left_line[i][m][2]>left_line[j][n][0]) or\
                            (left_line[j][n][2]<left_line[i][m][0]>left_line[j][n][0] and left_line[i][m][0]>left_line[j][n][0]>left_line[i][m][2]):
                            if center_line[i][0][1]<center_line[j][0][1]:
                                if left_line[j][n][1]<left_line[i][m][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(left_line[i][m][1]-left_line[j][n][1])
                            elif center_line[i][0][1]>center_line[j][0][1]:
                                if right_line[i][m][1]<right_line[j][n][1]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(right_line[j][n][1]-right_line[i][m][1]) 
                    elif ivl[i][3]=="Ю":
                        if (left_line[i][m][1]<=left_line[j][n][3] and left_line[i][m][3]>=left_line[j][n][1]) or\
                            (left_line[i][m][1]>=left_line[j][n][3] and left_line[i][m][3]<=left_line[j][n][1]) or\
                            (left_line[i][m][1]<left_line[j][n][3]<left_line[i][m][3] and left_line[j][n][3]<left_line[i][m][3]<left_line[j][n][1]) or\
                            (left_line[j][n][3]<left_line[i][m][1]<left_line[j][n][1] and left_line[i][m][1]<left_line[j][n][1]<left_line[i][m][3]):
                            if center_line[i][0][0]<center_line[j][0][0]:
                                if right_line[i][m][0]>right_line[j][n][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(right_line[i][m][0]-right_line[j][n][0])
                            elif center_line[i][0][0]>center_line[j][0][0]:
                                if left_line[j][n][0]>left_line[i][m][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(left_line[j][n][0]-left_line[i][m][0])
                    elif ivl[i][3]=="С":
                        if (left_line[i][m][1]>=left_line[j][n][3] and left_line[i][m][3]<=left_line[j][n][1]) or\
                            (left_line[i][m][1]<=left_line[j][n][3] and left_line[i][m][3]>=left_line[j][n][1]) or\
                            (left_line[i][m][1]>left_line[j][n][3]>left_line[i][m][3] and left_line[j][n][3]>left_line[i][m][3]>left_line[j][n][1]) or\
                            (left_line[j][n][3]<left_line[i][m][1]>left_line[j][n][1] and left_line[i][m][1]>left_line[j][n][1]>left_line[i][m][3]):
                            if center_line[i][0][0]<center_line[j][0][0]:
                                if left_line[j][n][0]<left_line[i][m][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "С":
                                            return Sp_zav[i][a][0], abs(left_line[i][m][0]-left_line[j][n][0])
                            elif center_line[i][0][0]>center_line[j][0][0]:
                                if right_line[i][m][0]<right_line[j][n][0]:
                                    for a in range(-1,len(Sp_zav[i])-1,-1):
                                        if Sp_zav[i][a][1] == "Ю":
                                            return Sp_zav[i][a][0], abs(right_line[j][n][0]-right_line[i][m][0])



def Peresech(i,ivl,left_line,center_line,right_line,Sp_zav):
    """ Проверяем пересекаются ли перпендикулярные линии """
    for j in range(i):
        if ivl[i][3] =="В" and ivl[j][3] == "С":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][0]<=left_line[j][n][0]<=left_line[i][m][2] and left_line[j][n][3]<=left_line[i][m][1]<=left_line[j][n][1]) or\
                        (left_line[i][m][0]<=right_line[j][n][0]<=left_line[i][m][2] and right_line[j][n][3]<=left_line[i][m][1]<=right_line[j][n][1]) or\
                        (right_line[i][m][0]<=left_line[j][n][0]<=right_line[i][m][2] and left_line[j][n][3]<=right_line[i][m][1]<=left_line[j][n][1]) or\
                        (right_line[i][m][0]<=right_line[j][n][0]<=right_line[i][m][2] and right_line[j][n][3]<=right_line[i][m][1]<=right_line[j][n][1]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "З":
                                l = abs(center_line[i][0][2]-left_line[j][n][0])
                                if l>0: return Sp_zav[i][a][0], l
        if ivl[i][3] =="В" and ivl[j][3] == "Ю":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][0]<=right_line[j][n][0]<=left_line[i][m][2] and right_line[j][n][1]<=left_line[i][m][1]<=right_line[j][n][3]) or\
                        (left_line[i][m][0]<=left_line[j][n][0]<=left_line[i][m][2] and left_line[j][n][1]<=left_line[i][m][1]<=left_line[j][n][3]) or\
                        (right_line[i][m][0]<=right_line[j][n][0]<=right_line[i][m][2] and right_line[j][n][1]<=right_line[i][m][1]<=right_line[j][n][3]) or\
                        (right_line[i][m][0]<=left_line[j][n][0]<=right_line[i][m][2] and left_line[j][n][1]<=right_line[i][m][1]<=left_line[j][n][3]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "З":
                                l = abs(center_line[i][0][2]-right_line[j][n][0])
                                if l>0: return Sp_zav[i][a][0], l 
        if ivl[i][3] =="З" and ivl[j][3] == "С":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][2]<=right_line[j][n][0]<=left_line[i][m][0] and right_line[j][n][3]<=left_line[i][m][1]<=right_line[j][n][1]) or\
                        (left_line[i][m][2]<=left_line[j][n][0]<=left_line[i][m][0] and left_line[j][n][3]<=left_line[i][m][1]<=left_line[j][n][1]) or\
                        (right_line[i][m][2]<=right_line[j][n][0]<=right_line[i][m][0] and right_line[j][n][3]<=right_line[i][m][1]<=right_line[j][n][1]) or\
                        (right_line[i][m][2]<=left_line[j][n][0]<=right_line[i][m][0] and left_line[j][n][3]<=right_line[i][m][1]<=left_line[j][n][1]): 
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "В":
                                l = abs(right_line[j][n][0]-center_line[i][0][2])
                                if l>0: return Sp_zav[i][a][0], l
        if ivl[i][3] =="З" and ivl[j][3] == "Ю":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][2]<=left_line[j][n][0]<=left_line[i][m][0] and left_line[j][n][1]<=left_line[i][m][1]<=left_line[j][n][3]) or\
                        (left_line[i][m][2]<=right_line[j][n][0]<=left_line[i][m][0] and right_line[j][n][1]<=left_line[i][m][1]<=right_line[j][n][3]) or\
                        (right_line[i][m][2]<=left_line[j][n][0]<=right_line[i][m][0] and left_line[j][n][1]<=right_line[i][m][1]<=left_line[j][n][3]) or\
                        (right_line[i][m][2]<=right_line[j][n][0]<=right_line[i][m][0] and right_line[j][n][1]<=right_line[i][m][1]<=right_line[j][n][3]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "В":
                                l = abs(left_line[j][n][0]-center_line[i][0][2])
                                if l>0: return Sp_zav[i][a][0], l 
        if ivl[i][3] =="Ю" and ivl[j][3] == "З":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][1]<=right_line[j][n][1]<=left_line[i][m][3] and right_line[j][n][2]<=left_line[i][m][0]<=right_line[j][n][0]) or\
                        (left_line[i][m][1]<=left_line[j][n][1]<=left_line[i][m][3] and left_line[j][n][2]<=left_line[i][m][0]<=left_line[j][n][0]) or\
                        (right_line[i][m][1]<=right_line[j][n][1]<=right_line[i][m][3] and right_line[j][n][2]<=right_line[i][m][0]<=right_line[j][n][0]) or\
                        (right_line[i][m][1]<=left_line[j][n][1]<=right_line[i][m][3] and left_line[j][n][2]<=right_line[i][m][0]<=left_line[j][n][0]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "З":
                                l = abs(left_line[i][m][0]-center_line[j][0][2])
                                if l>0: return Sp_zav[i][a][0], l
        if ivl[i][3] =="Ю" and ivl[j][3] == "В":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][1]<=left_line[j][n][1]<=left_line[i][m][3] and left_line[j][n][0]<=left_line[i][m][0]<=left_line[j][n][2]) or\
                        (left_line[i][m][1]<=right_line[j][n][1]<=left_line[i][m][3] and right_line[j][n][0]<=left_line[i][m][0]<=right_line[j][n][2]) or\
                        (right_line[i][m][1]<=left_line[j][n][1]<=right_line[i][m][3] and left_line[j][n][0]<=right_line[i][m][0]<=left_line[j][n][2]) or\
                        (right_line[i][m][1]<=right_line[j][n][1]<=right_line[i][m][3] and right_line[j][n][0]<=right_line[i][m][0]<=right_line[j][n][2]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "В":
                                l = abs(center_line[j][0][2]-right_line[i][m][0])
                                if l>0: return Sp_zav[i][a][0], l
        if ivl[i][3] =="С" and ivl[j][3] == "З":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][3]<=left_line[j][n][1]<=left_line[i][m][1] and left_line[j][n][2]<=left_line[i][m][0]<=left_line[j][n][0]) or\
                        (left_line[i][m][3]<=right_line[j][n][1]<=left_line[i][m][1] and right_line[j][n][2]<=left_line[i][m][0]<=right_line[j][n][0]) or\
                        (right_line[i][m][3]<=left_line[j][n][1]<=right_line[i][m][1] and left_line[j][n][2]<=right_line[i][m][0]<=left_line[j][n][0]) or\
                        (right_line[i][m][3]<=right_line[j][n][1]<=right_line[i][m][1] and right_line[j][n][2]<=right_line[i][m][0]<=right_line[j][n][0]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "Ю":
                                l = abs(left_line[j][n][1]-center_line[i][0][3])
                                if l>0: return Sp_zav[i][a][0], l

        if ivl[i][3] =="С" and ivl[j][3] == "Ю":
            for m in range(len(left_line[i])):
                for n in range(len(left_line[j])):
                    if (left_line[i][m][3]<=right_line[j][n][1]<=left_line[i][m][1] and right_line[j][n][0]<=left_line[i][m][0]<=right_line[j][n][2]) or\
                        (left_line[i][m][3]<=left_line[j][n][1]<=left_line[i][m][1] and left_line[j][n][0]<=left_line[i][m][0]<=left_line[j][n][2]) or\
                        (right_line[i][m][3]<=right_line[j][n][1]<=right_line[i][m][1] and right_line[j][n][0]<=right_line[i][m][0]<=right_line[j][n][2]) or\
                        (right_line[i][m][3]<=left_line[j][n][1]<=right_line[i][m][1] and left_line[j][n][0]<=right_line[i][m][0]<=left_line[j][n][2]):
                        for a in range(-1,len(Sp_zav[i])-1,-1):
                            if Sp_zav[i][a][1] == "В":
                                l = abs(center_line[j][0][2]-left_line[i][m][0])
                                if l>0: return Sp_zav[i][a][0], l

                     


                    
def Pos_Vetvi(ivl,xy,dl,D_Otv,Per_Check,Im_box,VVL_sort, Line_width, Min_len, Razm_dlin, ych_sb, text_height,font_size,PS,podp,N_op,x_list,y_list,per_name):
    """ Определение положения и длин ветвей без пересечений """ 
    Popr_dlin = [ 0 for i in ivl]
    Popr_dlin_s = [ 0 for i in ivl] 
    xy_cor = []

    for i in range(len(xy)):
        if xy[i][0] >  xy[i][1]:
            xy_cor.append([xy[i][0],-xy[i][1],-xy[i][3],-xy[i][2]])
        else:
            xy_cor.append([xy[i][0],xy[i][1],xy[i][2],xy[i][3]])

    k=0

    Othod = {"В":"x+","З":"x-","С":"y-","Ю":"y+"}
    Podhod = {"В":"x-","З":"x+","С":"y+","Ю":"y-"}
    
    per_key = list(per_name.keys())
    while k==0 or (sum(Popr_dlin)!=0 and k!=100):

        for i in range(len(Popr_dlin)):
            if Popr_dlin[i]>0:
                Popr_dlin_s[i]+=Popr_dlin[i]
                Popr_dlin[i] = 0
                c1,c2,c3,c4 = Vetvi_Ris(ivl[i],VVL_sort[i], Line_width[i], Min_len[i], Razm_dlin[i], ych_sb[i], text_height,font_size,PS[i],podp[i],per_name[per_key[i]],size=Popr_dlin_s[i]/dl[i])
                if c1[0] >  c1[1]:
                    xy_cor[i]=[c1[0],-c1[1],-c1[3],-c1[2]]
                else:
                    xy_cor[i]=[c1[0],c1[1],c1[2],c1[3]]
                Per_Check[i]=c2
                Im_box[i]=c4

        k+=1
        left_line = []
        center_line = []
        right_line = []
        yzl_cord = {}
        yzl_zav = {}
        Sp_zav = []

        
        x, y = 0, 0
        for i in range(len(ivl)):
            if len(D_Otv[ivl[i][0]]) == 0:
                if ivl[i][0] not in yzl_cord:
                    yzl_cord[ivl[i][0]] = (x,y)

            else:
                for j in D_Otv[ivl[i][0]]:
                    if Othod[ivl[i][3]] == j[1]:
                        (x,y) = yzl_cord[ivl[i][0]]
                        if j[1] =="x-" or j[1] =="x+":
                            x+=j[0]
                        else:
                            y+=j[0]
                        break

            Sp_zav.append(yzl_zav.get(ivl[i][0],[]))
            left_line.append([])
            right_line.append([])

            if ivl[i][3] =="В":
                xn = x+xy_cor[i][1]
                yn = y
                for j in range(len(Per_Check[i])):
                    left_line[i].append([x+abs(Per_Check[i][j][0]),y-Per_Check[i][j][2],
                        x+abs(Per_Check[i][j][1]),y-Per_Check[i][j][2]])
                    right_line[i].append([x+abs(Per_Check[i][j][0]),y+Per_Check[i][j][3],
                        x+abs(Per_Check[i][j][1]),y+Per_Check[i][j][3]])
            elif ivl[i][3] =="З":
                xn = x-xy_cor[i][1]
                yn = y
                for j in range(len(Per_Check[i])):
                    left_line[i].append([x-abs(Per_Check[i][j][0]),y+Per_Check[i][j][2],
                        x-abs(Per_Check[i][j][1]),y+Per_Check[i][j][2]])
                    right_line[i].append([x-abs(Per_Check[i][j][0]),y-Per_Check[i][j][3],
                        x-abs(Per_Check[i][j][1]),y-Per_Check[i][j][3]])
            elif ivl[i][3] =="С":
                xn = x
                yn = y-xy_cor[i][1]
                for j in range(len(Per_Check[i])):
                    left_line[i].append([x-Per_Check[i][j][2],y-abs(Per_Check[i][j][0]),
                        x-Per_Check[i][j][2],y-abs(Per_Check[i][j][1])])
                    right_line[i].append([x+Per_Check[i][j][3],y-abs(Per_Check[i][j][0]),
                        x+Per_Check[i][j][3],y-abs(Per_Check[i][j][1])])                
            elif ivl[i][3] =="Ю":
                xn = x
                yn = y+xy_cor[i][1]
                for j in range(len(Per_Check[i])):
                    left_line[i].append([x+Per_Check[i][j][2],y+abs(Per_Check[i][j][0]),
                        x+Per_Check[i][j][2],y+abs(Per_Check[i][j][1])])
                    right_line[i].append([x-Per_Check[i][j][3],y+abs(Per_Check[i][j][0]),
                        x-Per_Check[i][j][3],y+abs(Per_Check[i][j][1])]) 
            center_line.append([[x,y,xn,yn],3])

            # Проверяем паралельные линии на наслоение
            
            try:
                a,b = Paralel(i,ivl,left_line,center_line,right_line,Sp_zav)
                Popr_dlin[a] = b
                break
            except Exception:
                None
            try:
                a,b = Peresech(i,ivl,left_line,center_line,right_line,Sp_zav)
                Popr_dlin[a] = b
                break
            except Exception:
                None

            x = xn
            y = yn

            yzl_zav[ivl[i][1]] = yzl_zav.get(ivl[i][0],[])+[[i,ivl[i][3]]]

            if len(D_Otv[ivl[i][1]]) == 0:
                if ivl[i][1] not in yzl_cord:
                    yzl_cord[ivl[i][1]] = (x,y)

            else:
                if ivl[i][1] not in yzl_cord:
                    for j in D_Otv[ivl[i][1]]:
                        if Podhod[ivl[i][3]] == j[1]:
                            if j[1] =="x-" or j[1] =="x+":  
                                x-=j[0]
                            else:
                                y-=j[0]
                            yzl_cord[ivl[i][1]] = (x,y)
                            break

        Yzl_line = []
        N_op_n = {}

        for key in D_Otv:
            if len(D_Otv[key])>0:
                for i in range(len(D_Otv[key])):
                    if D_Otv[key][i][1] == "x-" or D_Otv[key][i][1] == "x+":
                        if D_Otv[key][i][0]>0:
                            yk=-0
                            xk=-2
                        else: 
                            yk=1
                            xk=0
                        Yzl_line.append([[yzl_cord[key][0],yzl_cord[key][1]+yk,\
                            yzl_cord[key][0]+D_Otv[key][i][0],yzl_cord[key][1]+yk],2])
                        Yzl_line.append([[yzl_cord[key][0]+D_Otv[key][i][0]+xk,yzl_cord[key][1]-5,\
                            yzl_cord[key][0]+D_Otv[key][i][0]+xk,yzl_cord[key][1]+5],2])
                        xt = yzl_cord[key][0]
                        yt = yzl_cord[key][1]
                    elif D_Otv[key][i][1] == "y-" or D_Otv[key][i][1] == "y+":
                        if D_Otv[key][i][0]>0:
                            xk=-0
                            yk=-2
                        else: 
                            xk=1
                            yk=0
                        Yzl_line.append([[yzl_cord[key][0]+xk,yzl_cord[key][1],\
                            yzl_cord[key][0]+xk,yzl_cord[key][1]+D_Otv[key][i][0]],2])
                        Yzl_line.append([[yzl_cord[key][0]-5,yzl_cord[key][1]+D_Otv[key][i][0]+yk,\
                            yzl_cord[key][0]+5,yzl_cord[key][1]+D_Otv[key][i][0]+yk],2])
                        xt = yzl_cord[key][0]
                        yt = yzl_cord[key][1]
                if N_op[key] != None:
                    N_op_n[key]=[N_op[key][0],N_op[key][1],(N_op[key][2][0]+xt,N_op[key][2][1]+yt),N_op[key][3]]
                else:
                    N_op_n[key]=None
            else:
                N_op_n[key] = None

        x_min,x_max=0,0
        y_min,y_max=0,0

        for i in center_line:
            x_min = i[0][0] if i[0][0]<x_min else x_min
            x_min = i[0][2] if i[0][2]<x_min else x_min
            x_max = i[0][0] if i[0][0]>x_max else x_max
            x_max = i[0][2] if i[0][2]>x_max else x_max

            y_min = i[0][1] if i[0][1]<y_min else y_min
            y_min = i[0][3] if i[0][3]<y_min else y_min
            y_max = i[0][1] if i[0][1]>y_max else y_max
            y_max = i[0][3] if i[0][3]>y_max else y_max
        
        for j in left_line:
            for i in j:
                x_min = i[0] if i[0]<x_min else x_min
                x_min = i[2] if i[2]<x_min else x_min
                x_max = i[0] if i[0]>x_max else x_max
                x_max = i[2] if i[2]>x_max else x_max

                y_min = i[1] if i[1]<y_min else y_min
                y_min = i[3] if i[3]<y_min else y_min
                y_max = i[1] if i[1]>y_max else y_max
                y_max = i[3] if i[3]>y_max else y_max

        for j in right_line:
            for i in j:
                x_min = i[0] if i[0]<x_min else x_min
                x_min = i[2] if i[2]<x_min else x_min
                x_max = i[0] if i[0]>x_max else x_max
                x_max = i[2] if i[2]>x_max else x_max

                y_min = i[1] if i[1]<y_min else y_min
                y_min = i[3] if i[3]<y_min else y_min
                y_max = i[1] if i[1]>y_max else y_max
                y_max = i[3] if i[3]>y_max else y_max

        
        if abs(x_min)+x_max<x_list:
            hor_col=0
            k_x=x_list-abs(x_min)-x_max
            for i in ivl:
                if i[3]=="В" or i[3]=="З":
                    hor_col+=1
            k_x = 0 if hor_col==0 else int(k_x/hor_col)
            for i in range(len(ivl)):
                if ivl[i][3]=="В" or ivl[i][3]=="З":
                    Popr_dlin[i]=k_x

        if abs(y_min)+y_max<y_list:
            vert_col=0
            k_y=y_list-abs(y_min)-y_max
            for i in ivl:
                if i[3]=="С" or i[3]=="Ю":
                    vert_col+=1
            k_y = 0 if vert_col==0 else int(k_y/vert_col)
            for i in range(len(ivl)):
                if ivl[i][3]=="С" or ivl[i][3]=="Ю":
                    Popr_dlin[i]=k_y


    image = Image.new('RGBA',(abs(x_min)+x_max,abs(y_min)+y_max), (0,0,0,0)) #'white'
    draw = ImageDraw.Draw(image)

    for i in range(len(ivl)):
        if ivl[i][3]=="В":
            s = (center_line[i][0][0]+abs(x_min),\
                center_line[i][0][1]+abs(y_min)+xy_cor[i][2],\
                center_line[i][0][0]+abs(x_min)+xy_cor[i][1],\
                center_line[i][0][1]+abs(y_min)+xy_cor[i][3])


            image.paste(Im_box[i].convert('RGB'), s, Im_box[i])
        if ivl[i][3]=="З":
            s = (center_line[i][0][0]+abs(x_min)-xy_cor[i][1],\
                center_line[i][0][1]+abs(y_min)-xy_cor[i][3],\
                center_line[i][0][0]+abs(x_min),\
                center_line[i][0][1]+abs(y_min)-xy_cor[i][2])


            image.paste(Im_box[i].convert('RGB'), s, Im_box[i])

        if ivl[i][3]=="С":
            Im_box[i]=Im_box[i].transpose(Image.ROTATE_90)

            s = (center_line[i][0][0]+abs(x_min)+xy_cor[i][2],\
                center_line[i][0][1]+abs(y_min)-xy_cor[i][1],\
                center_line[i][0][0]+abs(x_min)+xy_cor[i][3],\
                center_line[i][0][1]+abs(y_min))


            image.paste(Im_box[i].convert('RGB'), s, Im_box[i])
        if ivl[i][3]=="Ю":
            Im_box[i]=Im_box[i].transpose(Image.ROTATE_90)

            s = (center_line[i][0][0]+abs(x_min)-xy_cor[i][3],\
                center_line[i][0][1]+abs(y_min),\
                center_line[i][0][0]+abs(x_min)-xy_cor[i][2],\
                center_line[i][0][1]+abs(y_min)+xy_cor[i][1])


            image.paste(Im_box[i].convert('RGB'), s, Im_box[i])

    for k in N_op:
        if N_op_n[k] != None:
            im = Image.new('RGBA',N_op_n[k][3], (0,0,0,0))
            dr = ImageDraw.Draw(im)
            Ar = ImageFont.truetype ( 'Fonts/arial.ttf', font_size)
            if N_op_n[k][1] in set([1,2,3,4,8,9,10,11]):
                dr.text((0,0),N_op_n[k][0],fill="black", font=Ar)
                image.paste(im.convert('RGB'), (N_op_n[k][2][0]+abs(x_min),N_op_n[k][2][1]+abs(y_min)), im)
            else:
                dr.text((0,0),N_op_n[k][0],fill="black", font=Ar)
                im=im.transpose(Image.ROTATE_90)
                image.paste(im.convert('RGB'), (N_op_n[k][2][0]+abs(x_min),N_op_n[k][2][1]+abs(y_min)), im)

    
    """
    for i in center_line:
        i[0][0]+=abs(x_min)
        i[0][1]+=abs(y_min)
        i[0][2]+=abs(x_min)
        i[0][3]+=abs(y_min)
        draw.line(i[0] ,fill="black", width=i[1])
    
    for i in left_line:
        for j in i:
            j[0]+=abs(x_min)
            j[1]+=abs(y_min)
            j[2]+=abs(x_min)
            j[3]+=abs(y_min)
            draw.line(j ,fill="black", width=1)

    for i in right_line:
        for j in i:
            j[0]+=abs(x_min)
            j[1]+=abs(y_min)
            j[2]+=abs(x_min)
            j[3]+=abs(y_min)
            draw.line(j ,fill="black", width=1)
    """
    for i in Yzl_line:
        i[0][0]+=abs(x_min)
        i[0][1]+=abs(y_min)
        i[0][2]+=abs(x_min)
        i[0][3]+=abs(y_min)
        draw.line(i[0] ,fill="black", width=i[1])
    
    del draw
    
    
    #image.save('test1.png')
    return image

def PodpYzl(ivl,yr_op,per_name):
    per_key = list(per_name.keys())

    sp_yr = ['' for i in ivl]
    if yr_op:
        for k in yr_op:
            for i in yr_op[k]:
                sp_yr[i]=k

    d_yz = {}
    for i in range(len(ivl)):
        if ivl[i][0] not in d_yz:
            d_yz[ivl[i][0]]=[i]
        else:
            d_yz[ivl[i][0]].append(i)
        if ivl[i][1] not in d_yz:
            d_yz[ivl[i][1]]=[i]
        else:
            d_yz[ivl[i][1]].append(i)

    podp = [[] for i in ivl]

    N_op={}
    for k in d_yz:
        N_op[k]=None 
        Trig = False
        for i in range(len(d_yz[k])):
            for j in range(i+1,len(d_yz[k])):
                if ivl[d_yz[k][i]][5] == ivl[d_yz[k][j]][4] and\
                    sp_yr[d_yz[k][i]] == sp_yr[d_yz[k][j]] and sp_yr[d_yz[k][i]] !="":
                    nam_yz = str(ivl[d_yz[k][i]][5])

                    nam_yz1 = per_name[per_key[d_yz[k][i]]].get(ivl[d_yz[k][i]][5],str(ivl[d_yz[k][i]][5]))
                    nam_yz3 = nam_yz1 if nam_yz1 != nam_yz else nam_yz 
                    nam_yz2 = per_name[per_key[d_yz[k][j]]].get(ivl[d_yz[k][j]][4],str(ivl[d_yz[k][j]][4]))
                    nam_yz3 = nam_yz2 if nam_yz2 != nam_yz else nam_yz3

                    if nam_yz3[0] !="'": 
                        N_op[k]=str(nam_yz3)
                    else:
                        N_op[k]=str(ivl[d_yz[k][i]][5]) #  
                    for h in range(len(d_yz[k])):
                        podp[d_yz[k][h]].append(False)
                    Trig = True
                    break
            if Trig: break        
            podp[d_yz[k][i]].append(True)


    return N_op, podp

def Title_ris(im,x_list,y_list,font_size_title,name_vl):
    (x,y) = im.size
    #Image.new('RGBA',(abs(x_min)+x_max,abs(y_min)+y_max), (0,0,0,0)) #'white'
    #print(x,y)
    imt = Image.new('RGBA',(1000,1000), (0,0,0,0)) #'white'
    dr = ImageDraw.Draw(imt)
    Ar = ImageFont.truetype ( 'Fonts/arial.ttf', font_size_title)
    try:
        (x2,y2)=dr.textsize(name_vl, font=Ar)
    except Exception:
        x2,y2=0,0
    (x1,y1)=dr.textsize('Схема сближения',  font=Ar)
    if x2!=0 and y2!=0:
        imt2 = Image.new('RGBA',(x2,y2), (0,0,0,0)) #'white'
        dr = ImageDraw.Draw(imt2)
        dr.text((0,0),name_vl, fill="black", font=Ar)
    imt1 = Image.new('RGBA',(x1,y1), (0,0,0,0)) #'white'
    dr = ImageDraw.Draw(imt1)
    dr.text((0,0),'Схема сближения', fill="black", font=Ar)
    if y<y_list:
        y_c = int(y1+y2+y_list/2-y/2)
        y_s = y1+y2+y_list
    else:
        y_c = y1+y2
        y_s = y1+y2+y
    if x<x_list:
        x_c = int(x_list/2-x/2)
        x_s = x_list
    else:
        x_c = 0
        x_s = x
    #print(x_s,y_s,x_c,y_c,x,y)
    x_t1 = int(x_s/2-x1/2)
    x_t2 = int(x_s/2-x2/2)
    image = Image.new('RGB',(x_s,y_s), 'white')
    image.paste(imt1.convert('RGB'), (x_t1,0), imt1)
    if x2!=0 and y2!=0:
        image.paste(imt2.convert('RGB'), (x_t2,y1), imt2)
    image.paste(im.convert('RGB'), (x_c,y_c), im)
    image.save("Pictures/sh1.jpg")
    image=image.transpose(Image.ROTATE_90)
    image.save("Pictures/sh2.jpg")
    





def Ris_Sh_Sb(ivl, vvl, per, km, yr_op, font_size, font_size_title, name_vl,per_name):
    """ Рисование полной схемы сближения """
    x_list,y_list =1754,1059 #1175,830
    N_op, podp = PodpYzl(ivl,yr_op,per_name)
        
    VVL_sort, Line_width, Min_len, Razm_dlin, ych_sb, text_height, PS, N_op = RazdYch(ivl, vvl, per, km, N_op, font_size,per_name)

    xy=[]
    Per_Check=[]
    dl=[]
    Im_box = []
    per_key = list(per_name.keys())
    for i in range(len(ivl)): 
        a,b,c,im = Vetvi_Ris(ivl[i],VVL_sort[i], Line_width[i], Min_len[i], Razm_dlin[i], ych_sb[i], text_height,font_size,PS[i],podp[i],per_name[per_key[i]])
        xy.append(a)
        Per_Check.append(b)
        dl.append(c)
        Im_box.append(im)

    d_y = Yzl(ivl)

    
    D_Otv, N_op = Rasp(ivl,d_y,xy,Per_Check,N_op)

    image = Pos_Vetvi(ivl,xy,dl,D_Otv,Per_Check,Im_box,VVL_sort,Line_width, Min_len, Razm_dlin, ych_sb, text_height,font_size,PS,podp,N_op,x_list,y_list,per_name)
    #print("test")
    Title_ris(image,x_list,y_list,font_size_title,name_vl)


    #Vetvi_Ris(ivl[0],VVL_sort[0], Line_width[0], Min_len[0], Razm_dlin[0], ych_sb[0], text_height,font_size)
                    
                
            

                           
