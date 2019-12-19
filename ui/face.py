"""face.ui转换成的py文件"""
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from service import face_service
import service.camera as camera


class Ui_self(QWidget):
    def __init__(self, parent=None):
        super(Ui_self, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 定时器
        self.setupUi()
        self.retranslateUi()
        self.cap = cv2.VideoCapture()  # 准备获取图像
        self.CAM_NUM = 0

        self.slot_init()  # 设置槽函数
        self.open_camera()  # 打开窗口即打开摄像头

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(509, 389)


        self.id_label = QtWidgets.QLabel(self)
        self.id_label.setGeometry(QtCore.QRect(30, 20, 41, 9))
        self.id_label.setObjectName("id_label")
        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setGeometry(QtCore.QRect(30, 60, 41, 9))
        self.name_label.setObjectName("name_label")

        self.id_edit = QtWidgets.QLineEdit(self)
        self.id_edit.setGeometry(QtCore.QRect(60, 10, 113, 20))
        self.id_edit.setObjectName("id_edit")
        self.name_edit = QtWidgets.QLineEdit(self)
        self.name_edit.setGeometry(QtCore.QRect(60, 50, 113, 20))
        self.name_edit.setObjectName("name_edit")
        self.register_face_button = QtWidgets.QPushButton(self)
        self.register_face_button.setGeometry(QtCore.QRect(30, 90, 56, 17))
        self.register_face_button.setObjectName("register_face_button")
        self.face_recognition_button = QtWidgets.QPushButton(self)
        self.face_recognition_button.setGeometry(QtCore.QRect(90, 90, 56, 17))
        self.face_recognition_button.setObjectName("face_recognition_button")
        self.delete_face_button = QtWidgets.QPushButton(self)
        self.delete_face_button.setGeometry(QtCore.QRect(30, 120, 56, 17))
        self.delete_face_button.setObjectName("delete_face_button")

        self.msg_label = QtWidgets.QLabel(self)
        self.msg_label.setGeometry(QtCore.QRect(30, 150, 41, 9))
        self.msg_label.setObjectName("msg_label")

        self.static_face_label = QtWidgets.QLabel(self)
        self.static_face_label.setGeometry(QtCore.QRect(30, 170, 145, 178))
        self.static_face_label.setObjectName("static_face_label")
        self.dynamic_face_label = QtWidgets.QLabel(self)
        self.dynamic_face_label.setGeometry(QtCore.QRect(220, 30, 231, 321))
        self.dynamic_face_label.setObjectName("dynamic_face_label")
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "人脸识别欢迎系统"))
        self.register_face_button.setText(_translate("self", "注册人脸"))
        self.static_face_label.setText(_translate("self", "显示图片"))
        self.dynamic_face_label.setText(_translate("self", "显示摄像头动态图像"))
        self.id_label.setText(_translate("self", "学号"))
        self.name_label.setText(_translate("self", "姓名"))
        self.msg_label.setText(_translate("self", ""))
        self.face_recognition_button.setText(_translate("self", "人脸识别"))
        self.delete_face_button.setText(_translate("self", "删除人脸"))

    def slot_init(self):
        # 设置槽函数
        self.timer_camera.timeout.connect(self.show_camera)
        self.register_face_button.clicked.connect(self.register_face)
        self.face_recognition_button.clicked.connect(self.face_detect)
        self.delete_face_button.clicked.connect(self.delete_face)

    def open_camera(self):
        if self.timer_camera.isActive() == False:
            # flag = self.cap.open(self.CAM_NUM)
            flag = self.cap.open(self.CAM_NUM)
            print("摄像头开启")
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                    self, u"Warning", u"请检测相机与电脑是否连接正确",
                    buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                print("定时器开启")
                self.timer_camera.start(30)

    # 定时器执行显示动态图片
    def show_camera(self):
        flag, self.image = self.cap.read()
        # print("读取图片")
        self.image = cv2.flip(self.image, 1)  # 左右翻转
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.dynamic_face_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.dynamic_face_label.setScaledContents(True)

    def save_and_show_static_img(self):
        # 保存图片
        cv2.imwrite(camera.default_img_name, self.image)

        # cv2.putText(self.image, 'The picture have saved !',
        #             (int(self.image.shape[1]/2-130), int(self.image.shape[0]/2)),
        #             cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
        #             1.0, (255, 0, 0), 1)
        #
        # #self.timer_camera.stop()
        #
        # show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 左右翻转
        #
        # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)

        # self.label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #
        # self.label_face.setScaledContents(True)

        # 左侧框显示人脸图片

        jpg = QtGui.QPixmap(camera.default_img_name).scaled(self.static_face_label.width(), self.static_face_label.height())
        self.static_face_label.setPixmap(jpg)

    # 注册人脸
    def register_face(self):
        self.save_and_show_static_img()
        # 用此图片进行人脸注册
        userId = self.id_edit.text()
        user_info = self.name_edit.text()

        if not userId or not user_info:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "请填写完整的个人信息",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            return
        code = face_service.face_register_to_db(userId, user_info)
        if code == 0:
            msg = '人脸注册成功！请点击人脸识别！'
        else:
            msg = '人脸注册失败，请对准摄像头重试！'
        self.msg_label.setText(msg)
        self.msg_label.setStyleSheet("color:red")
        self.msg_label.adjustSize()

    def face_detect(self):
        self.save_and_show_static_img()

        jpg = QtGui.QPixmap(camera.default_img_name).scaled(self.static_face_label.width(), self.static_face_label.height())
        self.static_face_label.setPixmap(jpg)
        code, info = face_service.face_search_welcome()
        if code == 0:
            msg = "欢迎" + info + "同学！"
        else:
            msg = info
        self.msg_label.setText(msg)
        self.msg_label.setStyleSheet("color:red")
        self.msg_label.adjustSize()

    # 删除人脸
    def delete_face(self):
        userId = self.id_edit.text()

        if not userId:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "请填写要删除的学号",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            return
        code,msg = face_service.delete_face(userId)
        self.msg_label.setText(msg)
        self.msg_label.setStyleSheet("color:red")
        self.msg_label.adjustSize()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    ui = Ui_self()

    ui.show()
    exit(app.exec_())
