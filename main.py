import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from gui import Ui_MainWindow
import os
from os import environ
import csv
from pandas import read_csv
from functools import partial
from DanhSachLienKet import *
import random


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


listThuatToanSapXep = ["Sắp xếp chọn",
                       "Sắp xếp chèn",
                       "Sắp xếp nổi bọt",
                       "QuickSort",
                       "MergeSort"]

listKhoaSapXep = ["Mã lớp",
                  "Mã sinh viên",
                  "Họ và tên",
                  "Ngày sinh",
                  "Điểm trung bình tích lũy"]

listKhoaTimKiem = ["Tìm kiếm tuần tự", "Tìm kiếm nhị phân"]

listColor = ['#fb2410', '#62aa2d', '#f99300', '#0244fc', '#fb4f05',
             '#028cca', '#f6b600', '#3d009e', '#fcfb2d', '#8400ab', '#cbe426', '#a31746']
lstXepLoai = {'XuatSac': "Xuất sắc", 'Gioi': "Giỏi", 'Kha': "Khá",
              'TrungBinh': "Trung Bình", 'Yeu': "Yếu", 'Kem': "Kém"}


def xor(s):
    s = str(s)
    key = [110, 221, 342, 564, 212]
    answer = ""
    for i, c in enumerate(s):
        if (ord(c) ^ key[i % len(key)]) != 0:
            answer += chr((ord(c) ^ key[i % len(key)]))
        else:
            answer += c
    return answer


