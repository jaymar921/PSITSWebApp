@echo off
color 0f

call venv\Scripts\activate
echo ---------------------------------
echo      [STARTING VIRTUAL ENV]
echo call venv\Scripts\activate
echo      [STARTING SERVER]
echo.
echo  _____   _____ _____ _______ _____ 
echo ^|  __ \ / ____^|_   _^|__   __/ ____^|
echo ^| ^|__) ^| (___   ^| ^|    ^| ^| ^| (___  
echo ^|  ___/ \___ \  ^| ^|    ^| ^|  \___ \ 
echo ^| ^|     ____) ^|_^| ^|_   ^| ^|  ____) ^|
echo ^|_^|    ^|_____/^|_____^|  ^|_^| ^|_____/   
echo  [Web App: Developed by Jayharron Abejar]
echo  to exit: do 'ctrl + C'  
echo.     
echo python -m PSITSweb.webapp                       
echo ---------------------------------
python PSITSweb\webapp.py
pause