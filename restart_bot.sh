#!/bin/bash
# @AvtoTestUzbBot ni qayta ishga tushirish: eski jarayonni to'xtatadi, yangisini fonda ishga tushiradi.
# Ishlatish:  bash restart_bot.sh          (to'xtatish uchun: bash restart_bot.sh stop)
cd "$(dirname "$0")"

# CloudLinux / cPanel thread limitini saqlash
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

PYTHON="${PYTHON:-python3}"
LOG="logs/bot.log"
PIDFILE="tmp/bot.pid"
# run_bot.py yoki "manage.py run_avtotest_bot" orqali ishga tushirilgan nusxalar
PATTERN="run_bot\.py|run_avtotest_bot"

mkdir -p logs tmp

stop_bot() {
    PIDS=$(pgrep -u "$(id -u)" -f "$PATTERN")
    if [ -z "$PIDS" ]; then
        echo "Ishlab turgan bot topilmadi."
        return
    fi
    echo "Bot to'xtatilmoqda (PID: $(echo $PIDS))..."
    kill $PIDS 2>/dev/null
    # 10 soniyagacha o'zi yopilishini kutamiz, keyin majburan to'xtatamiz
    for _ in $(seq 10); do
        sleep 1
        pgrep -u "$(id -u)" -f "$PATTERN" > /dev/null || break
    done
    if pgrep -u "$(id -u)" -f "$PATTERN" > /dev/null; then
        echo "Yopilmadi — majburan to'xtatilmoqda."
        pkill -9 -u "$(id -u)" -f "$PATTERN"
    fi
    rm -f "$PIDFILE"
    echo "To'xtatildi."
}

stop_bot
[ "$1" = "stop" ] && exit 0

echo "Bot ishga tushirilmoqda..."
echo "===== $(date '+%Y-%m-%d %H:%M:%S') restart =====" >> "$LOG"
nohup "$PYTHON" run_bot.py >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"

# Telegram'ga ulanishini 20 soniyagacha kutamiz
for _ in $(seq 20); do
    sleep 1
    if ! kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "❌ Bot ishga tushmadi. Log oxiri:"
        tail -n 25 "$LOG"
        exit 1
    fi
    if tail -n 50 "$LOG" | grep -q "Bot muvaffaqiyatli ishga tushdi"; then
        echo "✅ Bot ishlayapti (PID: $(cat "$PIDFILE"))."
        tail -n 50 "$LOG" | grep -E "muvaffaqiyatli|Kanalga savol joylash|XATOLIK|Error" | tail -n 5
        echo "Logni kuzatish: tail -f $LOG"
        exit 0
    fi
done
echo "⚠️ Jarayon ishlayapti, lekin 20 soniyada ulanish xabari chiqmadi. Log oxiri:"
tail -n 25 "$LOG"
