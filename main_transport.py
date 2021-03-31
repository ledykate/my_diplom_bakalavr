import sys
import math
import numpy as np
import numpy.ma as ma   #маски
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class Transport_main(QMainWindow): #класс, где храняться все действия
    def __init__(self): #служебная функция инициализации,загрузка окна
         QMainWindow.__init__(self)
         loadUi("main_gui.ui",self) #файл с расположение кнопок и виджета (должны находиться в одной папке)

         global click_pereschet
         click_pereschet=0 #переменная отвечающая за нажатие кнопки пересчёта
        
         self.spinBox_postavhik.valueChanged.connect(lambda: self.dinam_table(1)) #при изменении количества поставщиков меняется табличка
         self.spinBox_potrebitel.valueChanged.connect(lambda: self.dinam_table(2)) #при изменении количества потребителей меняется табличка
         self.spinBox_transport.valueChanged.connect(lambda: self.dinam_table(3)) #при изменении количества видов транспорта/перевозчиков меняется табличка
         self.pushButton_pereschet.clicked.connect(self.matrica_ocenok) #при нажатии на кнопку "пересчитать" происходит пересчёт
         self.pushButton_result.clicked.connect(self.results_tz) #при нажатии на кнопку "решить" происходит поиск решения и считается целевая функция
         
         self.spinBox_postavhik.setMinimum(2) #минимальное количество поставщиков
         self.spinBox_postavhik.setMaximum(10) #максимальное количество поставщиков

         self.spinBox_potrebitel.setMinimum(2) #минимальное количество потребителей
         self.spinBox_potrebitel.setMaximum(10) #максимальное количество потребителей

         self.spinBox_transport.setMinimum(2) #минимальное количество перевозчиков/видов транспорта
         self.spinBox_transport.setMaximum(10) #максимальное количество перевозчиков/видов транспорта

         val_postavhik = self.spinBox_postavhik.value() #считываение заданного количества поставщиков при загрузке (для таблиц стоим. матрицы, пересчёта, решения)
         val_potrebitel = self.spinBox_potrebitel.value() #считываение заданного количества потребителей при загрузке (для таблиц стоим. матрицы, пересчёта, решения)
         val_transport = self.spinBox_transport.value() #считываение заданного количества перевозчиков/видов транспорта при загрузке (для таблиц стоим. матрицы, пересчёта, решения)
         
         self.update_table() #обновить таблицы
         
         #для создание счётчиков для ячеек с показателями качества
         for i in range(val_transport): #считывание количества видов транспорта (проход по строкам)
            item = QtWidgets.QTableWidgetItem() #для кадой строки создаются ячейчки
            item.setTextAlignment(QtCore.Qt.AlignCenter) #выравнивание по центру самих ячеек
            self.tableWidget_transport.setItem(i, 5, item) #обновление ячейки
            for j in range(5):
                #показатели качества - счётчики
                spbox_transport = QtWidgets.QSpinBox() #создаём виджет спибокс - счётчик
                spbox_transport.setMinimum(1) #минимальное в нём значение 1
                spbox_transport.setMaximum(5) #максимальное в нём значение 5
                spbox_transport.setProperty("value", 3) #значение по умолчанию
                spbox_transport.setProperty("alignment", "AlignHCenter") #выравниваем по ценру
                self.tableWidget_transport.setCellWidget(i, j, spbox_transport) #вставляем в табличку с транспортом эти счётчики
                cell = QtWidgets.QTableWidgetItem() #пересоздание ячейки
                cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем их
                cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрет на редактирование
                self.tableWidget_transport.setItem(i - 1, 0, cell) #спинбокс/счётчки центрируются
###------------------------------------------------------------------------------------------------------------------------
    def my_coord(self,element, matrix): #поиск координат (номер строки и столбца) в матрице
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == element:
                    return (i, j)
