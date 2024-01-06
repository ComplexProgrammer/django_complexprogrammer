import sqlite3
from googletrans import Translator
conn = sqlite3.connect('db.sqlite3')
c1 = conn.cursor()
i = 0
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

results = conn.execute("SELECT * from tests_answers where name_en_us='None' or name_ru_ru='None' or name_uz_crl='None'")   
# results = conn.execute("SELECT * from tests_questions")   
for row in results:
    if not str(row[7]).__contains__('    ') and row[7]!='   \t' and row[7]!='   ' and row[7]!='      ' and row[7]!='  ' and row[7]!='None' and row[7]!='\t\t' and row[7]!='  \t' and row[7]!=' ' and row[7]!=' \t\t' and row[7]!='\t' and row[7]!=' \t' and row[7]!='  \t\t ' and row[7]!='  \t\t':
        print(row)
        english = translator.translate(row[7], src='uzbek', dest='english').text.replace("'", "`")
        russian = translator.translate(row[7], src='uzbek', dest='russian').text.replace("'", "`")
        text=row[7]
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
        print(row[7], "->", english, "->", russian, "->", text)
        sql = "update tests_answers set name_en_us='"+english+"', name_ru_ru='"+russian+"', name_uz_crl='"+text+"' where id="+str(row[0])
        # print(sql)
        c1.execute(sql)
        conn.commit()
c1.close()
conn.close()
