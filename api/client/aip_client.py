from aip import AipFace


class FaceClient:
    static_client = None
    """ 你的 APPID AK SK """
    APP_ID = '17826594'
    API_KEY = 'qacZvHYOQ6tnvGgxjXRP71zH'
    SECRET_KEY = 'XGU9vyvveaFS2MiqpbgR9f3crFMfGkAu'

    @classmethod
    def get_face_client(cls):
        if FaceClient.static_client:
            return FaceClient.static_client
        print("first initialize client")
        FaceClient.static_client = AipFace(FaceClient.APP_ID, FaceClient.API_KEY, FaceClient.SECRET_KEY)
        return FaceClient.static_client
