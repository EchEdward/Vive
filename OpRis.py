from PIL import Image, ImageDraw, ImageFont



def Point(sp,k):
    x, y = sp
    return (x-k,y-k,x+k,y+k)

def Mashtab(xa,xb,xc,ya,yb,yc,girl,xt1,xt2,yt1,yt2,Razm):
    
    m=max(ya,yb,yc,yt1,yt2,abs(xa)+abs(xb),abs(xa)+abs(xc),abs(xc)+abs(xb))
    
    xa=(0.9*Razm)*xa/(m*1)
    xb=(0.9*Razm)*xb/(m*1)
    xc=(0.9*Razm)*xc/(m*1)
    xt1=(0.9*Razm)*xt1/(m*1)
    xt2=(0.9*Razm)*xt2/(m*1)

    ya=(0.9*Razm)*ya/(m)
    yb=(0.9*Razm)*yb/(m)
    yc=(0.9*Razm)*yc/(m)
    yt1=(0.9*Razm)*yt1/(m)
    yt2=(0.9*Razm)*yt2/(m)

    girl=(0.9*Razm)*girl/(m)
    
    return xa,xb,xc,ya,yb,yc,girl,xt1,xt2,yt1,yt2
        
    

def RisOpor(w,i,j,To):
    Razm=500
    Ar_30 = ImageFont.truetype ( 'Fonts/arial.ttf', 30 )
    Ar_10 = ImageFont.truetype ( 'Fonts/arial.ttf', 10 )
    (xa,xb,xc,ya,yb,yc,girl,xt1,xt2,yt1,yt2,pos)=w

    image = Image.new('RGB',(Razm,Razm), 'white')
    draw = ImageDraw.Draw(image)

    # Составим пояснительный текст
    s='Опора: '+To+'\n'
    s+='Координаты проводников \nотносительно оси опоры:\n'
    s+='XA='+str(round(xa,3))+' м; YA='+str(round(ya-girl,3))+' м;\n'
    s+='XB='+str(round(xb,3))+' м; YB='+str(round(yb-girl,3))+' м;\n'
    s+='XC='+str(round(xc,3))+' м; YC='+str(round(yc-girl,3))+' м;\n'
    if (xt1 != 0 and yt1 != 0) or (xt1 != 0 or yt1 != 0):
        s+='XT='+str(round(xt1,3))+' м; YT='+str(round(yt1,3))+' м;\n'
    if (xt2 != 0 and yt2 != 0) or (xt2 != 0 or yt2 != 0):
        s+='XT='+str(round(xt2,3))+' м; YT='+str(round(yt2,3))+' м;\n'
    s+='Длинна гирлянды: '+str(round(girl,3))+' м;'
    (x,y)=draw.textsize(s, font=Ar_10)
    draw.text((0,Razm-y),s, fill="black", font=Ar_10)

    # Выбор конфигурации опоры
    if xa<0 and xb<0 and xc<0:
        a=1
    elif xa>0 and xb>0 and xc>0:
        a=2
    elif ya==yb and ya==yc and (xa==0 or xb==0 or xc==0):
        a=3
    else:
        a=0


    xa,xb,xc,ya,yb,yc,girl,xt1,xt2,yt1,yt2=Mashtab(xa,xb,xc,ya,yb,yc,girl,xt1,xt2,yt1,yt2,Razm)


    xa+=0.5*Razm
    xb+=0.5*Razm
    xc+=0.5*Razm

    ya=Razm-ya
    yb=Razm-yb
    yc=Razm-yc
    


    if a==0:
        draw.line((0.5*Razm,Razm,0.5*Razm,min(ya,yb,yc)),fill="black", width=7)
        
        draw.line((0.5*Razm,ya,xa,ya),fill="black", width=7)
        draw.line((0.5*Razm,yb,xb,yb),fill="black", width=7)
        draw.line((0.5*Razm,yc,xc,yc),fill="black", width=7)

        draw.line((xa,ya,xa,ya+girl),fill="black", width=7)
        draw.line((xb,yb,xb,yb+girl),fill="black", width=7)
        draw.line((xc,yc,xc,yc+girl),fill="black", width=7)

        if (xt1 != 0 and yt1 != 0) or (xt1 != 0 or yt1 != 0):
            yt1=Razm-yt1
            xt1+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt1),fill="black", width=7)
            draw.line((0.5*Razm,yt1,xt1,yt1),fill="black", width=7)
            draw.ellipse(Point((xt1,yt1),15), fill="blue", outline="blue")
            draw.text((xt1-9,yt1-16),'T', fill="black", font=Ar_30)
        if (xt2 != 0 and yt2 != 0) or (xt2 != 0 or yt2 != 0):
            yt2=Razm-yt2
            xt2+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt2),fill="black", width=7)
            draw.line((0.5*Razm,yt2,xt2,yt2),fill="black", width=7)
            draw.ellipse(Point((xt2,yt2),15), fill="blue", outline="blue")
            draw.text((xt2-9,yt2-16),'T', fill="black", font=Ar_30)
            
    if a==1:
        draw.line((0.5*Razm,Razm,0.5*Razm,min(ya,yb,yc)),fill="black", width=7)
        
        draw.line((0.5*Razm,ya,xa,ya),fill="black", width=7)
        draw.line((0.5*Razm,yb,xb,yb),fill="black", width=7)
        draw.line((0.5*Razm,yc,xc,yc),fill="black", width=7)

        draw.line((xa,ya,xa,ya+girl),fill="black", width=7)
        draw.line((xb,yb,xb,yb+girl),fill="black", width=7)
        draw.line((xc,yc,xc,yc+girl),fill="black", width=7)

        if (xt1 != 0 and yt1 != 0) or (xt1 != 0 or yt1 != 0):
            yt1=Razm-yt1
            xt1+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt1),fill="black", width=7)
            draw.line((0.5*Razm,yt1,xt1,yt1),fill="black", width=7)
            draw.ellipse(Point((xt1,yt1),15), fill="blue", outline="blue")
            draw.text((xt1-9,yt1-16),'T', fill="black", font=Ar_30)
        if (xt2 != 0 and yt2 != 0) or (xt2 != 0 or yt2 != 0):
            yt2=Razm-yt2
            xt2+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt2),fill="black", width=7)
            draw.line((0.5*Razm,yt2,xt2,yt2),fill="black", width=7)
            draw.ellipse(Point((xt2,yt2),15), fill="blue", outline="blue")
            draw.text((xt2-9,yt2-16),'T', fill="black", font=Ar_30)

    if a==2:
        draw.line((0.5*Razm,Razm,0.5*Razm,min(ya,yb,yc)),fill="black", width=7)
        
        draw.line((0.5*Razm,ya,xa,ya),fill="black", width=7)
        draw.line((0.5*Razm,yb,xb,yb),fill="black", width=7)
        draw.line((0.5*Razm,yc,xc,yc),fill="black", width=7)

        draw.line((xa,ya,xa,ya+girl),fill="black", width=7)
        draw.line((xb,yb,xb,yb+girl),fill="black", width=7)
        draw.line((xc,yc,xc,yc+girl),fill="black", width=7)

        if (xt1 != 0 and yt1 != 0) or (xt1 != 0 or yt1 != 0):
            yt1=Razm-yt1
            xt1+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt1),fill="black", width=7)
            draw.line((0.5*Razm,yt1,xt1,yt1),fill="black", width=7)
            draw.ellipse(Point((xt1,yt1),15), fill="blue", outline="blue")
            draw.text((xt1-9,yt1-16),'T', fill="black", font=Ar_30)
        if (xt2 != 0 and yt2 != 0) or (xt2 != 0 or yt2 != 0):
            yt2=Razm-yt2
            xt2+=0.5*Razm
            draw.line((0.5*Razm,min(ya,yb,yc),0.5*Razm,yt2),fill="black", width=7)
            draw.line((0.5*Razm,yt2,xt2,yt2),fill="black", width=7)
            draw.ellipse(Point((xt2,yt2),15), fill="blue", outline="blue")
            draw.text((xt2-9,yt2-16),'T', fill="black", font=Ar_30)

    if a==3:
        op1=(max(xa,xb,xc)-min(xa,xb,xc))/4
        mn=min(xa,xb,xc)
        draw.line((mn+op1,Razm,mn+op1,min(ya,yb,yc)),fill="black", width=7)
        draw.line((mn+3*op1,Razm,mn+3*op1,min(ya,yb,yc)),fill="black", width=7)
        draw.line((mn+op1,min(ya,yb,yc),mn+4*op1,min(ya,yb,yc)),fill="black", width=7)
        
        draw.line((0.5*Razm,ya,xa,ya),fill="black", width=7)
        draw.line((0.5*Razm,yb,xb,yb),fill="black", width=7)
        draw.line((0.5*Razm,yc,xc,yc),fill="black", width=7)

        draw.line((xa,ya,xa,ya+girl),fill="black", width=7)
        draw.line((xb,yb,xb,yb+girl),fill="black", width=7)
        draw.line((xc,yc,xc,yc+girl),fill="black", width=7)

        if (xt1 != 0 and yt1 != 0) or (xt1 != 0 or yt1 != 0):
            yt1=Razm-yt1
            xt1+=0.5*Razm
            if ((mn+op1-xt1)**2+(min(ya,yb,yc)-yt1)**2)<((mn+3*op1-xt1)**2+(min(ya,yb,yc)-yt1)**2):
                draw.line((mn+op1,min(ya,yb,yc),xt1,yt1),fill="black", width=7)
            else:
                draw.line((mn+3*op1,min(ya,yb,yc),xt1,yt1),fill="black", width=7)
            draw.ellipse(Point((xt1,yt1),15), fill="blue", outline="blue")
            draw.text((xt1-9,yt1-16),'T', fill="black", font=Ar_30)
        if (xt2 != 0 and yt2 != 0) or (xt2 != 0 or yt2 != 0):
            yt2=Razm-yt2
            xt2+=0.5*Razm
            if ((mn+op1-xt2)**2+(min(ya,yb,yc)-yt2)**2)<((mn+3*op1-xt2)**2+(min(ya,yb,yc)-yt2)**2):
                draw.line((mn+op1,min(ya,yb,yc),xt2,yt2),fill="black", width=7)
            else:
                draw.line((mn+3*op1,min(ya,yb,yc),xt2,yt2),fill="black", width=7)
            draw.ellipse(Point((xt2,yt2),15), fill="blue", outline="blue")
            draw.text((xt2-9,yt2-16),'T', fill="black", font=Ar_30)

    draw.ellipse(Point((xa,ya+girl),15), fill="yellow", outline="yellow")
    draw.ellipse(Point((xb,yb+girl),15), fill="green", outline="green")
    draw.ellipse(Point((xc,yc+girl),15), fill="red", outline="red")

    
    draw.text((xa-9,ya+girl-16),'A', fill="black", font=Ar_30)
    draw.text((xb-9,yb+girl-16),'B', fill="black", font=Ar_30)
    draw.text((xc-9,yc+girl-16),'C', fill="black", font=Ar_30)

    del draw
    image.save('Op_Fig/'+str(j)+str(i)+'.jpg')

  
    
    
