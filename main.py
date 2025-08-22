from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xls'):
            # Speichere die Datei im temporären Verzeichnis
            filepath = os.path.join('/tmp', file.filename)
            file.save(filepath)

            # Verarbeitung: Extrahiere Zelle B40
            df = pd.read_excel(filepath, header=None, engine='xlrd')
            b40_value = df.iloc[39, 1]  # B40 = Zeile 40, Spalte 2 (Index 39, 1)

            # Ergebnisdatei im temporären Verzeichnis erstellen
            result_path = os.path.join('/tmp', 'result.xlsx')
            result_df = pd.DataFrame({'B40': [b40_value]})
            result_df.to_excel(result_path, index=False)

            # HTML-Bestätigungsseite mit Download-Link
            confirmation_html = f'''
            <h2>Datei erfolgreich verarbeitet!</h2>
            <p>Der extrahierte Wert aus Zelle B40 lautet: <strong>{b40_value}</strong></p>
            <a href="/download" target="_blank">
                <button>Ergebnisdatei herunterladen</button>
            </a>
            '''
            return render_template_string(confirmation_html)

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/download')
def download_file():
    result_path = os.path.join('/tmp', 'result.xlsx')
    return send_file(result_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
