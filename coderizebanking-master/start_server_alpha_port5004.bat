call venv/scripts/activate
color 6F
title CodeRizeBanking ALPHA 5004 Server

set LIFECYCLE=ALPHA

rem To run default django server
rem python manage.py runserver 0.0.0.0:5001

rem To Run with SSL
call python manage.py runsslserver 0.0.0.0:5004 --certificate "C:\Certbot\live\beta.fruitly.co.in\cert.pem" --key "C:\Certbot\live\beta.fruitly.co.in\privkey.pem"