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
                try:
                    content = uploaded_file.read().decode("utf-8")
                except UnicodeDecodeError:
                    # Fallback auf ISO-8859-1 (Windows-Standard)
                    content = uploaded_file.read().decode("latin1")
                results = extract_b40_values(content)
        except Exception as e:
            error = str(e)
    return render_template_string(HTML_TEMPLATE, results=results, error=error)
