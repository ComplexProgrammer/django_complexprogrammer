@echo off
chcp 65001 > nul
title AvtoTest Telegram Bot (@AvtoTestUzbBot)
echo ======================================================
echo    @AvtoTestUzbBot - Telegram Avtotest Boti
echo    Loyiha: django_complexprogrammer
echo ======================================================
echo.

python run_bot.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Bot to'xtadi yoki xatolik yuz berdi.
    pause
)
