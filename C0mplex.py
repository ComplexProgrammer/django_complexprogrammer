from datetime import datetime
import docx
import sqlite3 
conn = sqlite3.connect('db.sqlite3') 
cursor = conn.cursor()
javoblar =['1-B ','2-C ','3-D ','4-A ','5-C ','6-A ','7-B ','8-C ','9-B ','l0-D ','11-C ','12-A ','13-C ','14-A ','15-D ','16-D ','17-A ','18-B ','19-B ','20-C ','21-A ','22-B ','23-D ','24-C ','25-D ','26-B ','27-B ','28-A ','29-D ','30-A ','31-D ','32-D ','33-B ','34-B ','35-C ','36-B ','37- ','38-A ','39-B ','40-A ','41-C ','42-D ','43-B ','44-D ','45-D ','46-A ','47-B ','48-A ','49-B ','50-A ','51-D ','52-A ','53-B ','54-D ','55-B ','56-C ','57-D ','58-D ','59-C ','60-B ','61-B ','62-C ','63-D ','64-D ','65-B ','66-C ','67-A ','68-D ','69-B ','70-D ','7l-B ','72-A ','73-B ','74-C ','75-C ','76-B ','77-A ','78-A ','79-C ','80-D ','81-C ','82-A ','83-D ','84-C ','85-D ','86-A ','87-A ','88-C ','89-B ','90-B ','91-D ','92-A ','93-B ','94-B ','95-A ','96-B ','97-C ','98-B ','99-C ','l00-D ','101-B ','102-B ','103-A ','104-A ','105-B ','106-C ','107-A ','108-C ','109-D ','110-A ','111-A ','112-C ','113-A ','114-D ','115-C ','116-A ','117-A ','118-A ','119-A ','120-D ','121-C ','122-C ','123-D ','124-B ','125-C ','126-B ','127-B ','128-C ','129-B ','130-C ','131-D ','132-A ','133-B ','134-A ','135-B ','136-A ','137-B ','138-C ','139-B ','140-B ','141-B ','142-A ','143-A ','144-C ','145-A ','146-B ','147-C ','148-B ','149-A ','150-D ','151-C ','152-C ','153-B ','154-B ','155-B ','156-C ','157-D ','158-D ','159-D ','160-B ','161-D ','162-C ','163-D ','164-B ','165-C ','166-C ','167-A ','168-D ','169-D ','170-A ','171-B ','172-C ','173-D ','174-D ','175-D ','176-D ','177-B ','178-A ','179-A ','180-C ','181-B ','182-C ','183-A ','184-D ','185-B ','186-A ','187-B ','188-B ','189-A ','190-B ','191-A ']
def getText(filename):
    row_savol = 0
    savol = 0
    javob = 0
    doc = docx.Document(filename)
    jj=0
    right=0
    for para in doc.paragraphs:
        row_savol=row_savol+1
        if str(para.text).__contains__('#'):
            javob = 0
            savol=savol+1
            j=str(javoblar[savol-1]).replace(str(savol)+'-', '')
            if j=='A ':
                jj=1
            if j=='B ':
                jj=2
            if j=='C ':
                jj=3
            if j=='D ':
                jj=4
            if j=='E ':
                jj=5
            text_savol=str(para.text).replace('#', '')
            print(str(savol)+'-savol -> '+text_savol+" "+str(jj))
            params=(datetime.now(), datetime.now(), '0', str(text_savol), '.', '.', '.', str(savol), '', '1')
            cursor.execute("insert into tests_questions (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, image, topic_id) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        if str(para.text).__contains__('@'):
            javob=javob+1
            if javob == jj:
                right=1
            else:
                right=0

            text_javob=str(para.text).replace('@', '')
            print(str(javob)+' -> '+text_javob+" "+ str(jj))
            params=(datetime.now(), datetime.now(), '0', str(text_javob), '.', '.', '.', str(javob), '', right, '1')
            cursor.execute("insert into tests_answers (created_at, updated_at, is_deleted, name_en_us, name_ru_ru, name_uz_crl, name_uz_uz, number, image, right, question_id) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        


getText(r'general_knowledge_test.docx')