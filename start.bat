@echo off
color 02
echo STARTING SERVER
call venv\Scripts\activate
python -m PSITSweb.webapp
pause