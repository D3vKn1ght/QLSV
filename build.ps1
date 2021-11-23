pyrcc5.exe -o InDanhSach_rc.py .\image\InDanhSach.qrc
pyrcc5.exe -o ThemHoSo_rc.py .\image\ThemHoSo.qrc
pyrcc5.exe -o home_rc.py .\image\home.qrc
pyrcc5.exe -o SapXep_rc.py .\image\SapXep.qrc
pyrcc5.exe -o TimKiem_rc.py .\image\TimKiem.qrc
# pyrcc5.exe -o login_rc.py .\image\login.qrc
pyrcc5.exe -o ThongKe_rc.py .\image\ThongKe.qrc
pyuic5 -x .\gui.ui -o gui.py
