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

            # Javoblarni kiritish
            answers_to_insert = [
                {
                    'number': 1,
                    'name_en_us': 'Option A',
                    'name_ru_ru': 'Вариант A',
                    'name_uz_uz': 'A variant',
                    'name_uz_crl': 'A вариант',
                    'right': 1
                },
                {
                    'number': 2,
                    'name_en_us': 'Option B',
                    'name_ru_ru': 'Вариант B',
                    'name_uz_uz': 'B variant',
                    'name_uz_crl': 'B вариант',
                    'right': 0
                },
                {
                    'number': 3,
                    'name_en_us': 'Option C',
                    'name_ru_ru': 'Вариант C',
                    'name_uz_uz': 'C variant',
                    'name_uz_crl': 'C вариант',
                    'right': 0
                },
                {
                    'number': 4,
                    'name_en_us': 'Option D',
                    'name_ru_ru': 'Вариант D',
                    'name_uz_uz': 'D variant',
                    'name_uz_crl': 'D вариант',
                    'right': 0
                }
            ]

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