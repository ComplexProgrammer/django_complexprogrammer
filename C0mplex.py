# import sqlite3


# db = sqlite3.connect(r"C:\Users\User\PycharmProjects\pythonProject_complexprogrammer_web\website\avtotest.db")
# # db2 = sqlite3.connect(r"E:\VSCODE\django_complexprogrammer\db.sqlite3")
# # db = sqlite3.connect(r"C:\Users\odilj\PycharmProjects\pythonProject_complexprogrammer_web\website\avtotest.db")
# db2 = sqlite3.connect(r"db.sqlite3")
# res = db.execute("select id, savol, savol_en, savol_ru, javob_a, javob_a_en, javob_a_ru, javob_b, javob_b_en, javob_b_ru, javob_c, javob_c_en, javob_c_ru, javob_d, javob_d_en, javob_d_ru, javob, bilet, raqam, rasm from savollar")
# for row in res:
#     id=row[0]
#     savol=row[1]
#     savol_en=row[2]
#     savol_ru=row[3]
#     javob_a=row[4]
#     javob_a_en=row[5]
#     javob_a_ru=row[6]
#     javob_b=row[7]
#     javob_b_en=row[8]
#     javob_b_ru=row[9]
#     javob_c=row[10]
#     javob_c_en=row[11]
#     javob_c_ru=row[12]
#     javob_d=row[13]
#     javob_d_en=row[14]
#     javob_d_ru=row[15]
#     javob=row[16]
#     bilet=row[17]
#     raqam=row[18]
#     rasm=row[19]
#     if javob_a_en is None:
#         javob_a_en = ''
#     if javob_a_ru is None:
#         javob_a_ru = ''
#     if javob_b_en is None:
#         javob_b_en = ''
#     if javob_b_ru is None:
#         javob_b_ru = ''
#     if javob_c_en is None:
#         javob_c_en = ''
#     if javob_c_ru is None:
#         javob_c_ru = ''
#     if javob_d_en is None:
#         javob_d_en = ''
#     if javob_d_ru is None:
#         javob_d_ru = ''
#     params = (savol, savol_en, savol_ru, javob_a, javob_a_en, javob_a_ru, javob_b, javob_b_en, javob_b_ru, javob_c, javob_c_en, javob_c_ru, javob_d, javob_d_en, javob_d_ru, javob, bilet, raqam, rasm)
#     print(id)
#     db2.execute("insert into projects_avtotest (savol, savol_en, savol_ru, javob_a, javob_a_en, javob_a_ru, javob_b, javob_b_en, javob_b_ru, javob_c, javob_c_en, javob_c_ru, javob_d, javob_d_en, javob_d_ru, javob, bilet, raqam, rasm) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)



# import pyttsx3

# def say(sp):
#     engine = pyttsx3.init()
#     engine.say(sp)
#     engine.runAndWait()
    
# say("Hello my name is Neuron")
# from projects import youtube_downloader
# quality='low'
# link='https://www.youtube.com/shorts/yNIFcuD4niQ'
# youtube_downloader.download_video(link, quality)


from pytube import YouTube
YouTube('https://youtu.be/9bZkp7q19f0').streams.first()