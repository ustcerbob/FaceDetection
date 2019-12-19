"""人脸服务模块"""
from service import camera, db_manage, speech
from api import face_baidu_api

"""人脸注册到人脸库"""


def face_register_to_db(userId, user_info):

    img_path = camera.default_folder_path + camera.default_img_name
    # 检测获取图片是否为人脸
    code, msg = face_baidu_api.face_detect(img_path)
    print(code, msg)
    if code == 1:
        speech.speak(msg + "，请对准摄像头，重新录入")
        return code
    if code == 2:
        print('人脸检测出现接口错误或异常')
        speech.speak("人脸录入失败，请对准摄像头，重新录入")
        return code
    # 如果人脸合格，录入
    print("人脸合格，开始保存到人脸库")
    speech.speak("人脸合格，开始保存到人脸库")
    if db_manage.user_add(img_path, userId, user_info) == 0:
        print("保存到人脸库成功")
        speech.speak("人脸录入成功")
        return 0
    print("保存到人脸库失败")
    speech.speak("人脸录入失败，请对准摄像头，重新录入")

    return 1


"""人脸库搜索并致欢迎语"""


def face_search_welcome():
    img_path = camera.default_folder_path + camera.default_img_name
    # 检测获取图片是否为人脸
    code, msg = face_baidu_api.face_detect(img_path)
    if code == 1:
        print(msg)
        speech.speak(msg + "，请对准摄像头，重新录入")
        return code, msg
    if code == 2:
        print('照片不合格')
        speech.speak(msg + "，请对准摄像头，重新录入")
        return code, msg
    # 如果人脸合格，录入
    print("人脸合格，开始比对人脸")
    speech.speak("人脸合格，开始比对人脸库")
    code, info = face_baidu_api.face_search_1n(img_path)

    if code == 0:
        print("与%s匹配成功" % (info))
        speech.speak("欢迎" + info + "同学")
        return 0, info

    print("没有匹配到人脸")
    speech.speak("没有匹配到人脸，请先注册人脸")

    # speech.speak("连续10次失败，请等候片刻再继续")
    return 1, '没有匹配到人脸，请先注册人脸'


def delete_face(userId):
    # 调用百度api删除用户
    code, msg = db_manage.delete_user(userId)
    return code, msg