###--------------------------------------------------------------------------------------------------------------------
    def dinam_table(self,din): #динамическое обновление таблиц поставщиков/потребителей/транспортов
        if din == 1: #динамическое обновление таблицы с поставщиками
            #print("Динамически меняем объемы поставщиков")
            value_spinBox_postavhik = self.spinBox_postavhik.value() #считываем значение поставщиков
            self.tableWidget_postavhik.setRowCount(value_spinBox_postavhik) #задание количества строк с учётом выбраного количества поставщиков
            Z_postavhik = [] #заголовки поставщиков - массик
            for i in range(1, value_spinBox_postavhik+1): #от 1 до количества поставщиков (введеного)
                Z_postavhik.append("A" + str(i)) #добавляем название
            self.tableWidget_postavhik.setVerticalHeaderLabels(Z_postavhik) #заголовки в талице поставщиков
            cell = QtWidgets.QTableWidgetItem() #ячейка пересоздаётся
            cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрирцем 
            self.tableWidget_postavhik.setItem(i-1, 0, cell) #выполнение с координатами ячеек
            self.update_table() #обновление всех таблиц (больших)
        
        elif din == 2:#динамическое обновление таблицы с потребителями
            #аналогичнос поставщикам, но для потребителей
            value_spinBox_potrebitel = self.spinBox_potrebitel.value() #считывание количества потребителей
            self.tableWidget_potrebitel.setRowCount(value_spinBox_potrebitel) #изменение количесства строк
            Z_potrebitel = [] #массив заголовков
            for j in range(1, value_spinBox_potrebitel+1):
                Z_potrebitel.append("B" + str(j))
            self.tableWidget_potrebitel.setVerticalHeaderLabels(Z_potrebitel) #отображение заголовков
            cell = QtWidgets.QTableWidgetItem() #пересоздание ячеек
            cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрирование
            self.tableWidget_potrebitel.setItem(j-1, 0, cell) #загружаем ячейку в таблицу
            self.update_table() #обновление таблиц (больших)
        
        elif din == 3:#динамическое обновление таблицы с видами транспортами/перевозчиками
            value_spinBox_transport = self.spinBox_transport.value()  #считываем количество видов транспорта
            self.tableWidget_transport.setRowCount(value_spinBox_transport) #измение количества строк в табличце с транспортами
            Z_transport = [] #масси с заголовками
            for k in range(1, value_spinBox_transport+1):
                Z_transport.append("P" + str(k))
            self.tableWidget_transport.setVerticalHeaderLabels(Z_transport) #отображение заголовков
            for k1 in range(5):
                #для создание спибоксов/счётчиков
                spbox_transport = QtWidgets.QSpinBox() #создаём виджет спибокс - счётчик
                spbox_transport.setMinimum(1) #минимальное значение
                spbox_transport.setMaximum(5) #максильное значение
                spbox_transport.setProperty("value", 3) #по умолчанию
                spbox_transport.setProperty("alignment", "AlignHCenter") #центрируем
                self.tableWidget_transport.setCellWidget(value_spinBox_transport-1, k1, spbox_transport) #вставляем этот спинбокс в ячейку
                cell = QtWidgets.QTableWidgetItem() #пересоздаём
                cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                self.tableWidget_transport.setItem(value_spinBox_transport - 1, 0, cell) #загружаем
            #для каждой строки
            cell = QtWidgets.QTableWidgetItem() #перевоздаём 
            cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
            self.tableWidget_transport.setItem(value_spinBox_transport-1, 5, cell) #загружаем
            self.update_table() #обновляем большие таблицы
