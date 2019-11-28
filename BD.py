import sqlite3


DB=sqlite3.connect('VLdatabase.db') # Открываем (создаём) базу данных
cur=DB.cursor()        # Создаем объект-курсор

# Создаём таблицу для настроеек
sql = """\
CREATE TABLE Nastrouki (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   int INTEGER,
   real REAL,
   text TEXT
);
"""

try:                       # Обрабатываем исключения
    cur.executescript(sql) # Выполняем SQL-запросы
except sqlite3.DatabaseError as err:
    print("Настройки. Ошибка:", err)
else:
    print("Настройки. Запрос успешно выполнен")

# Создаём таблицу корня
sql = """\
CREATE TABLE Koren (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   Name TEXT,
   Name_SQL TEXT
);
"""

try:                       # Обрабатываем исключения
    cur.executescript(sql) # Выполняем SQL-запросы
except sqlite3.DatabaseError as err:
    print("Корень. Ошибка:", err)
else:
    print("Корень. Запрос успешно выполнен")

def Vvod_nasrt(sp):
    sql_z='INSERT INTO Nastrouki VALUES (?,?,?,?)'
    for i in sp:
        try:  
            cur.execute(sql_z,i)
            
        except sqlite3.DatabaseError as err1:
            #print("Ошибка1:", err1)
            try:
                sql_up="UPDATE Nastrouki SET int=%r, real=%r, text=%r WHERE id=%r" %(i[1],i[2],i[3],i[0])
                cur.executescript(sql_up)
            except sqlite3.DatabaseError as err2:
                #print("Ошибка2:", err2)
                #cur.executescript("DROP TABLE Nastrouki")
                Vvod_nasrt(sp)
            #else:
                #print('Good2')
                #DB.commit() # Завершаем транзакцию
        #else:
            #print('Good1')
            #DB.commit() # Завершаем транзакцию
    else:
        print("commit")
        DB.commit() # Завершаем транзакцию
        
    
       
def Chit_nasrt():
    sp = [(1,0,0,''),\
            (2,0,0,''),\
            (3,0,0,''),\
            (4,0,0,''),\
            (5,0,25.0,''),\
            (6,0,1.0,''),\
            (7,0,0,''),\
            (8,1,0,'Фаза А'),\
            (9,1,0,'Фаза В'),\
            (10,1,0,'Фаза С'),\
            (11,1,0,'Трос'),
            (12,26,0,''),
            (13,18,0,''),
            (14,0,0,''),
            (15,0,100,''),
            (16,1,0,''),
            (17,1,0,''),
            (18,1,0,''),
            (19,1,0,''),
            (20,1,0,''),
            (21,2,0,''),
            (22,0,0,''),
            (23,5,0,''),
            (24,0,30.0,''),
            (25,0,0.5,''),
            (26,0,0.05,''),
            (27,1,0,''),
            (28,0,0,''),
            (29,0,0,''),
            (30,0,0,''),
            (31,0,0,'')]
    try:
        sql='SELECT * FROM Nastrouki'
        cur.execute(sql)
        arr=cur.fetchall()
        if len(arr) == 0: return sp
        else: return arr
    except:
        return sp 

# Добавать новую запись
def NewZap(Table,Name,Type):
    try:
        # Проверяем наличие такого имени в каталоге
        sql='SELECT * FROM '+Table+' WHERE Name=?'
        cur.execute(sql,[(Name)])
        arr=cur.fetchall()
        if len(arr)!=0:
            print('Имя занято')
            return  'Имя занято'
        # Ищем свободный id
        i=-1
        while True:
            i+=1
            sql='SELECT * FROM '+Table+' WHERE id=?'
            cur.execute(sql,[(i)])
            arr=cur.fetchall()
            if len(arr)==0:
                break
        # Дабавляем запись в таблицу
        sql_z='INSERT INTO '+Table+' VALUES (?,?,?)'
        if Table[:5]=='papk_' or Table[:5]=='file_':
            a=Table[5:]
        else:
            a=Table
        t=(i,Name,Type+a+'_'+str(i))
        cur.execute(sql_z,t)
        if Type=='papk_': 
            Papka(Type+a+'_'+str(i))
        elif Type=='file_':
            File(Type+a+'_'+str(i))
    except sqlite3.DatabaseError as err:
        print("Новая запись. Ошибка:", err)
    else:
        print('Новая запись. Запрос успешно выполнен')
        DB.commit() # Завершаем транзакцию
        return  t[2]

# Удалить запись
def DelZap(Table,Name):
    try:
        sql='SELECT * FROM '+Table+' WHERE Name=?'
        cur.execute(sql,[(Name)])
        arr=cur.fetchall()
        if len(arr)==0:
            print('Такой записи нет',arr)
            return None
        else:
            for i in range(len(arr)):
                sql_d="DELETE FROM "+Table+" WHERE id="+str(arr[i][0])
                cur.execute(sql_d)
                if arr[i][2][:5]=='papk_':
                    DelPapka(arr[i][2])
                elif arr[i][2][:5]=='file_':
                    DelFile(arr[i][2]) 
    except sqlite3.DatabaseError as err:
        print("Удаление. Ошибка:", err)
    else:
        print('Удаление. Запрос успешно выполнен')
        DB.commit() # Завершаем транзакцию

