@echo off
color 0f
call venv\Scripts\activate
echo ---------------------------------
echo      [STARTING VIRTUAL ENV]
echo call venv\Scripts\activate
echo        [STARTING SERVER]                
echo ---------------------------------
:run
py .\PSITSweb\webapp.py
pause
goto run