###------------------------------------------------------------------------------------------------------------------
    def update_table_schet(self): #очистка таблицы с результатом 
        #очищение таблиц
        self.tableWidget_result.clearSpans() #таблица "решение"
        #считывание количества со спинбоксов/счётчиков:
        val_postavhik = self.spinBox_postavhik.value() #поставщиков
        val_potrebitel = self.spinBox_potrebitel.value() #потребителей
        val_transport = self.spinBox_transport.value()  #видов транспортов/перевозчиков
        #обновление таблиц по строкам, первые две строки - это заголовки для Bj и Pk
        self.tableWidget_result.setRowCount(2+val_postavhik) #таблица "решение"
        #обновление таблиц по столбцам, первый столбец - заголовки для Ai
        #общее количество столбцо это количество потребителей * количество видов транспорта/поставщиков
        self.tableWidget_result.setColumnCount(val_potrebitel*val_transport + 1) #таблица "решение"
        #объедение верхний левый угол в каждой из таблиц
        self.tableWidget_result.setSpan(0, 0, 2, 1)
        #строки А
        row_post = 2 #отсчёт с 2, т.к. со второй строки всех таблиц записываются Ai
        for i in range(0,val_postavhik): #по каждой строке
            name="A" + str(i+1) #формируем заголов строки
            new_cell = QTableWidgetItem(name) #формируем ячейку с именем
            new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем это имя
            new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать
            color_post = QtGui.QBrush(QtGui.QColor(190, 190, 190)) #задаём цвет ячейки
            color_post.setStyle(QtCore.Qt.SolidPattern) #выбираем способ заливки - сплошной
            new_cell.setBackground(color_post) #закрашиваем ячейку выбранным цветом и заливкой
            w_post = QtGui.QFont() #шрифт
            w_post.setBold(True) #жирный
            w_post.setWeight(75) #задаём размер
            new_cell.setFont(w_post) #задаём это для кадой ячейки
                #записываем это в каждую из таблиц
                #if j==3:
            self.tableWidget_result.setItem(row_post, 0, new_cell) #матрица с решением
            row_post=row_post+1 #переход на следующую строку
        #столбцы B
        col_potr = 1 #отсчёт с 1, т.к. 0 столбце -это заголовки для поставщиков
        for i in range(0,val_potrebitel): #по каждой группе столбцов потребителей
            #объеденеие левого верхнего угла в разных таблицах
            self.tableWidget_stoimosti.setSpan(0,col_potr,1,val_transport) #стоимостная матрица
            self.tableWidget_pereschet.setSpan(0,col_potr,1,val_transport) #пересчитанная матрица
            self.tableWidget_result.setSpan(0,col_potr,1,val_transport) #матрица с результатом
            name="B" + str(i+1) #формируем имя заголовка
            new_cell = QTableWidgetItem(name) #формируем ячейку с именем
            new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
            new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать
            color_potr = QtGui.QBrush(QtGui.QColor(190, 190, 190)) #цвет
            color_potr.setStyle(QtCore.Qt.SolidPattern) #заливка
            new_cell.setBackground(color_potr) #закрашиваем
            w_potr = QtGui.QFont() #шрифт
            w_potr.setBold(True) #жирный
            w_potr.setWeight(75) #размер
            new_cell.setFont(w_potr) #задаём для каждой ячейки
            self.tableWidget_result.setItem(0,col_potr,new_cell)#матрица с решением
            col_potr=col_potr+val_transport  
        #столбцы P
        col_tran=1 #отсчёт с 1, т.к. 0 столбце -это заголовки для поставщиков
        for i in range(0, val_potrebitel): #проход по каждой группе поребителей
            for j in range(0,val_transport): #проход по каждому виду транспорта
                name = "P" + str(j+1) #имя заголовка
                new_cell = QTableWidgetItem(name) #ячейка с этим именем
                new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать 
                color_tran = QtGui.QBrush(QtGui.QColor(235, 235, 235)) #цвет
                color_tran.setStyle(QtCore.Qt.SolidPattern) #заливка
                new_cell.setBackground(color_tran) #закрашиваем
                w_tran = QtGui.QFont() #шрифт
                w_tran.setBold(True) #жирный
                w_tran.setWeight(75) #размер
                new_cell.setFont(w_tran) #применяем
                self.tableWidget_result.setItem(1,col_tran,new_cell) #матрица с решением
                col_tran = col_tran + 1
        #центрировани надписей (именно где сами значения)
        for i in range(2, val_postavhik+2): #по строкам
            for j in range(1, val_potrebitel * val_transport+1): #по всем столбцам
                cell=QtWidgets.QTableWidgetItem() #пустые ячейки
                cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                self.tableWidget_result.setItem(i,j,cell) #матрица с решением
        #растяжение последнего столбца не применяется
        self.tableWidget_result.horizontalHeader().setStretchLastSection(False)
        self.textEdit_celevaya.clear()
