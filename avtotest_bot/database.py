import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional
import aiosqlite

from .config import DB_PATH, UZB_AVTOTEST_BOOK_ID, CDL_USA_BOOK_ID

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)

    @asynccontextmanager
    async def connect(self):
        """aiosqlite xavfsiz asinxron ulanish kontekst menejeri."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            yield conn

    async def init_db(self):
        """Bot jadvallarini ma'lumotlar bazasida yaratish (mavjud bo'lmasa)."""
        async with self.connect() as db:
            # Foydalanuvchilar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS avtotest_bot_users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    lang TEXT DEFAULT 'uz',
                    total_tests INTEGER DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    wrong_answers INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Foydalanuvchi faol test sessiyasi
            await db.execute("""
                CREATE TABLE IF NOT EXISTS avtotest_bot_sessions (
                    user_id INTEGER PRIMARY KEY,
                    mode TEXT,
                    topic_id INTEGER,
                    title TEXT,
                    question_ids TEXT,
                    current_index INTEGER DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    mistakes INTEGER DEFAULT 0,
                    answers_history TEXT DEFAULT '{}',
                    last_message_id INTEGER,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Xatolar tarixi (xatolar ustida ishlash uchun)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS avtotest_bot_mistakes (
                    user_id INTEGER,
                    question_id INTEGER,
                    mistake_count INTEGER DEFAULT 1,
                    last_mistake_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, question_id)
                )
            """)

            await db.commit()
            logger.info("Bot ma'lumotlar bazasi jadvallari muvaffaqiyatli tekshirildi.")

    # ==================== FOYDALANUVCHILAR ====================

    async def get_or_create_user(self, user_id: int, username: Optional[str], full_name: str) -> Dict[str, Any]:
        async with self.connect() as db:
            async with db.execute("SELECT * FROM avtotest_bot_users WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                if row:
                    await db.execute(
                        "UPDATE avtotest_bot_users SET username = ?, full_name = ?, last_active = ? WHERE user_id = ?",
                        (username, full_name, datetime.now().isoformat(), user_id)
                    )
                    await db.commit()
                    return dict(row)

            now = datetime.now().isoformat()
            await db.execute("""
                INSERT INTO avtotest_bot_users (user_id, username, full_name, lang, created_at, last_active)
                VALUES (?, ?, ?, 'uz', ?, ?)
            """, (user_id, username, full_name, now, now))
            await db.commit()

            return {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "lang": "uz",
                "total_tests": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "wrong_answers": 0,
                "created_at": now,
                "last_active": now
            }

    async def update_user_lang(self, user_id: int, lang: str):
        async with self.connect() as db:
            await db.execute(
                "UPDATE avtotest_bot_users SET lang = ? WHERE user_id = ?",
                (lang, user_id)
            )
            await db.commit()

    async def get_user_lang(self, user_id: int) -> str:
        async with self.connect() as db:
            async with db.execute("SELECT lang FROM avtotest_bot_users WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                return row["lang"] if row and row["lang"] else "uz"

    async def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with self.connect() as db:
            async with db.execute("SELECT * FROM avtotest_bot_users WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def get_total_stats(self) -> Dict[str, Any]:
        async with self.connect() as db:
            async with db.execute("SELECT COUNT(*) as total_users FROM avtotest_bot_users") as cur:
                total_users = (await cur.fetchone())["total_users"]
            
            async with db.execute("SELECT SUM(total_tests) as total_tests, SUM(total_questions) as total_q FROM avtotest_bot_users") as cur:
                row = await cur.fetchone()
                total_tests = row["total_tests"] or 0
                total_q = row["total_q"] or 0

            return {
                "total_users": total_users,
                "total_tests": total_tests,
                "total_questions": total_q
            }

    async def get_all_user_ids(self) -> List[int]:
        async with self.connect() as db:
            async with db.execute("SELECT user_id FROM avtotest_bot_users") as cur:
                rows = await cur.fetchall()
                return [r["user_id"] for r in rows]

    # ==================== TESTLAR (BILETLAR VA SAVOLLAR) ====================

    async def get_topics(self, book_id: int = UZB_AVTOTEST_BOOK_ID) -> List[Dict[str, Any]]:
        """Biletlar ro'yxatini olish (masalan, 1-bilet, 2-bilet, ..., 108-bilet)."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id, number, name_uz_uz, name_ru_ru, book_id
                FROM tests_topics
                WHERE book_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                ORDER BY number ASC
            """, (book_id,)) as cur:
                rows = await cur.fetchall()
                return [dict(r) for r in rows]

    async def get_topic_by_id(self, topic_id: int) -> Optional[Dict[str, Any]]:
        async with self.connect() as db:
            async with db.execute("""
                SELECT id, number, name_uz_uz, name_ru_ru, book_id
                FROM tests_topics
                WHERE id = ?
            """, (topic_id,)) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def get_next_topic(self, current_topic_number: int, book_id: int = UZB_AVTOTEST_BOOK_ID) -> Optional[Dict[str, Any]]:
        async with self.connect() as db:
            async with db.execute("""
                SELECT id, number, name_uz_uz, name_ru_ru, book_id
                FROM tests_topics
                WHERE book_id = ? AND number = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                LIMIT 1
            """, (book_id, current_topic_number + 1)) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def get_bilet_question_ids(self, topic_id: int) -> List[int]:
        """Berilgan biletning savollar ID larini olish."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id FROM tests_questions
                WHERE topic_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                ORDER BY number ASC
            """, (topic_id,)) as cur:
                rows = await cur.fetchall()
                return [r["id"] for r in rows]

    async def get_random_exam_question_ids(self, book_id: int = UZB_AVTOTEST_BOOK_ID, count: int = 20) -> List[int]:
        """Tasodifiy imtihon uchun 20 ta savol ID lari."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id FROM tests_questions
                WHERE book_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                ORDER BY RANDOM() LIMIT ?
            """, (book_id, count)) as cur:
                rows = await cur.fetchall()
                return [r["id"] for r in rows]

    async def get_cdl_question_ids(self, count: int = 20) -> List[int]:
        """AQSh CDL testi savollari ID lari."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id FROM tests_questions
                WHERE book_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                ORDER BY RANDOM() LIMIT ?
            """, (CDL_USA_BOOK_ID, count)) as cur:
                rows = await cur.fetchall()
                return [r["id"] for r in rows]

    async def get_user_mistake_question_ids(self, user_id: int, count: int = 20) -> List[int]:
        """Foydalanuvchi oldin xato qilgan savollari ID lari."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT q.id FROM avtotest_bot_mistakes m
                JOIN tests_questions q ON m.question_id = q.id
                WHERE m.user_id = ? AND (q.is_deleted = 0 OR q.is_deleted IS NULL)
                ORDER BY m.mistake_count DESC, RANDOM()
                LIMIT ?
            """, (user_id, count)) as cur:
                rows = await cur.fetchall()
                return [r["id"] for r in rows]

    async def get_question(self, question_id: int) -> Optional[Dict[str, Any]]:
        """Savol ma'lumotlarini olish (rasm va matn)."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id, number, name_uz_uz, name_ru_ru, name_en_us, image, topic_id, book_id
                FROM tests_questions
                WHERE id = ?
            """, (question_id,)) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def get_answers(self, question_id: int) -> List[Dict[str, Any]]:
        """Savolning javob variantlarini olish."""
        async with self.connect() as db:
            async with db.execute("""
                SELECT id, number, name_uz_uz, name_ru_ru, name_en_us, image, "right"
                FROM tests_answers
                WHERE question_id = ? AND (is_deleted = 0 OR is_deleted IS NULL)
                ORDER BY number ASC
            """, (question_id,)) as cur:
                rows = await cur.fetchall()
                return [dict(r) for r in rows]

    # ==================== SESSIYALAR (FAOL TESTLAR) ====================

    async def create_session(self, user_id: int, mode: str, title: str, question_ids: List[int], topic_id: Optional[int] = None):
        async with self.connect() as db:
            q_ids_str = ",".join(str(i) for i in question_ids)
            await db.execute("""
                INSERT OR REPLACE INTO avtotest_bot_sessions 
                (user_id, mode, topic_id, title, question_ids, current_index, score, mistakes, answers_history, started_at)
                VALUES (?, ?, ?, ?, ?, 0, 0, 0, '{}', ?)
            """, (user_id, mode, topic_id, title, q_ids_str, datetime.now().isoformat()))
            await db.commit()

    async def get_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with self.connect() as db:
            async with db.execute("SELECT * FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                if not row:
                    return None
                data = dict(row)
                data["question_ids"] = [int(i) for i in data["question_ids"].split(",") if i]
                data["answers_history"] = json.loads(data["answers_history"] or "{}")
                return data

    async def update_session_answer(self, user_id: int, q_id: int, answer_id: int, is_correct: bool):
        async with self.connect() as db:
            async with db.execute("SELECT * FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                if not row:
                    return

            history = json.loads(row["answers_history"] or "{}")
            history[str(q_id)] = {
                "answer_id": answer_id,
                "is_correct": is_correct
            }
            score = row["score"] + (1 if is_correct else 0)
            mistakes = row["mistakes"] + (0 if is_correct else 1)

            await db.execute("""
                UPDATE avtotest_bot_sessions
                SET score = ?, mistakes = ?, answers_history = ?
                WHERE user_id = ?
            """, (score, mistakes, json.dumps(history), user_id))

            if not is_correct:
                await db.execute("""
                    INSERT INTO avtotest_bot_mistakes (user_id, question_id, mistake_count, last_mistake_at)
                    VALUES (?, ?, 1, ?)
                    ON CONFLICT(user_id, question_id) 
                    DO UPDATE SET mistake_count = mistake_count + 1, last_mistake_at = ?
                """, (user_id, q_id, datetime.now().isoformat(), datetime.now().isoformat()))
            else:
                await db.execute("""
                    DELETE FROM avtotest_bot_mistakes
                    WHERE user_id = ? AND question_id = ?
                """, (user_id, q_id))

            await db.commit()

    async def advance_session_index(self, user_id: int) -> int:
        async with self.connect() as db:
            async with db.execute("SELECT current_index FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                if not row:
                    return 0
                new_idx = row["current_index"] + 1

            await db.execute("UPDATE avtotest_bot_sessions SET current_index = ? WHERE user_id = ?", (new_idx, user_id))
            await db.commit()
            return new_idx

    async def update_last_message_id(self, user_id: int, message_id: int):
        async with self.connect() as db:
            await db.execute("UPDATE avtotest_bot_sessions SET last_message_id = ? WHERE user_id = ?", (message_id, user_id))
            await db.commit()

    async def finish_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with self.connect() as db:
            async with db.execute("SELECT * FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                if not row:
                    return None
                session_data = dict(row)
                session_data["question_ids"] = [int(i) for i in session_data["question_ids"].split(",") if i]
                session_data["answers_history"] = json.loads(session_data["answers_history"] or "{}")

            total_answered = len(session_data["answers_history"])
            correct = session_data["score"]
            wrong = session_data["mistakes"]

            await db.execute("""
                UPDATE avtotest_bot_users
                SET total_tests = total_tests + 1,
                    total_questions = total_questions + ?,
                    correct_answers = correct_answers + ?,
                    wrong_answers = wrong_answers + ?,
                    last_active = ?
                WHERE user_id = ?
            """, (total_answered, correct, wrong, datetime.now().isoformat(), user_id))

            await db.execute("DELETE FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,))
            await db.commit()

            return session_data

    async def cancel_session(self, user_id: int):
        async with self.connect() as db:
            await db.execute("DELETE FROM avtotest_bot_sessions WHERE user_id = ?", (user_id,))
            await db.commit()

db = Database()
