
# B40 XLS Extractor Flask App

Diese Webanwendung erlaubt das Hochladen mehrerer XLS(X)-Dateien und extrahiert alle Zeilen, die das Stichwort 'B40' enthalten. Die Ergebnisse werden als ZIP-Datei mit gefilterten Excel-Dateien zum Download bereitgestellt.

## Deployment auf Render

1. Dieses Repository auf GitHub hochladen
2. Bei [Render](https://render.com) anmelden
3. Neues Web Service erstellen und dieses Repo verbinden
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn main:app`

Die App wird unter einer öffentlichen URL erreichbar sein.