class QuanLySinhVien(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.stackedWidget.setCurrentWidget(self.home)
        self.stackedWidget.setCurrentWidget(self.home)
        self.pathData = 'Data'
        self.handle_gui()
        self.handle_action()
        self.listData = []
        self.thuatToan = -1
        self.keySort = -1
        self.keySearch = -1
        self.llist = LinkedList()
        self.loadData()
        self.listClass = []
        self.indexChartClass = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2000)
        self.indexAnimationChart = 0

    def gui_ThemHoSo(self):
        font = QtGui.QFont()
        font.setPointSize(16)
        self.maLop_ThemHoSo.setFont(font)
        self.maLop_ThemHoSo.setPlaceholderText('BDATTT')
        self.maSinhVien_ThemHoSo.setFont(font)
        self.maSinhVien_ThemHoSo.setValidator(QtGui.QIntValidator())
        self.maSinhVien_ThemHoSo.setPlaceholderText('36')
        self.hoTen_ThemHoSo.setFont(font)
        self.hoTen_ThemHoSo.setPlaceholderText('Nguyễn Văn A')
        self.ngaySinh_ThemHoSo.setFont(font)
        self.DTB_ThemHoSo.setFont(font)
        self.maLop_ThemHoSo.setAlignment(QtCore.Qt.AlignCenter)
        self.maSinhVien_ThemHoSo.setAlignment(QtCore.Qt.AlignCenter)
        self.hoTen_ThemHoSo.setAlignment(QtCore.Qt.AlignCenter)
        self.ngaySinh_ThemHoSo.setAlignment(QtCore.Qt.AlignCenter)
        # self.ngaySinh_ThemHoSo.setInputMask('00   /   00   /   0000')
        self.ngaySinh_ThemHoSo.setPlaceholderText('01/01/2001')
        self.DTB_ThemHoSo.setAlignment(QtCore.Qt.AlignCenter)
        self.DTB_ThemHoSo.setValidator(QtGui.QDoubleValidator(0.1, 10, 1))
        self.DTB_ThemHoSo.setPlaceholderText('10.0')

    def handle_gui(self):
        self.setWindowTitle("Quản lý sinh viên")
        # self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setFixedSize(1590, 871)

        self.gui_ThemHoSo()

        self.tableWidget.setColumnWidth(0, 160)
        self.tableWidget.setColumnWidth(1, 210)
        self.tableWidget.setColumnWidth(2, 360)
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setColumnWidth(4, 195)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.table_SapXep.setColumnWidth(0, 160)
        self.table_SapXep.setColumnWidth(1, 210)
        self.table_SapXep.setColumnWidth(2, 360)
        self.table_SapXep.setColumnWidth(3, 200)
        self.table_SapXep.setColumnWidth(4, 195)
        self.table_SapXep.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.searchTable_TimKiem.setColumnWidth(0, 160)
        self.searchTable_TimKiem.setColumnWidth(1, 210)
        self.searchTable_TimKiem.setColumnWidth(2, 360)
        self.searchTable_TimKiem.setColumnWidth(3, 200)
        self.searchTable_TimKiem.setColumnWidth(4, 195)
        self.searchTable_TimKiem.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.inputSearch_TimKiem.setAlignment(QtCore.Qt.AlignCenter)

        self.table1_ThongKe.setColumnWidth(0, 170)
        self.table1_ThongKe.setColumnWidth(1, 170)
        self.table1_ThongKe.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

    def handle_action(self):
        self.btnThoat.clicked.connect(self.close)

        self.btnThemHoSo.clicked.connect(self.btnThemHoSo_clicked)
        self.btnAdd_ThemHoSo.clicked.connect(self.btnAdd_ThemHoSo_clicked)
        self.maLop_ThemHoSo.returnPressed.connect(
            self.btnAdd_ThemHoSo.click)
        self.maSinhVien_ThemHoSo.returnPressed.connect(
            self.btnAdd_ThemHoSo.click)
        self.ngaySinh_ThemHoSo.returnPressed.connect(
            self.btnAdd_ThemHoSo.click)
        self.DTB_ThemHoSo.returnPressed.connect(
            self.btnAdd_ThemHoSo.click)
        self.btnDelete_ThemHoSo.clicked.connect(
            self.btnClear_ThemHoSo_clicked)

        self.btnInDanhSach.clicked.connect(self.btnInDanhSach_clicked)
        self.btnTimKiem_InDanhSach.clicked.connect(self.btnTimKiem_clicked)

        self.btnSapXep.clicked.connect(self.btnSapXep_clicked)
        self.btnThuatToan_SapXep.clicked.connect(
            self.btnThuatToan_SapXep_clicked)
        self.muiTenThuatToan_SapXep.clicked.connect(
            self.btnThuatToan_SapXep_clicked)
        self.chon_SapXep.clicked.connect(
            partial(self.ThuatToan_SapXep_clicked, 0))
        self.chen_SapXep.clicked.connect(
            partial(self.ThuatToan_SapXep_clicked, 1))
        self.noiBot_SapXep.clicked.connect(
            partial(self.ThuatToan_SapXep_clicked, 2))
        self.QuickSort_SapXep.clicked.connect(
            partial(self.ThuatToan_SapXep_clicked, 3))
        self.MergeSort_SapXep.clicked.connect(
            partial(self.ThuatToan_SapXep_clicked, 4))
        self.btnKhoa_SapXep.clicked.connect(self.btnKhoa_SapXep_clicked)
        self.muiTenKhoa_SapXep.clicked.connect(self.btnKhoa_SapXep_clicked)
        self.MaLop_SapXep.clicked.connect(partial(self.Khoa_SapXep_clicked, 0))
        self.MaSinhVien_SapXep.clicked.connect(
            partial(self.Khoa_SapXep_clicked, 1))
        self.HoVaTen_SapXep.clicked.connect(
            partial(self.Khoa_SapXep_clicked, 2))
        self.NgaySinh_SapXep.clicked.connect(
            partial(self.Khoa_SapXep_clicked, 3))
        self.DTB_SapXep.clicked.connect(
            partial(self.Khoa_SapXep_clicked, 4))
        self.btnSapXep_SapXep.clicked.connect(self.btnSapXep_SapXep_clicked)
        self.quayLai_SapXep.clicked.connect(self.btnSapXep_clicked)

        self.btnTimKiem.clicked.connect(self.btnTimKiem_clicked)
        self.btnThuatToan_TimKiem.clicked.connect(
            self.btnThuatToan_TimKiem_clicked)
        self.MuiTenThuatToan_TimKiem.clicked.connect(
            self.btnThuatToan_TimKiem_clicked)
        self.btnKhoa_TimKiem.clicked.connect(self.btnKhoa_TimKiem_clicked)
        self.MuiTenKhoa_TimKiem.clicked.connect(self.btnKhoa_TimKiem_clicked)
        self.TuanTu_TimKiem.clicked.connect(
            partial(self.ThuatToan_TimKiem_clicked, 0))
        self.NhiPhan_TimKiem.clicked.connect(
            partial(self.ThuatToan_TimKiem_clicked, 1))
        self.btnSearch_TimKiem.clicked.connect(self.btnSearch_TimKiem_clicked)
        self.inputSearch_TimKiem.returnPressed.connect(
            self.btnSearch_TimKiem.click)
        self.MaLop_TimKiem.clicked.connect(
            partial(self.Khoa_TimKiem_clicked, 0))
        self.MaSinhVien_TimKiem.clicked.connect(
            partial(self.Khoa_TimKiem_clicked, 1))
        self.HoVaTen_TimKiem.clicked.connect(
            partial(self.Khoa_TimKiem_clicked, 2))
        self.NgaySinh_TimKiem.clicked.connect(
            partial(self.Khoa_TimKiem_clicked, 3))
        self.DTB_TimKiem.clicked.connect(
            partial(self.Khoa_TimKiem_clicked, 4))
        self.btnBack_TimKiem.clicked.connect(
            self.btnTimKiem_clicked)

        self.btnThongKe.clicked.connect(self.btnThongKe_clicked)
        self.btnThongKeTheoLop.clicked.connect(self.btnThongKeTheoLop_clicked)
        self.btnThongKeTheoKetQua.clicked.connect(
            self.btnThongKeTheoKetQua_clicked)
        self.QuayLai1_ThongKe.clicked.connect(self.btnThongKe_clicked)
        self.QuayLai2_ThongKe.clicked.connect(self.btnThongKe_clicked)
        self.btnTruoc_ThongKe.clicked.connect(self.btnTruoc_ThongKe_clicked)
        self.btnSau_ThongKe.clicked.connect(self.btnSau_ThongKe_clicked)

    def loadData(self):
        self.llist.deleteList()
        if os.path.exists(self.pathData) and os.path.getsize(self.pathData) > 0:
            self.listData = read_csv(self.pathData, header=None,
                                     encoding='utf8').values.tolist()
            for person in self.listData:
                for i in range(len(person)):
                    person[i] = xor(person[i])
                person[1] = int(person[1])
                person[4] = float(person[4])
                self.llist.push(person)
        else:
            print("File is empty")

    def loadDataTable(self):
        if self.stackedWidget.currentWidget() == self.InDanhSach:
            if self.llist.Length() < 15:
                self.tableWidget.setRowCount(15)
                for row in range(15):
                    for col in range(5):
                        item = QTableWidgetItem(str(""))
                        item.setTextAlignment(
                            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                        self.tableWidget.setItem(row, col, item)
            else:
                self.tableWidget.setRowCount(self.llist.Length())
            temp = self.llist.head
            row = 0
            while (temp):
                person = temp.data
                for col in range(5):
                    item = QTableWidgetItem(str(person[col]))
                    item.setTextAlignment(
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.tableWidget.setItem(row, col, item)
                row += 1
                temp = temp.next
        elif self.stackedWidget.currentWidget() == self.InDanhSach_SapXep:
            if self.llist.Length() < 15:
                self.table_SapXep.setRowCount(15)
                for row in range(15):
                    for col in range(5):
                        item = QTableWidgetItem(str(""))
                        item.setTextAlignment(
                            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                        self.table_SapXep.setItem(row, col, item)
            else:
                self.table_SapXep.setRowCount(self.llist.Length())
            temp = self.llist.head
            row = 0
            while (temp):
                person = temp.data
                for col in range(5):
                    item = QTableWidgetItem(str(person[col]))
                    item.setTextAlignment(
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.table_SapXep.setItem(row, col, item)
                row += 1
                temp = temp.next

    def llisttoList(self):
        self.listData = []
        temp = self.llist.head
        while (temp):
            person = temp.data
            self.listData.append(person)
            temp = temp.next

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def btnThemHoSo_clicked(self):
        # self.btnClear_ThemHoSo_clicked()
        self.stackedWidget.setCurrentWidget(self.ThemHoSo)

    def btnAdd_ThemHoSo_clicked(self):
        malop = self.maLop_ThemHoSo.text().strip()
        maSinhVien = self.maSinhVien_ThemHoSo.text().strip()
        hoTen = self.hoTen_ThemHoSo.text().strip()
        ngaySinh = self.ngaySinh_ThemHoSo.text().strip()
        DTB = self.DTB_ThemHoSo.text().strip()
        if malop == "" or maSinhVien == "" or hoTen == "" or ngaySinh == "" or DTB == "":
            print("Lỗi : Chưa nhập đủ thông tin")
            return
        sv = ["".join(malop), int(maSinhVien), " ".join(
            hoTen.split()), "".join(
            ngaySinh.split()), float(DTB)]
        dct = {'MaLop': xor(sv[0]),
               'MaSinhVien': xor(sv[1]),
               'HoTen': xor(sv[2]),
               'NgaySinh': xor(sv[3]),
               'DTB': xor(sv[4])}
        print(sv)
        with open(self.pathData, 'a', newline="", encoding='utf-8') as file:
            field = ['MaLop', 'MaSinhVien', 'HoTen', 'NgaySinh', 'DTB']
            data = csv.DictWriter(file, fieldnames=field)
            data.writerow(dct)
        self.llist.push(sv)
        self.listData.append(sv)
        self.btnClear_ThemHoSo_clicked()

    def btnClear_ThemHoSo_clicked(self):
        _translate = QtCore.QCoreApplication.translate
        self.maLop_ThemHoSo.setText(_translate("MainWindow", ""))
        self.maSinhVien_ThemHoSo.setText(_translate("MainWindow", ""))
        self.hoTen_ThemHoSo.setText(_translate("MainWindow", ""))
        self.ngaySinh_ThemHoSo.setText(_translate("MainWindow", ""))
        self.DTB_ThemHoSo.setText(_translate("MainWindow", ""))

    def btnInDanhSach_clicked(self):
        self.stackedWidget.setCurrentWidget(self.InDanhSach)
        self.loadDataTable()

    def btnSapXep_clicked(self):
        _translate = QtCore.QCoreApplication.translate
        self.ThuatToan_SapXep.hide()
        self.muiTenThuatToan_SapXep.setStyleSheet(
            "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")
        self.KhoaSapXep_SapXep.hide()
        self.muiTenThuatToan_SapXep.setStyleSheet(
            "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")
        self.stackedWidget.setCurrentWidget(self.SapXep)
        if self.keySort == -1:
            self.btnKhoa_SapXep.setText(
                _translate("MainWindow", "Khóa sắp xếp"))
        else:
            self.btnKhoa_SapXep.setText(_translate(
                "MainWindow", listKhoaSapXep[self.keySort]))
        self.warning_SapXep.hide()

    def btnThuatToan_SapXep_clicked(self):
        if self.ThuatToan_SapXep.isHidden():
            self.ThuatToan_SapXep.show()
            self.muiTenThuatToan_SapXep.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muitenLen.png);")
        else:
            self.ThuatToan_SapXep.hide()
            self.muiTenThuatToan_SapXep.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")

    def btnKhoa_SapXep_clicked(self):
        if self.KhoaSapXep_SapXep.isHidden():
            self.KhoaSapXep_SapXep.show()
            self.muiTenKhoa_SapXep.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muitenLen.png);")
        else:
            self.KhoaSapXep_SapXep.hide()
            self.muiTenKhoa_SapXep.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")

    def ThuatToan_SapXep_clicked(self, index):
        self.llist.isSorted = -1
        _translate = QtCore.QCoreApplication.translate
        self.btnThuatToan_SapXep.setText(
            _translate("MainWindow", listThuatToanSapXep[index]))
        self.thuatToan = index
        self.btnThuatToan_SapXep_clicked()

    def Khoa_SapXep_clicked(self, index):
        self.llist.isSorted = -1
        _translate = QtCore.QCoreApplication.translate
        self.btnKhoa_SapXep.setText(_translate(
            "MainWindow", listKhoaSapXep[index]))
        self.keySort = index
        self.btnKhoa_SapXep_clicked()

    def btnSapXep_SapXep_clicked(self):
        if self.thuatToan != -1 and self.keySort != -1:
            if self.thuatToan == 0:
                self.llist.selectionSort(self.keySort)
            elif self.thuatToan == 1:
                self.llist.insertionSort(self.keySort)
            elif self.thuatToan == 2:
                self.llist.bubbleSort(self.keySort)
            elif self.thuatToan == 3:
                self.llist.quickSort(self.listData, self.keySort)
            elif self.thuatToan == 4:
                self.llist.mergeSort(self.listData, self.keySort)
            self.stackedWidget.setCurrentWidget(self.InDanhSach_SapXep)
            self.loadDataTable()
            if self.thuatToan == 0 or self.thuatToan == 1 or self.thuatToan == 2:
                self.llisttoList()
        else:
            self.warning_SapXep.show()
            print("Chưa chọn thuật toán hoặc khóa")

    def btnTimKiem_clicked(self):
        self.warning1_TimKiem.hide()
        self.warning2_TimKiem.hide()
        _translate = QtCore.QCoreApplication.translate
        self.ThuatToan_TimKiem.hide()
        self.MuiTenThuatToan_TimKiem.setStyleSheet(
            "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")
        self.KhoaTK_TimKiem.hide()
        self.MuiTenKhoa_TimKiem.setStyleSheet(
            "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")
        self.stackedWidget.setCurrentWidget(self.TimKiem)
        if self.keySort != -1:
            self.btnKhoa_TimKiem.setText(_translate(
                "MainWindow", listKhoaSapXep[self.keySort]))
            self.createCheckInput_TimKiem(self.keySort)
        if self.keySearch == -1:
            self.btnThuatToan_TimKiem.setText(
                _translate("MainWindow", "Thuật toán tìm kiếm"))
        if self.llist.isSorted == -1:
            self.NhiPhan_TimKiem.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        else:
            self.NhiPhan_TimKiem.setCursor(
                QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stackedWidget.setCurrentWidget(self.TimKiem)

    def btnThuatToan_TimKiem_clicked(self):
        if self.ThuatToan_TimKiem.isHidden():
            self.ThuatToan_TimKiem.show()
            self.MuiTenThuatToan_TimKiem.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muitenLen.png);")
        else:
            self.ThuatToan_TimKiem.hide()
            self.MuiTenThuatToan_TimKiem.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")

    def ThuatToan_TimKiem_clicked(self, index):
        _translate = QtCore.QCoreApplication.translate
        if index == 0:
            self.keySearch = 0
            self.btnThuatToan_TimKiem.setText(
                _translate("MainWindow", listKhoaTimKiem[0]))
        elif index == 1:
            if self.llist.isSorted != -1:
                self.keySearch = 1
                self.btnThuatToan_TimKiem.setText(
                    _translate("MainWindow", listKhoaTimKiem[1]))
            else:
                self.keySearch = -1
        self.btnThuatToan_TimKiem_clicked()

    def btnKhoa_TimKiem_clicked(self):
        if self.KhoaTK_TimKiem.isHidden():
            self.KhoaTK_TimKiem.show()
            self.MuiTenKhoa_TimKiem.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muitenLen.png);")
        else:
            self.KhoaTK_TimKiem.hide()
            self.MuiTenKhoa_TimKiem.setStyleSheet(
                "border-image: url(:/MuiTen/SapXep/muiTenXuong.png);")

    def Khoa_TimKiem_clicked(self, index):
        self.llist.isSorted = -1
        self.NhiPhan_TimKiem.setCursor(
            QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        _translate = QtCore.QCoreApplication.translate
        self.btnKhoa_TimKiem.setText(_translate(
            "MainWindow", listKhoaSapXep[index]))
        self.keySort = index
        self.createCheckInput_TimKiem(self.keySort)
        self.btnKhoa_TimKiem_clicked()

    def btnSearch_TimKiem_clicked(self):
        ans = []
        input = self.inputSearch_TimKiem.text().strip()
        if input == "":
            print("Chưa nhập gì")
            return
        if self.keySort == 1:
            input = int(input)
        elif self.keySort == 4:
            input = float(input)
        if self.keySearch == -1 or self.keySort == -1:
            self.warning1_TimKiem.show()
            self.warning2_TimKiem.hide()
            print("Chưa chọn thuật toán hoặc khóa")
            return
        if self.keySearch == 0:
            ans = self.llist.linearSearch(input, self.keySort)

        elif self.keySearch == 1:
            if self.llist.isSorted == -1:
                self.warning1_TimKiem.hide()
                self.warning2_TimKiem.show()
                print("Chưa sắp xếp")

                return
            else:
                ans = self.llist.getBinarySearch(
                    self.listData, input, self.keySort)
        self.stackedWidget.setCurrentWidget(self.result_TimKiem)
        if ans == None:
            ans = []
        if len(ans) < 15:
            self.searchTable_TimKiem.setRowCount(15)
            for row in range(15):
                for col in range(5):
                    item = QTableWidgetItem(str(""))
                    item.setTextAlignment(
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.searchTable_TimKiem.setItem(row, col, item)
        else:
            self.searchTable_TimKiem.setRowCount(len(ans))
        for row in range(len(ans)):
            for col in range(5):
                item = QTableWidgetItem(str(ans[row][col]))
                item.setTextAlignment(
                    QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.searchTable_TimKiem.setItem(row, col, item)

    def createCheckInput_TimKiem(self, index):
        self.inputSearch_TimKiem.setText(
            QtCore.QCoreApplication.translate("MainWindow", ""))
        self.inputSearch_TimKiem.setInputMask("")
        self.inputSearch_TimKiem.setValidator(None)
        if index == 0:
            self.inputSearch_TimKiem.setPlaceholderText("Mã lớp")
        elif index == 1:
            self.inputSearch_TimKiem.setPlaceholderText("Mã sinh viên")
            self.inputSearch_TimKiem.setValidator(QtGui.QIntValidator())
        elif index == 2:
            self.inputSearch_TimKiem.setPlaceholderText("Họ và tên")
        elif index == 3:
            self.inputSearch_TimKiem.setPlaceholderText("Ngày sinh")
            self.inputSearch_TimKiem.setInputMask('00/00/0000')
        elif index == 4:
            self.inputSearch_TimKiem.setPlaceholderText(
                "ĐTB tích lũy")
            self.inputSearch_TimKiem.setValidator(QtGui.QDoubleValidator())
        else:
            self.inputSearch_TimKiem.setPlaceholderText("")

    def btnThongKe_clicked(self):
        try:
            self.timer.timeout.disconnect()
            self.timer.stop()
        except:
            pass
        self.stackedWidget.setCurrentWidget(self.ThongKe)
        dictQuanSo = self.llist.statisticAccordingToGrade()

        self.listClass = [
            lop for lop in dictQuanSo]
        self.handleTable1_ThongKe(dictQuanSo)
        # lstColor = [random.choice(listColor)
        #             for i in range(len(self.listClass))]
        self.indexAnimationChart = 0
        self.handleChart1(dictQuanSo, True)
        self.timer.timeout.connect(
            partial(self.handleChart1, dictQuanSo))

    def handleTable1_ThongKe(self, dictQuanSo):
        if len(self.listClass) < 12:
            self.table1_ThongKe.setRowCount(12)
            for row in range(12):
                for col in range(2):
                    item = QTableWidgetItem(str(""))
                    item.setTextAlignment(
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.table1_ThongKe.setItem(row, col, item)
        else:
            self.table1_ThongKe.setRowCount(len(self.listClass))
        for row in range(len(self.listClass)):
            item = QTableWidgetItem(str(self.listClass[row]))
            item.setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table1_ThongKe.setItem(row, 0, item)
            item = QTableWidgetItem(str(dictQuanSo[self.listClass[row]]))
            item.setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table1_ThongKe.setItem(row, 1, item)

    def handleChart1(self, dictQuanSo, animation=False):
        series = QPieSeries()
        series.setHoleSize(0.40)
        font = QtGui.QFont("Times", 10)
        lengthChart = len(self.listClass)
        for i in range(lengthChart):
            my_slice = series.append(
                self.listClass[i], dictQuanSo[self.listClass[i]])
            # my_slice.setExploded(True)
            my_slice.setBrush(QtGui.QColor(listColor[i % len(listColor)]))
            my_slice.setLabelVisible(True)
            my_slice.setLabelFont(font)
            my_slice.setLabelColor(QtGui.QColor("#FFFFFF"))
            series.append(my_slice)

        series.slices()[self.indexAnimationChart %
                        len(self.listClass)].setExploded(True)

        chart = QChart()
        chart.addSeries(series)
        # chart.setAnimationOptions(None)
        if animation:
            chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setTheme(QChart.ChartThemeDark)
        chart.legend().setVisible(False)
        chart.setBackgroundBrush(
            QtGui.QBrush(QtGui.QColor("transparent")))

        chartview = QChartView(chart)
        self.clearLayout(self.layout_chart_1)
        # self.layout_chart_1.setParent(None)
        self.layout_chart_1.addWidget(chartview)
        self.indexAnimationChart += 1

    def btnThongKeTheoLop_clicked(self):
        self.stackedWidget.setCurrentWidget(self.ThongKeTheoLop)
        self.timer.start()

    def btnThongKeTheoKetQua_clicked(self):
        self.handleKetQua()
        self.stackedWidget.setCurrentWidget(self.ThongKeTheoKetQua)

    def handleKetQuaFrame_ThongKe(self, dicKetQua):
        _translate = QtCore.QCoreApplication.translate
        if self.indexChartClass == 0:
            self.lbClass_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ffffff;\">Tổng quan</span></p></body></html>"))
            self.XuatSac_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Xuất sắc : {dicKetQua['Tong']['XuatSac']} sinh viên</span></p></body></html>"))
            self.Gioi_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Giỏi : {dicKetQua['Tong']['Gioi']} sinh viên</span></p></body></html>"))
            self.Kha_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Khá : {dicKetQua['Tong']['Kha']} sinh viên</span></p></body></html>"))
            self.TrungBinh_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Trung bình : {dicKetQua['Tong']['TrungBinh']} sinh viên</span></p></body></html>"))
            self.Yeu_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Yếu : {dicKetQua['Tong']['Yeu']} sinh viên</span></p></body></html>"))
            self.Kem_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Kém : {dicKetQua['Tong']['Kem']} sinh viên</span></p></body></html>"))
        else:
            self.lbClass_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ffffff;\">Mã Lớp : {self.listClass[self.indexChartClass-1]}</span></p></body></html>"))
            self.XuatSac_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Xuất sắc : {dicKetQua[self.listClass[self.indexChartClass-1]]['XuatSac']} sinh viên</span></p></body></html>"))
            self.Gioi_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Giỏi : {dicKetQua[self.listClass[self.indexChartClass-1]]['Gioi']} sinh viên</span></p></body></html>"))
            self.Kha_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Khá : {dicKetQua[self.listClass[self.indexChartClass-1]]['Kha']} sinh viên</span></p></body></html>"))
            self.TrungBinh_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Trung bình : {dicKetQua[self.listClass[self.indexChartClass-1]]['TrungBinh']} sinh viên</span></p></body></html>"))
            self.Yeu_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Yếu : {dicKetQua[self.listClass[self.indexChartClass-1]]['Yeu']} sinh viên</span></p></body></html>"))
            self.Kem_ThongKe.setText(_translate(
                "MainWindow", f"<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">Kém : {dicKetQua[self.listClass[self.indexChartClass-1]]['Kem']} sinh viên</span></p></body></html>"))

    def handleChart2(self, dicKetQua):
        series = QPieSeries()
        series.setHoleSize(0.40)
        font = QtGui.QFont("Times", 10)
        indexColor = 0
        color = random.sample(listColor, len(lstXepLoai))
        for xepHang in lstXepLoai:
            if self.indexChartClass != 0:
                ketQuaXepHang = dicKetQua[self.listClass[self.indexChartClass-1]][xepHang]
            else:
                ketQuaXepHang = dicKetQua['Tong'][xepHang]
            my_slice = series.append(
                lstXepLoai[xepHang], ketQuaXepHang)
            # my_slice.setExploded(True)
            # my_slice.setBrush(QtGui.QColor(random.choice(listColor)))
            my_slice.setBrush(QtGui.QColor(color[indexColor]))
            indexColor += 1
            if ketQuaXepHang != 0:
                my_slice.setLabelVisible(True)
            else:
                my_slice.setLabelVisible(False)
            my_slice.setLabelFont(font)
            my_slice.setLabelColor(QtGui.QColor("#FF0000"))
            series.append(my_slice)
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setTheme(QChart.ChartThemeLight)
        chart.setBackgroundBrush(
            QtGui.QBrush(QtGui.QColor("transparent")))
        chart.legend().setVisible(False)
        chartview = QChartView(chart)
        self.clearLayout(self.layout_chart2)
        self.layout_chart2.addWidget(chartview)

    def handleKetQua(self):
        dicKetQua = self.llist.getStatisticsAccordingToLearningResults()
        self.handleKetQuaFrame_ThongKe(dicKetQua)
        self.handleChart2(dicKetQua)

    def btnTruoc_ThongKe_clicked(self):
        if self.indexChartClass == 0:
            self.indexChartClass = len(self.listClass)
        else:
            self.indexChartClass -= 1
        self.handleKetQua()

    def btnSau_ThongKe_clicked(self):
        self.indexChartClass += 1
        self.indexChartClass = self.indexChartClass % (len(self.listClass) + 1)
        self.handleKetQua()


if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    window = QuanLySinhVien()
    window.show()
    sys.exit(app.exec_())
