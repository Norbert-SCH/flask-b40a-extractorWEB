from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

def extract_b40_values(file_content):
    lines = file_content.splitlines()
    return [line for line in lines if 'B40' in line]

HTML_TEMPLATE = """
<!doctype html>
<title>B40 Extractor</title>
<h2>Datei hochladen</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if error %}
  <p style="color:red;"><strong>Fehler: {{ error }}</strong></p>
{% endif %}
{% if results %}
  <h3>Gefundene B40-Zeilen:</h3>
  <ul>
  {% for line in results %}
    <li>{{ line }}</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    results = []
    error = None
    if request.method == "POST":
        try:
            uploaded_file = request.files.get("file")
            if not uploaded_file:
                error = "Keine Datei hochgeladen."
            else:
                content = uploaded_file.read().decode("utf-8")
                results = extract_b40_values(content)
        except Exception as e:
            error = str(e)
    return render_template_string(HTML_TEMPLATE, results=results, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