# Создание таблицы для новой папки
def Papka(Name):
    sql = """\
        CREATE TABLE """+Name+""" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Name_SQL TEXT
        );
        """
    try:                       # Обрабатываем исключения
        cur.executescript(sql) # Выполняем SQL-запросы
    except sqlite3.DatabaseError as err:
        print("Папка "+Name+". Ошибка:", err)
    else:
        print("Папка "+Name+". Создана")


#Удаление таблицы папки
def DelPapka(Name):
    sql='DROP TABLE '+Name
    try:                       # Обрабатываем исключения
        cur.executescript(sql) # Выполняем SQL-запросы
    except sqlite3.DatabaseError as err:
        print("Папка "+Name+". Ошибка:", err)
    else:
        print("Папка "+Name+". Удалена")
    

# Создаём таблыцы для файлов
def File(Name):
    sql = """\
        CREATE TABLE """+Name+"""_ivl (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t1 TEXT, t2 TEXT, t3 TEXT, t4 TEXT, t5 TEXT, t6 TEXT, t7 TEXT, t8 TEXT, t9 TEXT
        );    
        CREATE TABLE """+Name+"""_vvl (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t1 TEXT, t2 TEXT, t3 TEXT, t4 TEXT, t5 TEXT, t6 TEXT, t7 TEXT, t8 TEXT, t9 TEXT
        );
        CREATE TABLE """+Name+"""_zy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t1 TEXT, t2 TEXT, t3 TEXT, t4 TEXT, t5 TEXT, t6 TEXT, t7 TEXT, t8 TEXT
        );
        CREATE TABLE """+Name+"""_zytr (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t1 TEXT, t2 TEXT, t3 TEXT, t4 TEXT, t5 TEXT
        );
        CREATE TABLE """+Name+"""_zvl (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t1 TEXT, t2 TEXT, t3 TEXT, t4 TEXT, t5 TEXT, t6 TEXT, t7 TEXT, t8 TEXT, t9 TEXT
        );
        """
    try:                       # Обрабатываем исключения
        cur.executescript(sql) # Выполняем SQL-запросы
    except sqlite3.DatabaseError as err:
        print("файл "+Name+". Ошибка:", err)
    else:
        print("Файл "+Name+". Создан")

# Удаленые таблиц файла
def DelFile(Name):
    sql="""DROP TABLE """+Name+"""_ivl;
            DROP TABLE """+Name+"""_vvl;
            DROP TABLE """+Name+"""_zy;
            DROP TABLE """+Name+"""_zytr;
            DROP TABLE """+Name+"""_zvl;"""
    try:                       # Обрабатываем исключения
        cur.executescript(sql) # Выполняем SQL-запросы
    except sqlite3.DatabaseError as err:
        print("Файл "+Name+". Ошибка:", err)
    else:
        print("Файл "+Name+". Удалена")

# Содержание папок 
def SdPapk(Name):
    try:
        sql='SELECT * FROM '+Name
        cur.execute(sql)
        arr=cur.fetchall()
    except sqlite3.DatabaseError as err:
        print('Содержимое папки ошибка: ',err)
    else:
        print('Содержимое папки успешно прочитано')
        return arr

# Запапись данных в файл
def ZapFile(Name, ivl, vvl, zy, zytr, zvl):
    try:
        sql_z='INSERT INTO '+Name+'_ivl VALUES (?,?,?,?,?,?,?,?,?,?)'
        for i in range(len(ivl)):
            cur.execute(sql_z,(i,ivl[i][0],ivl[i][1],ivl[i][2],ivl[i][3],ivl[i][4],ivl[i][5],ivl[i][6],ivl[i][7],ivl[i][8]))
        sql_z='INSERT INTO '+Name+'_vvl VALUES (?,?,?,?,?,?,?,?,?,?)'
        for i in range(len(vvl)):
            cur.execute(sql_z,(i,vvl[i][0],vvl[i][1],vvl[i][2],vvl[i][3],vvl[i][4],vvl[i][5],vvl[i][6],vvl[i][7],vvl[i][8]))
        sql_z='INSERT INTO '+Name+'_zy VALUES (?,?,?,?,?,?,?,?,?)'
        for i in range(len(zy)):
            cur.execute(sql_z,(i,zy[i][0],zy[i][1],zy[i][2],zy[i][3],zy[i][4],zy[i][5],zy[i][6],zy[i][7]))
        sql_z='INSERT INTO '+Name+'_zytr VALUES (?,?,?,?,?,?)'
        for i in range(len(zytr)):
            cur.execute(sql_z,(i,zytr[i][0],zytr[i][1],zytr[i][2],zytr[i][3],zytr[i][4]))
        sql_z='INSERT INTO '+Name+'_zvl VALUES (?,?,?,?,?,?,?,?,?,?)'
        for i in range(len(zvl)):
            cur.execute(sql_z,(i,zvl[i][0],zvl[i][1],zvl[i][2],zvl[i][3],zvl[i][4],zvl[i][5],zvl[i][6],zvl[i][7],zvl[i][8]))
    except sqlite3.DatabaseError as err:
        print('Запись даннын в файл ошибка: ',err)
    else:
        print('Запись данных в файл успешно')
        DB.commit() # Завершаем транзакцию

