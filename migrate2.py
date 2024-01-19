import datetime
import sqlite3
from googletrans import Translator
conn = sqlite3.connect('db.sqlite3')
c1 = conn.cursor()
c2 = conn.cursor()
c3 = conn.cursor()
c4 = conn.cursor()
c5 = conn.cursor()
i = 0
n=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
translator = Translator()
characters = [["A", "А"], ["B", "Б"], ["D", "Д"], ["E", "Е"], ["F", "Ф"], ["G", "Г"], ["H", "Ҳ"], ["I", "И"],
            ["J", "Ж"], ["K", "К"], ["L", "Л"], ["M", "М"], ["N", "Н"], ["O", "О"], ["P", "П"], ["Q", "Қ"],
            ["R", "Р"], ["S", "С"], ["T", "Т"], ["U", "У"], ["V", "В"], ["X", "Х"], ["Y", "Й"], ["Z", "З"],
            ["a", "а"], ["b", "б"], ["d", "д"], ["e", "е"], ["f", "ф"], ["g", "г"], ["h", "ҳ"], ["i", "и"],
            ["j", "ж"], ["k", "к"], ["l", "л"], ["m", "м"], ["n", "н"], ["o", "о"], ["p", "п"], ["q", "қ"],
            ["r", "р"], ["s", "с"], ["t", "т"], ["u", "у"], ["v", "в"], ["x", "х"], ["y", "й"], ["z", "з"],
            ["А", "A"], ["Б", "B"], ["С", "C"], ["Ч", "Ch"], ["Д", "D"], ["Е", "E"], ["Ф", "F"], ["Г", "G"],
            ["Ҳ", "H"], ["И", "I"], ["Ж", "J"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "N"], ["О", "O"],
            ["П", "P"], ["Қ", "Q"], ["Р", "R"], ["С", "S"], ["Ш", "Sh"], ["Т", "T"], ["У", "U"], ["В", "V"],
            ["Х", "X"], ["Й", "Y"], ["Я", "Ya"], ["Ю", "Yu"], ["Ё", "Yo"], ["З", "Z"], ["Ғ", "Gʼ"], ["а", "a"],
            ["б", "b"], ["с", "c"], ["ч", "ch"], ["д", "d"], ["е", "e"], ["ф", "f"], ["г", "g"], ["ҳ", "h"],
            ["и", "i"], ["ж", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "n"], ["о", "o"], ["п", "p"],
            ["қ", "q"], ["р", "r"], ["с", "s"], ["ш", "sh"], ["т", "t"], ["у", "u"], ["в", "v"], ["х", "x"],
            ["й", "y"], ["я", "ya"], ["ю", "yu"], ["ё", "yo"], ["з", "z"], ["ғ", "gʼ"], ["ъ", "`"], ["`", "ъ"],
            ["'", "ъ"], ["’", "ъ"], ["‘", "ъ"]]
def to_crl(text):
    arr = list(text)
    for ar in arr:
        for obj in characters:
            if obj[0] == ar:
                text = text.replace(ar, obj[1])
    text = text.replace("Оъ", "Ў").replace("оъ", "ў")
    text = text.replace("йа", "я").replace("Йа", "Я").replace("ЙА", "Я").replace("йА", "я")
    text = text.replace("йо", "ё").replace("Йо", "Ё").replace("ЙО", "Ё").replace("йО", "ё")
    text = text.replace("йу", "ю").replace("Йу", "Ю").replace("ЙУ", "Ю").replace("йУ", "ю")
    text = text.replace("сҳ", "ш").replace("Сҳ", "Ш").replace("СҲ", "Ш").replace("сҲ", "ш")
    text = text.replace("cҳ", "ч").replace("Cҳ", "Ч").replace("CҲ", "Ч").replace("cҲ", "ч")
    text = text.replace("Гъ", "Ғ").replace("гъ", "ғ")
    return text


