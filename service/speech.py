""" 语音播报模块 """
import pyttsx3

def speak(word):
    # 模块初始化
    engine = pyttsx3.init()

    # print('准备开始语音播报...')

    # 设置要播报的Unicode字符串
    engine.say(word)
    engine.runAndWait()

if __name__ == '__main__':
    word = "欢迎李帅伟同学"
    speak(word)