# Считывание данных из файла
def ChitFile(Name):
    try:
        sql='SELECT * FROM '+Name+'_ivl'
        cur.execute(sql)
        ivl=cur.fetchall()
        for i in range(len(ivl)):
            ivl[i]=list(ivl[i])
            del ivl[i][0]
        sql='SELECT * FROM '+Name+'_vvl'
        cur.execute(sql)
        vvl=cur.fetchall()
        for i in range(len(vvl)):
            vvl[i]=list(vvl[i])
            del vvl[i][0]
        sql='SELECT * FROM '+Name+'_zy'
        cur.execute(sql)
        zy=cur.fetchall()
        for i in range(len(zy)):
            zy[i]=list(zy[i])
            del zy[i][0]
        sql='SELECT * FROM '+Name+'_zytr'
        cur.execute(sql)
        zytr=cur.fetchall()
        for i in range(len(zytr)):
            zytr[i]=list(zytr[i])
            del zytr[i][0]
        sql='SELECT * FROM '+Name+'_zvl'
        cur.execute(sql)
        zvl=cur.fetchall()
        for i in range(len(zvl)):
            zvl[i]=list(zvl[i])
            del zvl[i][0]
    except sqlite3.DatabaseError as err:
        print('Считывание файла ошибка: ',err)
    else:
        print('Считывание файла прошоло успешно')
        return ivl, vvl, zy, zytr, zvl

def ReName(Table,Name ,NewName):
    try:
        sql='SELECT * FROM '+Table+' WHERE Name=?'
        cur.execute(sql,[(NewName)])
        arr=cur.fetchall()
        if len(arr) !=0:
            return 'Имя занято'
   
        t=(NewName,Name)
        sql='UPDATE '+Table+' SET Name=? WHERE Name=?'
    
        cur.execute(sql,t)
    except sqlite3.DatabaseError as err:
        print("Переименование. Ошибка:", err)
    else:
        print('Переименование. Запрос успешно выполнен')
        DB.commit() # Завершаем транзакцию
    
        
        
        
def CloseBD():
    cur.close()                # Закрываем объект-курсор
    DB.close()                # Закрываем соединение
    print('Close')


a=[['1','2','3','4','5','6','7','8'],['9','10','11','12','13','14','15','16']]
b=[['18','17','16','15','14','13','12','11','10'],['9','8','7','6','5','4','3','2','1']]
c=[['10','9','8','7','6'],['1','2','3','4','5']]

#DelZap('Koren','Новая папка')
#NewZap('Koren','Папка 1','papk_')
#NewZap('papk_Koren_0_0','Файл 2','file_')
#DelZap('Koren','Папка 1')

#print(SdPapk('Koren'))
#ZapFile('file_Koren_0', a, b, a, c, b)
#print(ChitFile('file_Koren_0'))

#ReName('Koren','Файл 2' ,'Файл 4')
"""
sql='DROP TABLE '+'Nastrouki'
try:                       # Обрабатываем исключения
    cur.executescript(sql) # Выполняем SQL-запросы
except sqlite3.DatabaseError as err:
    print("Bad", err)
else:
    print("Good") 
"""

""" sp = [(1,0,0,''),\
            (2,0,0,''),\
            (3,0,0,''),\
            (4,0,0,''),\
            (5,0,25.0,''),\
            (6,0,1.0,''),\
            (7,0,0,''),\
            (8,1,0,'Фаза А'),\
            (9,1,0,'Фаза В'),\
            (10,1,0,'Фаза С'),\
            (11,1,0,'Трос'),
            (12,26,0,''),
            (13,18,0,''),
            (14,0,0,''),
            (15,0,100,''),
            (16,1,0,''),
            (17,1,0,''),
            (18,1,0,''),
            (19,1,0,''),
            (20,1,0,''),
            (21,2,0,''),
            (22,0,0,''),
            (23,5,0,''),
            (24,0,30.0,''),
            (25,0,0.5,''),
            (26,0,0.05,''),
            (27,1,0,''),
            (28,0,0,''),
            (29,0,0,''),
            (30,0,0,''),
            (31,0,0,'')]
Vvod_nasrt(sp)
CloseBD() """



