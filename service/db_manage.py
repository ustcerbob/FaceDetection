"""人脸库管理模块"""
from api.client.aip_client import FaceClient
from utils.base64_image import transfer2_base64_str
from time import time

"""
0成功 1失败
"""


def user_add(img_path, userId, user_info):
    try:
        image = transfer2_base64_str(img_path)

        imageType = "BASE64"

        groupId = "soft19"

        """ 如果有可选参数 """
        options = {}
        options["user_info"] = str(user_info.encode("utf8"))
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"

        """ 带参数调用人脸注册 """
        response = FaceClient.get_face_client().addUser(image, imageType, groupId, userId, options)
        print(response)
        if response['error_code'] == 0:
            return 0
        return 1
    except Exception as e:
        print('调用百度用户注册接口出现异常',e)
        return 1


def delete_user(userId):
    try:

        groupId = "soft19"

        """ 带参数调用人脸搜索 """
        response = FaceClient.get_face_client().deleteUser(groupId, userId)
        print(response)
        if response['error_code'] == 223103:
            return 1, '没有此用户'
        if response['error_code'] != 0:
            return 1, '百度接口返回错误'

        return 0, '删除成功'
    except Exception as e:
        print("删除用户发生异常", e)
        return 1, '删除用户发生异常'

if __name__ == '__main__':
    # user_add("D:\北航\资料\人脸识别实践\Demo\测试头像\\1421221304095989.jpg")
    print(str(time()).replace('.', ''))
