import sqlite3
from datetime import datetime

def migrate_missing_answers():
    try:
        # Bazaga ulanish
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # tests_answers jadvalidagi mavjud question_id larni olish
        cursor.execute("""
            SELECT DISTINCT question_id FROM tests_answers
        """)
        existing_question_ids = {row[0] for row in cursor.fetchall()}

        # tests_questions jadvalidagi barcha question_id larni olish
        cursor.execute("""
            SELECT id FROM tests_questions
        """)
        all_question_ids = {row[0] for row in cursor.fetchall()}

        # tests_questions jadvalidagi question_id lar orasidan tests_answers jadvalidagi mavjud bo'lmaganlarini topish
        missing_question_ids = all_question_ids - existing_question_ids
        print(existing_question_ids.issubset(all_question_ids))
        print(f"Jami savollar: {len(all_question_ids)}")
        print(all_question_ids.issubset(existing_question_ids))
        print(f"Mavjud javoblar: {len(existing_question_ids)}")
        print(missing_question_ids.issubset(all_question_ids))
        print(f"Topilmagan savollar: {len(missing_question_ids)}")
        if not missing_question_ids:
            print("Barcha savollar uchun javoblar mavjud!")
            return

        # Har bir question_id uchun
        for question_id in missing_question_ids:
            # tests_questions jadvalidan savol ma'lumotlarini olish
            cursor.execute("""
                SELECT name_uz_uz FROM tests_questions WHERE id = ?
            """, (question_id,))
            question = cursor.fetchone()
            if not question:
                print(f"XATO: question_id = {question_id} uchun savol topilmadi")
                continue

            # projects_avtotests jadvalidan javoblarni olish
            cursor.execute("""
                SELECT 
                    javob_a, javob_a_en, javob_a_ru,
                    javob_b, javob_b_en, javob_b_ru,
                    javob_c, javob_c_en, javob_c_ru,
                    javob_d, javob_d_en, javob_d_ru,
                    javob
                FROM projects_avtotest 
                WHERE savol = ?
            """, (question[0],))
            answers = cursor.fetchone()
            if not answers:
                print(f"XATO: question_id = {question_id} uchun javoblar topilmadi")
                continue

            # Javoblarni kiritish
            answers_to_insert = []
            
            # A variant
            answers_to_insert.append({
                'number': 1,
                'name_en_us': answers[1],
                'name_ru_ru': answers[2],
                'name_uz_uz': answers[0],
                'name_uz_crl': answers[0],
                'right': 1 if answers[12] == 'A' else 0
            })
            
            # B variant
            answers_to_insert.append({
                'number': 2,
                'name_en_us': answers[4],
                'name_ru_ru': answers[5],
                'name_uz_uz': answers[3],
                'name_uz_crl': answers[3],
                'right': 1 if answers[12] == 'B' else 0
            })
            
            # C variant (agar bo'sh bo'lmasa)
            if answers[6] and answers[6].strip():
                answers_to_insert.append({
                    'number': 3,
                    'name_en_us': answers[7],
                    'name_ru_ru': answers[8],
                    'name_uz_uz': answers[6],
                    'name_uz_crl': answers[6],
                    'right': 1 if answers[12] == 'C' else 0
                })
            
            # D variant (agar bo'sh bo'lmasa)
            if answers[9] and answers[9].strip():
                answers_to_insert.append({
                    'number': 4,
                    'name_en_us': answers[10],
                    'name_ru_ru': answers[11],
                    'name_uz_uz': answers[9],
                    'name_uz_crl': answers[9],
                    'right': 1 if answers[12] == 'D' else 0
                })

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                # Javoblarni tests_answers jadvaliga qo'shish
                for answer in answers_to_insert:
                    cursor.execute("""
                        INSERT INTO tests_answers (
                            question_id, number, 
                            name_en_us, name_ru_ru, name_uz_uz, name_uz_crl,
                            right, created_at, updated_at, is_deleted, image, sort_order, created_by_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        question_id,
                        answer['number'],
                        answer['name_en_us'],
                        answer['name_ru_ru'],
                        answer['name_uz_uz'],
                        answer['name_uz_crl'],
                        answer['right'],
                        current_time,
                        current_time,
                        0,  # is_deleted = False
                        '',  # image = NULL (yoki bo'sh qiymat)
                        0,
                        1
                    ))
                print(f"Javoblar qo'shildi: question_id = {question_id}")

            except sqlite3.Error as e:
                print(f"XATO: question_id = {question_id} uchun javoblarni qo'shishda xatolik yuz berdi: {str(e)}")
                continue

        # Oxirgi o'zgarishlarni saqlash
        conn.commit()
        print(f"\nMigratsiya muvaffaqiyatli yakunlandi! Jami {len(missing_question_ids)} ta savol uchun javoblar qo'shildi.")

    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_missing_answers() 