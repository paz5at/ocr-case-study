import os
import tempfile
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from ocr_script import extract_text

app = Flask(__name__)

# allowed image file extensions
extensions = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

# to run my front end
@app.get("/")
def index():
    return render_template("index.html")

# check my apis 
@app.get("/health")
def health():
    return jsonify(ok=True, status="healthy"), 200

# to allow uploads without azure for now
@app.post("/api/v1/ocr_upload")
def ocr_upload():
    if 'file' not in request.files:
        return jsonify(ok=False, error="No file provided"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(ok=False, error="Empty filename"), 400
    if not allowed_file(file.filename):
        return jsonify(ok=False, error="File type not allowed"), 400
    filename = secure_filename(file.filename)

    #save to a temporary file for convenience
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        temp_path = temp.name

    # run ocr script i made
    try:
        results = []
        for text, conf in extract_text(temp_path):
            results.append({"text": text, "confidence": conf})
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
    finally:
        os.remove(temp_path)
    return jsonify(ok=True, results=results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