###---------------------------------------------------------------------------------------------------------------
    def update_table(self): #обновление таблиц - отображение в окне
        #очищение таблиц
        self.tableWidget_stoimosti.clearSpans() #таблица "стоимостная матрица"
        self.tableWidget_pereschet.clearSpans() #таблица "матрица оценок"
        self.tableWidget_result.clearSpans() #таблица "решение"
        
        #считывание количества со спинбоксов/счётчиков:
        val_postavhik = self.spinBox_postavhik.value() #поставщиков
        val_potrebitel = self.spinBox_potrebitel.value() #потребителей
        val_transport = self.spinBox_transport.value()  #видов транспортов/перевозчиков
        
        #обновление таблиц по строкам, первые две строки - это заголовки для Bj и Pk
        self.tableWidget_stoimosti.setRowCount(2+val_postavhik) #таблица "стоимостная матрица"
        self.tableWidget_pereschet.setRowCount(2+val_postavhik) #таблица "матрица оценок"
        self.tableWidget_result.setRowCount(2+val_postavhik) #таблица "решение"
        
        #обновление таблиц по столбцам, первый столбец - заголовки для Ai
        #общее количество столбцо это количество потребителей * количество видов транспорта/поставщиков
        self.tableWidget_stoimosti.setColumnCount(val_potrebitel*val_transport+1) #таблица "стоимостная матрица"
        self.tableWidget_pereschet.setColumnCount(val_potrebitel*val_transport + 1) #таблица "матрица оценок"
        self.tableWidget_result.setColumnCount(val_potrebitel*val_transport + 1) #таблица "решение"
        
        #объедение верхний левый угол в каждой из таблиц
        self.tableWidget_stoimosti.setSpan(0, 0, 2, 1)
        self.tableWidget_pereschet.setSpan(0, 0, 2, 1)
        self.tableWidget_result.setSpan(0, 0, 2, 1)

        #строки А
        row_post = 2 #отсчёт с 2, т.к. со второй строки всех таблиц записываются Ai
        for i in range(0,val_postavhik): #по каждой строке
            for j in range(1,4): #пкаждой большой таблицы (их всего 3)
                name="A" + str(i+1) #формируем заголов строки
                new_cell = QTableWidgetItem(name) #формируем ячейку с именем
                new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем это имя
                new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать
                color_post = QtGui.QBrush(QtGui.QColor(190, 190, 190)) #задаём цвет ячейки
                color_post.setStyle(QtCore.Qt.SolidPattern) #выбираем способ заливки - сплошной
                new_cell.setBackground(color_post) #закрашиваем ячейку выбранным цветом и заливкой
                w_post = QtGui.QFont() #шрифт
                w_post.setBold(True) #жирный
                w_post.setWeight(75) #задаём размер
                new_cell.setFont(w_post) #задаём это для кадой ячейки
                #записываем это в каждую из таблиц
                if j==1:
                    self.tableWidget_stoimosti.setItem(row_post, 0, new_cell) #стоимостная матрица
                elif j==2:
                    self.tableWidget_pereschet.setItem(row_post, 0, new_cell) #пересчитанная матрица
                elif j==3:
                    self.tableWidget_result.setItem(row_post, 0, new_cell) #матрица с решением
            row_post=row_post+1 #переход на следующую строку

        #столбцы B
        col_potr = 1 #отсчёт с 1, т.к. 0 столбце -это заголовки для поставщиков
        for i in range(0,val_potrebitel): #по каждой группе столбцов потребителей
            #объеденеие левого верхнего угла в разных таблицах
            self.tableWidget_stoimosti.setSpan(0,col_potr,1,val_transport) #стоимостная матрица
            self.tableWidget_pereschet.setSpan(0,col_potr,1,val_transport) #пересчитанная матрица
            self.tableWidget_result.setSpan(0,col_potr,1,val_transport) #матрица с результатом
            for j in range(1,4): #проход по каждой из таблиц
                name="B" + str(i+1) #формируем имя заголовка
                new_cell = QTableWidgetItem(name) #формируем ячейку с именем
                new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать
                color_potr = QtGui.QBrush(QtGui.QColor(190, 190, 190)) #цвет
                color_potr.setStyle(QtCore.Qt.SolidPattern) #заливка
                new_cell.setBackground(color_potr) #закрашиваем
                w_potr = QtGui.QFont() #шрифт
                w_potr.setBold(True) #жирный
                w_potr.setWeight(75) #размер
                new_cell.setFont(w_potr) #задаём для каждой ячейки
                #записываем это в каждую из таблиц
                if j==1:
                    self.tableWidget_stoimosti.setItem(0,col_potr,new_cell) #стоимостная матрица
                elif j==2:
                    self.tableWidget_pereschet.setItem(0,col_potr,new_cell) #пересчитанная матрица
                elif j==3:
                    self.tableWidget_result.setItem(0,col_potr,new_cell)#матрица с решением
            col_potr=col_potr+val_transport
            
        #столбцы P
        col_tran=1 #отсчёт с 1, т.к. 0 столбце -это заголовки для поставщиков
        for i in range(0, val_potrebitel): #проход по каждой группе поребителей
            for j in range(0,val_transport): #проход по каждому виду транспорта
                for k in range(1, 4): #проход по каждой таблице
                    name = "P" + str(j+1) #имя заголовка
                    new_cell = QTableWidgetItem(name) #ячейка с этим именем
                    new_cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                    new_cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать 
                    color_tran = QtGui.QBrush(QtGui.QColor(235, 235, 235)) #цвет
                    color_tran.setStyle(QtCore.Qt.SolidPattern) #заливка
                    new_cell.setBackground(color_tran) #закрашиваем
                    w_tran = QtGui.QFont() #шрифт
                    w_tran.setBold(True) #жирный
                    w_tran.setWeight(75) #размер
                    new_cell.setFont(w_tran) #применяем
                    #записываем это в каждую из таблиц
                    if k == 1:
                        self.tableWidget_stoimosti.setItem(1,col_tran,new_cell) #стоимостная матрица
                    elif k == 2:
                        self.tableWidget_pereschet.setItem(1,col_tran,new_cell) #пересчитанная матрица
                    elif k == 3:
                        self.tableWidget_result.setItem(1,col_tran,new_cell) #матрица с решением
                col_tran = col_tran + 1
                
        #центрировани надписей (именно где сами значения)
        for i in range(2, val_postavhik+2): #по строкам
            for j in range(1, val_potrebitel * val_transport+1): #по всем столбцам
                for k in range(1,4): #по каждой таблице
                    cell=QtWidgets.QTableWidgetItem() #пустые ячейки
                    cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                    #применяем к каждой таблице
                    if k == 1:
                        self.tableWidget_stoimosti.setItem(i,j,cell) #стоимостная матрица
                    elif k == 2:
                        self.tableWidget_pereschet.setItem(i,j,cell) #пересчитанная матрица
                    elif k == 3:
                        self.tableWidget_result.setItem(i,j,cell) #матрица с решением

        #растяжение последнего столбца не применяется
        self.tableWidget_stoimosti.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_pereschet.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_result.horizontalHeader().setStretchLastSection(False)
        self.textEdit_celevaya.clear()
