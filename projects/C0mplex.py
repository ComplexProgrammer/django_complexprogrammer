import sqlite3


db = sqlite3.connect(r"C:\Users\User\PycharmProjects\pythonProject_complexprogrammer_web\website\avtotest.db")
db2 = sqlite3.connect(r"E:\VSCODE\django_complexprogrammer\db.sqlite3")
res = db.execute("select id, savol, savol_en, savol_ru, javob_a, javob_a_en, javob_a_ru, javob_b, javob_b_en, javob_b_ru, javob_c, javob_c_en, javob_c_ru, javob_d, javob_d_en, javob_d_ru, javob, bilet, raqam, rasm from savollar")
for row in res:
    id=row[0]
    savol=row[1]
    savol_en=row[2]
    savol_ru=row[3]
    javob_a=row[4]
    javob_a_en=row[5]
    javob_a_ru=row[6]
    javob_b=row[7]
    javob_b_en=row[8]
    javob_b_ru=row[9]
    javob_c=row[10]
    javob_c_en=row[11]
    javob_c_ru=row[12]
    javob_d=row[13]
    javob_d_en=row[14]
    javob_d_ru=row[15]
    javob=row[12]
    bilet=row[13]
    raqam=row[14]
    rasm=row[15]
    params = (savol, savol_en, savol_ru, javob_a_ru, row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
    # print(params)
    # db2.execute("insert into projects_avtotest (savol, savol_en, savol_ru, javob_a, javob_a_en, javob_a_ru, javob_b, javob_b_en, javob_b_ru, javob_c, javob_c_en, javob_c_ru, javob_d, javob_d_en, javob_d_ru, javob, bilet, raqam, rasm) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)