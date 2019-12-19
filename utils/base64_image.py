import base64

def transfer2_base64_str(imgPath):
    img = open(imgPath,'rb')
    return str(base64.b64encode(img.read()),'utf-8')