results1 = conn.execute("SELECT * from projects_avtotest where id>1")   
results2 = conn.execute("SELECT * from tests_questions where book_id=49")   
for row1 in results1:
    for row2 in results2:
        if row1[17]+374==row2[9]:
            print(row1[17], row2[9], row1[1], row2[7], "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            i=i+1
            text=to_crl(str(row1[1]).replace('"', '`').replace("'", "`"))
            right_a=0
            right_b=0
            right_c=0
            right_d=0
            if(row1[16]=='A'):
                right_a=1
            if(row1[16]=='B'):
                right_b=1
            if(row1[16]=='C'):
                right_c=1
            if(row1[16]=='D'):
                right_d=1
            image=''
            if row1[19]!='':
                image='tests/questions/images/'+row1[19]
            sql1 = "update tests_questions set name_uz_crl='"+text+"', image='"+image+"' where id="+str(row2[0])
            print(sql1)
            c1.execute(sql1)
            conn.commit()
            if row1[4]!='':
                text=to_crl(str(row1[4]).replace('"', '`').replace("'", "`"))
                sql2 = 'insert into tests_answers (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, right, question_id, sort_order, image, book_id, group_id, topic_id, type_id) VALUES ("'+n+'", "'+n+'", 0, "'+str(row1[5]).replace('"', '`').replace("'", "`")+'", "'+str(row1[6]).replace('"', '`').replace("'", "`")+'", "'+str(text)+'", "'+str(row1[4]).replace('"', '`').replace("'", "`")+'", "1", '+str(right_a)+', '+str(row2[0])+', 0, "", 49, 24, '+str(row2[9])+', 3)'
                print(sql2)
                c2.execute(sql2)
                conn.commit()
            if row1[7]!='':
                text=to_crl(str(row1[7]).replace('"', '`').replace("'", "`"))
                sql3 = 'insert into tests_answers (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, right, question_id, sort_order, image, book_id, group_id, topic_id, type_id) VALUES ("'+n+'", "'+n+'", 0, "'+str(row1[8]).replace('"', '`').replace("'", "`")+'", "'+str(row1[9]).replace('"', '`').replace("'", "`")+'", "'+str(text)+'", "'+str(row1[7]).replace('"', '`').replace("'", "`")+'", "2", '+str(right_b)+', '+str(row2[0])+', 0, "", 49, 24, '+str(row2[9])+', 3)'
                print(sql3)
                c3.execute(sql3)
                conn.commit()
            if row1[10]!='':
                text=to_crl(str(row1[10]).replace('"', '`').replace("'", "`"))
                sql4 = 'insert into tests_answers (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, right, question_id, sort_order, image, book_id, group_id, topic_id, type_id) VALUES ("'+n+'", "'+n+'", 0, "'+str(row1[11]).replace('"', '`').replace("'", "`")+'", "'+str(row1[12]).replace('"', '`').replace("'", "`")+'", "'+str(text)+'", "'+str(row1[10]).replace('"', '`').replace("'", "`")+'", "3", '+str(right_c)+', '+str(row2[0])+', 0, "", 49, 24, '+str(row2[9])+', 3)'
                print(sql4)
                c4.execute(sql4)
                conn.commit()
            if row1[13]!='':
                text=to_crl(str(row1[13]).replace('"', '`').replace("'", "`"))
                sql5 = 'insert into tests_answers (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, right, question_id, sort_order, image, book_id, group_id, topic_id, type_id) VALUES ("'+n+'", "'+n+'", 0, "'+str(row1[14]).replace('"', '`').replace("'", "`")+'", "'+str(row1[15]).replace('"', '`').replace("'", "`")+'", "'+str(text)+'", "'+str(row1[13]).replace('"', '`').replace("'", "`")+'", "4", '+str(right_d)+', '+str(row2[0])+', 0, "", 49, 24, '+str(row2[9])+', 3)'
                print(sql5)
                c5.execute(sql5)
                conn.commit()
            break
    # english = translator.translate(row[7], src='uzbek', dest='english').text.replace("'", "`")
    # russian = translator.translate(row[7], src='uzbek', dest='russian').text.replace("'", "`")

c1.close()
c2.close()
c3.close()
c4.close()
c5.close()
conn.close()
