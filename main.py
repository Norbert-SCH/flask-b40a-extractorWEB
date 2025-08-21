
from flask import Flask, request, send_file, render_template_string
import pandas as pd
import io
import zipfile

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>B40 XLS Extractor</title>
<h2>Upload XLS-Dateien</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=files multiple>
  <input type=submit value=Upload>
</form>
{% if download_link %}
  <p><a href="{{ download_link }}">Download Ergebnis</a></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("files")
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as zipf:
            for file in files:
                df = pd.read_excel(file, engine="openpyxl")
                b40_rows = df[df.apply(lambda row: row.astype(str).str.contains("B40").any(), axis=1)]
                result_io = io.BytesIO()
                b40_rows.to_excel(result_io, index=False)
                result_io.seek(0)
                zipf.writestr(f"B40_{file.filename}", result_io.read())
        output.seek(0)
        return send_file(output, mimetype="application/zip", as_attachment=True, download_name="b40_results.zip")
    return render_template_string(HTML_TEMPLATE)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

