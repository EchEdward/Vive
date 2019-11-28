from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout,QLabel,QHBoxLayout, qApp, QTableWidget,\
    QTableWidgetItem
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage, QIcon
from PyQt5.QtCore import Qt
import sys



class KOp(QWidget):
    def __init__(self,parent=None):
        super(KOp,self).__init__(parent)
        self.setWindowIcon(QIcon('Pictures/icon.jpg'))
    def KonfOp(self,k,i,To):
        self.setFixedSize(500,500)
        self.setWindowTitle('Конфигурация опоры: '+To)
        pal = QPalette()
        img = QImage('Op_Fig/'+str(k)+str(i)+'.jpg')
        scaled = img.scaled(self.size(), Qt.IgnoreAspectRatio, transformMode = Qt.SmoothTransformation)
        pal.setBrush(QPalette.Normal,QPalette.Window, QBrush(scaled))
        self.setPalette(pal)
    def Program_info(self):
        self.setFixedSize(650,365)
        self.setWindowTitle('O программе')
        pal = QPalette()
        img = QImage('Pictures/Program_info.jpg')
        scaled = img.scaled(self.size(), Qt.IgnoreAspectRatio, transformMode = Qt.SmoothTransformation)
        pal.setBrush(QPalette.Normal,QPalette.Window, QBrush(scaled))
        self.setPalette(pal)
    def Spisok(self,sp):

        self.resize(500,500)
        self.setWindowTitle("Cписок ВЛ")

        V_layout = QVBoxLayout()
        self.setLayout(V_layout)

        table = QTableWidget(self)
        table.setColumnCount(1)
        table.setRowCount(len(sp))

        table.setHorizontalHeaderLabels([ "Наименование добаленых файлов"]) #"№",

        for i in range(len(sp)):
            #table.setItem(i, 0, QTableWidgetItem(str(sp[i][0])))
            table.setItem(i, 0, QTableWidgetItem(sp[i]))

        table.resizeColumnsToContents()
        V_layout.addWidget(table)   # Добавляем таблицу в сетку

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KOp() # Создаём экземпляр класса
    window.show() # Отображаем окно
    sys.exit(app.exec_()) # Запускаем цикл обработки событий
