# import win32com.client
#
# speaker = win32com.client.Dispatch("SAPI.SpVoice")
# str1 = """
# 日照香炉生紫烟，
# 遥看瀑布挂前川。
# 飞流直下三千尺，
# 疑是银河落九天。
# """
# speaker.Speak(str1)
# for i in range(1, 6):
#     speaker.Speak("呵呵第" + str(i) + "次")

# import win32com.client
# import winsound
# speak = win32com.client.Dispatch('SAPI.SPVOICE')
# winsound.Beep(2015, 500) #第二个参数是500毫秒

# import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice, voice.id)
#     engine.setProperty('voice', voice.id)
#     engine.say("Hello World!")
#     engine.runAndWait()
#     engine.stop()
a ='11'
b =['111']
print(a in b)