####--------------------------------------------------------------------------------------------------------------        
    def matrica_ocenok(self): #пересчёт стоимостной матрицы
        global C, C_shtrih #объявление глобальных матриц С и С штрих
        global Ai, Bj, Pk
        global val_postavhik, val_potrebitel, val_transport
        global click_pereschet
        
        summa_Ai = 0 #сумма объёмов поставщиков
        summa_Bj = 0 #сумма объёма потребителей
        summa_Pk = 0 #сумма мощностей перевозчиков/транспорта
        error_Ai = 0 #ошибки на пустоту поставщиков
        error_Bj = 0 #ошибки на пустоту потребителей
        error_Pk = 0 #ошибка по пустоту мощности транспорта
        error_Pk1 = 0 #ошибка на сумму мощностей транспорта
        error_Cijk = 0 #ошибка на пустоту стоимостей

        PK = []  #сумарный показатель качества ПК
        PK_shtrih = [] #пересчитанный показатель качества ПК штрих
        PK_max = 25 #максимлаьное изначальное значение показателя качества ПК

        val_postavhik = self.spinBox_postavhik.value()  #считываем количество поставщиков
        val_potrebitel = self.spinBox_potrebitel.value() #считываем количество потребителей
        val_transport = self.spinBox_transport.value()  #считываем количество транспорта

        Ai=[] #значения объёмов поставщиков
        for i in range(0, val_postavhik): #проход по строкам таблицы с объёмами поставщиков
            A_i=self.tableWidget_postavhik.item(i,0).text() #значение объёма
            if A_i=='' or A_i.isdigit()==False: #если пустой
                error_Ai=error_Ai+1 #ошибка
            else: #не пустой
                Ai.append(float(A_i)) #добавляем значение в массив
                summa_Ai = summa_Ai + float(A_i) #находим сумму

        Bj=[] #значение объёмов потребителей
        for j in range(0, val_potrebitel): #проход по тсрокам таблицы с объёмами постребителей
            B_j=self.tableWidget_potrebitel.item(j,0).text() #считываем значение объёма
            if B_j=='' or B_j.isdigit()==False: #если пусто
                error_Bj = error_Bj + 1 #ошибка
            else: #не пустая
                Bj.append(float(B_j)) #добавляем в массив
                summa_Bj = summa_Bj + float(B_j) #суммируем

        Pk=[] #значение мощности транспорта/перевозчика
        for i in range(0, val_transport): #проход по строкам с транспортами
            P_k=self.tableWidget_transport.item(i,5).text() #считываем мощность (последний столбец)
            if P_k=='' or P_k.isdigit()==False: #если пустая ячейка
                error_Pk = error_Pk + 1 #ошибка
            else:
                if float(P_k)>=summa_Ai: #если значение больше перевозимого объёма
                    error_Pk1 = error_Pk1+1 #ошибка
                else:
                    Pk.append(float(P_k)) #добавляем в массив
                    summa_Pk = summa_Pk + float(P_k) #суммируем

        Cijk = [] #массив со всеми стоимостями
        C = np.zeros([val_postavhik,val_potrebitel*val_transport])  #матрица стоимостей
        C_shtrih = np.zeros([val_postavhik,val_potrebitel*val_transport])#матрица пересчёта

        for i in range(2, val_postavhik+2):  #со второй строки таблицы
            for j in range(1, val_potrebitel*val_transport+1): #с первого столбца таблицы
                c_ijk = self.tableWidget_stoimosti.item(i, j).text() #считываем введёные стоимости
                if c_ijk == '' or c_ijk.isdigit()==False: #если пустая
                    error_Cijk = error_Cijk + 1 #ошибка
                else:
                    C[i - 2][j - 1] = float(c_ijk) #преобразуем
                    Cijk.append(float(c_ijk)) #добавляем
        ###пересчёт
        if error_Ai==0 and error_Bj==0 and error_Pk==0 and error_Cijk==0: #без ошибок
            if all(i!=0 for i in Ai): #если все значение объёмов поставщиков не равны 0
                if all(i!=0 for i in Bj):  #если все значение объёмов потребителей не равны 0
                    if all(i!=0 for i in Pk): #если все значение мощностей транспортнрй не равны 0
                        if all(i!=0 for i in Cijk): #в стоимостной матрице нет нулевых значений
                            if summa_Ai==summa_Bj: #проверка объёма перевозимого груза - правильный баланс
                                if error_Pk1==0: #нельзя перевезти одним транспортом
                                    if summa_Pk>=summa_Ai: #сумма мощностей транспорта больше либо равна объёму перевозимого груза
                                        Cmax = max(Cijk) #максимальная стоимость
                                        for i in range (0,val_transport): #для каждого транспорта
                                            summa_pk=0
                                            for j in range (0,5):
                                                kriter=self.tableWidget_transport.cellWidget(i,j) #считываем значени показателя со спибокса/счётчика
                                                summa_pk=summa_pk+kriter.value() #находим показатель качества для данного транспорта
                                            PK.append(summa_pk) #показатель качества
                                            pk_sh=(summa_pk/PK_max)*Cmax #пересчёт
                                            PK_shtrih.append(pk_sh) #добавляем пересчитанный в массив
                                        for k in range(0,val_transport):#по каждому транспорту
                                            for i in range(2,val_postavhik+2): #по каждой строке
                                                for j in range(1+k, val_potrebitel*val_transport+1,val_transport):#проход по ячейкам транспорта
                                                    c_ijk = self.tableWidget_stoimosti.item(i, j).text() #считывание
                                                    c_ijk_sh=float(np.sqrt(int(c_ijk)**2+(Cmax-PK_shtrih[k])**2)) #новая оценка
                                                    c_ijk_sh_r=round(c_ijk_sh,5) #округление
                                                    C_shtrih[i-2][j-1] = c_ijk_sh #запись в матрицу
                                                    cell = QTableWidgetItem(str(c_ijk_sh_r)) #преобразуем значение в ячейку
                                                    cell.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать
                                                    self.tableWidget_pereschet.setItem(i, j, cell) #отображаем
                                        click_pereschet=1 #пересчёт выполнен
                                        self.reply = QMessageBox.information(self, 'Сообщение',"Пересчёт выполнен")
                                    else:
                                        self.reply = QMessageBox.information(self, 'Сообщение',
                                        "Должно выполняться условие о количестве перевозимого груза.\nСумма мощностей всех видов транспорта >= Суммы перевозимого груза")
                                else:
                                    self.reply = QMessageBox.information(self, 'Сообщение',
                                    "Нельзя перевезти груз только одинм транспортом.\nМощность каждого транспорта < суммы перевозимого груза")
                            else:
                                self.reply = QMessageBox.information(self, 'Сообщение',
                                "Транспортная задача должна быть с правильным балансом.\nОбъёмы поставщиков=объёму потребителей")
                        else:
                            self.reply = QMessageBox.information(self, 'Сообщение',
                            "Проверьте стоимостную матрицу.\nТаблица должна быть заполненена ненулевыми значениями.")
                    else:
                        self.reply = QMessageBox.information(self, 'Сообщение',
                        "Проверьте таблицу транспортов.\nТаблица должна быть заполненена ненулевыми значениями.")
                else:
                    self.reply = QMessageBox.information(self, 'Сообщение',
                    "Проверьте таблицу потребителей.\nТаблица должна быть заполненена ненулевыми значениями.")
            else:
                self.reply = QMessageBox.information(self, 'Сообщение',
                "Проверьте таблицу поставщиков.\nТаблица должна быть заполненена ненулевыми значениями.")
        else:
            self.reply = QMessageBox.information(self, 'Сообщение',
            "В таблицах имеются пустные ячейки или где-то есть не число.\nПроверьте ещё раз на заполненость.")
            #обнуление
            error_Ai = 0 #ошибки на пустоту поставщиков
            error_Bj = 0 #ошибки на пустоту потребителей
            error_Pk = 0 #ошибка по пустоту мощности транспорта
            error_Pk1 = 0 #ошибка на введённое значение
            error_Cijk = 0 #ошибка на пустоту стоимостей
