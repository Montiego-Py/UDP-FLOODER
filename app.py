import os
os.system("pip install flask")
from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import subprocess

app = Flask(__name__)

# Maksimum upload boyutu (ör: 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

HTML = """
<!doctype html>
<title>Dosya Yönetim Sistemi</title>
<h2>Dosya İşlemleri</h2>
<ul>
  <li><a href="/">Yeni Dosya Oluştur / Ekle</a></li>
  <li><a href="/upload">Dosya Yükle</a></li>
  <li><a href="/list">Dosyaları Listele ve Düzenle</a></li>
  <li><a href="/terminal">Terminal (Sınırlı)</a></li>
</ul>
"""

CREATE_HTML = HTML + """
<h3>Yeni Dosya Oluştur / İçerik Ekle</h3>
<form method=post action="/">
  Dosya Yolu/Adı: <input type=text name=filename required placeholder="ör: alt/dizin/dosya.txt"><br><br>
  İçerik: <br>
  <textarea name=content rows=5 cols=50 required></textarea><br><br>
  <input type=submit value="Kaydet">
</form>
<pre>{{message}}</pre>
"""

UPLOAD_HTML = HTML + """
<h3>Dosya Yükle</h3>
<form method=post enctype=multipart/form-data action="/upload">
  Dosya Yolu/Adı (isteğe bağlı, yoksa orijinal adı kullanılır): 
  <input type=text name=filename placeholder="ör: alt/dizin/dosya.txt"><br><br>
  Dosya Seç: <input type=file name=file required><br><br>
  <input type=submit value="Yükle">
</form>
<pre>{{message}}</pre>
"""

LIST_HTML = HTML + """
<h3>Dosyaları Listele (Mevcut Çalışma Dizini)</h3>
<ul>
{% for file in files %}
  <li>{{file}} - <a href="/edit/{{file}}">Düzenle</a> | <a href="/download/{{file}}">İndir</a></li>
{% endfor %}
</ul>
<pre>{{message}}</pre>
"""

EDIT_HTML = HTML + """
<h3>'{{filename}}' Dosyasını Düzenle</h3>
<form method=post action="/edit/{{filename}}">
  İçerik: <br>
  <textarea name=content rows=10 cols=50 required>{{content}}</textarea><br><br>
  <input type=submit value="Kaydet">
</form>
<pre>{{message}}</pre>
"""

TERMINAL_HTML = HTML + """
<h3>Sınırlı Terminal</h3>
<p>Desteklenen komutlar: ls [dizin], pwd, cat dosya</p>
<form method=post action="/terminal">
  Komut: <input type=text name=command required placeholder="ör: ls veya cat dosya.txt"><br><br>
  <input type=submit value="Çalıştır">
</form>
<pre>{{output}}</pre>
"""

@app.route("/", methods=["GET", "POST"])
def create():
    message = ""
    if request.method == "POST":
        filename = request.form.get("filename", "").strip()
        content = request.form.get("content", "").strip()
        if filename and content:
            path = os.path.normpath(filename)
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
            message = f"✅ '{filename}' dosyasına içerik eklendi!"
    return render_template_string(CREATE_HTML, message=message)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = ""
    if request.method == "POST":
        if 'file' not in request.files:
            message = "❌ Dosya bulunamadı!"
        else:
            file = request.files['file']
            filename = request.form.get("filename", "").strip() or file.filename
            if filename == '':
                message = "❌ Dosya adı boş!"
            else:
                path = os.path.normpath(filename)
                os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
                file.save(path)
                message = f"✅ '{filename}' dosyası yüklendi!"
    return render_template_string(UPLOAD_HTML, message=message)

@app.route("/list")
def list_files():
    files = []
    current_dir = os.getcwd()
    for root, dirs, filenames in os.walk(current_dir):
        for fname in filenames:
            rel_path = os.path.relpath(os.path.join(root, fname), current_dir)
            files.append(rel_path)
    return render_template_string(LIST_HTML, files=sorted(files), message="")

@app.route("/edit/<path:filename>", methods=["GET", "POST"])
def edit(filename):
    path = os.path.normpath(filename)
    if not os.path.exists(path):
        return redirect(url_for('list_files'))
    
    message = ""
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        message = f"✅ '{filename}' dosyası güncellendi!"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return render_template_string(EDIT_HTML, filename=filename, content=content, message=message)

@app.route("/download/<path:filename>")
def download(filename):
    directory = os.path.dirname(os.path.normpath(filename))
    basename = os.path.basename(filename)
    return send_from_directory(directory or '.', basename, as_attachment=True)

@app.route("/terminal", methods=["GET", "POST"])
def terminal():
    output = ""
    if request.method == "POST":
        command = request.form.get("command", "").strip()
        cmd_parts = command.split()
        if not cmd_parts:
            output = "❌ Komut boş!"
        else:
            allowed_commands = ['ls', 'pwd', 'cat']
            if cmd_parts[0] not in allowed_commands:
                output = f"❌ Yalnızca şu komutlar desteklenir: {', '.join(allowed_commands)}"
            else:
                try:
                    output = subprocess.check_output(cmd_parts, text=True, stderr=subprocess.STDOUT)
                except Exception as e:
                    output = f"❌ Hata: {str(e)}"
    return render_template_string(TERMINAL_HTML, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
