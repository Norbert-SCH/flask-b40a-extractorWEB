from flask import Flask, request, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xls'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Verarbeitung: Extrahiere Zelle B40
            df = pd.read_excel(filepath, header=None, engine='xlrd')
            b40_value = df.iloc[39, 1]  # B40 = Zeile 40, Spalte 2 (Index 39, 1)

            # Ergebnisdatei erstellen
            result_path = os.path.join(RESULT_FOLDER, 'result.xlsx')
            result_df = pd.DataFrame({'B40': [b40_value]})
            result_df.to_excel(result_path, index=False)

            # Datei zum Download zurückgeben
            return send_file(result_path, as_attachment=True)

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