#-------------------------------------------------------------------
    def results_tz(self): #функция для решения
        global click_pereschet
        if click_pereschet==1: #пересчёт произведён
            self.update_table_schet()
            #копируем данные объёмы и мощности для сравнивания
            Ai_0 = Ai    
            Bj_0 = Bj
            Pk_0 = Pk
            ijk=val_potrebitel*val_transport #общий объём - количество всех ячеек со стоимостями
            Rez = np.zeros((val_postavhik, ijk)) #матрица решения - заполняем нулями

            flag=1 #условия для цикла
            while flag==1:
                #поиск ненулевых значений
                cijk_min_sht=np.min(ma.masked_where(C_shtrih==0,C_shtrih)) #ищем минимальное ненулевое значение
                ind=self.my_coord(cijk_min_sht,C_shtrih) #находим координаты (номер строки столбца)
                ind_row = ind[0]+1  #строка этого элемента
                ind_col = ind[1]+1  #столбец столбец этого элемента
                ind_A = ind_row #индекс однозначного определения строки
                ind_B = math.ceil((ind_col/val_transport)) #в какую группу Bj попал элемент
                ind_P=ind_col-(ind_B-1)*val_transport #из индекса отбрасываем первые группы Bj для определения группы Pi

                znach=[Ai_0[ind_A-1],Bj_0[ind_B - 1],Pk_0[ind_P - 1]] #элементы из которых будем выбираем минимальный элемент A,B,P
                min_znach=np.min(znach) #выбор минимального из этих элементов
                
                cell = QTableWidgetItem(str(min_znach)) #ячейка с минимальным значением
                cell.setTextAlignment(QtCore.Qt.AlignCenter) #центрируем
                cell.setFlags(QtCore.Qt.ItemIsEnabled) #нельзя редактировать
                self.tableWidget_result.setItem(ind_row+1,ind_col,cell) #вставка этого значения в таблицу с результами

                Rez[ind_row-1][ind_col-1]=min_znach #запись найденого элемента в матрицу
                
                #вычитаем этот элемент
                Ai_0[ind_A-1] = Ai_0[ind_A-1]-min_znach 
                Bj_0[ind_B-1] = Bj_0[ind_B-1]-min_znach
                Pk_0[ind_P-1] = Pk_0[ind_P-1]-min_znach

                if Ai_0[ind_A-1]==0: #если исчерпана
                    C_shtrih[ind_row-1][:]=0 #обнуляем строкц 

                if Bj_0[ind_B-1]==0: 
                    for i in range(0,val_postavhik):
                        C_shtrih[i][(ind_B-1)*val_transport:(ind_B)*val_transport] = 0 #обнуление группы Bj

                if Pk_0[ind_P-1]==0: #если исчерпан 
                    kt=0 #переход по транспорту который обнулился
                    for i in range (0,val_potrebitel):
                        for j in range(0,val_postavhik):
                            C_shtrih[j][ind_P-1+kt]=0 #обнуляем
                        kt=kt+val_transport
                        i=i+1
                #проверка остановки алгоритма 
                if all(i == 0 for i in Ai_0) and all(i == 0 for i in Bj_0):
                    flag=0 # Переменная остановки. Если в алгоритме она становится =0, то выходим из цикла while
                    click_pereschet=0
            #подсчёт целевой функции
            Z=0
            for i in range(0,val_postavhik):
                for j in range (0,val_potrebitel * val_transport):
                    Z=Z+C[i][j]*Rez[i][j]
            self.textEdit_celevaya.setText(str(Z))
            self.reply = QMessageBox.information(self, 'Message', "Расчёт готов")
            click_pereschet=0
        else:
            self.update_table_schet()
            self.reply = QMessageBox.information(self, 'Сообщение',
            "Сначала необходимо подсчитать модифицированную матрицу оценок")
###-----------------------------------------------------------------------------------------
#вызов окна 
if __name__ == '__main__': 
   app = QApplication(sys.argv) 
   form = Transport_main() 
   form.show() 
   app.exec() 