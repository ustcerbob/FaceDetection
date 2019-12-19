"""百度api封装模块"""
from api.client.aip_client import FaceClient
from utils.base64_image import transfer2_base64_str
from utils.ascii_to_utf8 import ascii_to_utf8


def face_search_1n(img_path):
    try:
        image = transfer2_base64_str(img_path)

        imageType = "BASE64"

        groupIdList = "soft19"

        """ 调用人脸搜索 """

        """ 如果有可选参数 """
        options = {}
        options["max_face_num"] = 1
        options["match_threshold"] = 70
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "NONE"
        # options["user_id"] = "233451"
        options["max_user_num"] = 3

        """ 带参数调用人脸搜索 """
        response = FaceClient.get_face_client().search(image, imageType, groupIdList, options)
        print(response)
        # response = json.loads(response)
        if response['error_code'] == 222207:
            return 1, '没有匹配到人脸，请先注册人脸'
        if response['error_code'] != 0:
            return 1, 'not found'
        user_info = response['result']['user_list'][0]['user_info']
        if user_info[:2] == 'b\'':
            user_info = ascii_to_utf8(user_info)[2:-1]
        return 0, user_info
    except Exception as e:
        print("调用百度人脸搜索接口出现异常", e)
        return 1, 'exception occurred'


"""
0代表成功
1代表没有检测到人脸
2代表人脸不合格
"""


def face_detect(img_path):
    try:
        image = transfer2_base64_str(img_path)

        imageType = "BASE64"

        """ 调用人脸检测 """

        """ 如果有可选参数 """
        options = {}
        options["face_field"] = "quality"
        options["face_type"] = "LIVE"
        options["liveness_control"] = "LOW"

        """ 带参数调用人脸搜索 """
        response = FaceClient.get_face_client().detect(image, imageType, options)
        print(response)
        if response['error_code'] == 222202:
            return 1, '照片中没有检测到人脸'
        if response['error_code'] != 0:
            return 1, '百度接口返回错误'
        # response = json.loads(response)
        result = response['result']
        if result['face_num'] <= 0:
            return 1, '照片中没有检测到人脸'
        angle = result['face_list'][0]['angle']
        # print(angle)
        if angle['yaw'] > 20 or angle['pitch'] > 20 or angle['roll'] > 20:
            return 2, '身体倾斜'
        quality = result['face_list'][0]['quality']
        # print(quality)
        if quality['occlusion']['left_eye'] > 0.6 or quality['occlusion']['mouth'] > 0.7 or quality['occlusion'][
            'right_eye'] > 0.6 or quality['occlusion']['nose'] > 0.7 or quality['occlusion']['left_cheek'] > 0.8 or \
                quality['occlusion']['right_cheek'] > 0.8 or quality['occlusion']['chin_contour'] > 0.6:
            print("脸部有遮挡")
            return 2, '脸部有遮挡'
        if quality['blur'] > 0.8:
            print("照片模糊")
            return 2, '照片模糊'
        if quality['illumination'] < 30:
            print("光线不好")
            return 2, '光线不好'
        return 0, '人脸合格'
    except Exception as e:
        print("人脸检测发生异常", e)
        return 1, '人脸检测发生异常'
