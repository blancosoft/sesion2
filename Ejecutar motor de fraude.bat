@echo off
cd /d "%~dp0"
py motor_fraude.py
if errorlevel 1 python motor_fraude.py
