from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'hwp', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 카테고리 맵
CATEGORIES = {
    'policy': '개인채무자보호법 관련 내부 기준',
    'auction': '경매 예정 통지서',
    'notice': '개인 채무자보호 관련 공고',
    'privacy': '개인정보 처리방침',
    'assets': '기타 유동화 자산관련 공고',
    'qna': 'QnA'
}

# 파일 필터 함수
def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return '.' in filename and (ext in ALLOWED_IMAGE_EXTENSIONS or ext in ALLOWED_FILE_EXTENSIONS)

def is_image(filename):
    return filename.rsplit('.', 1)[-1].lower() in ALLOWED_IMAGE_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/company/<subpage>")
def company(subpage):
    return render_template(f"company/{subpage}.html")

@app.route("/management/<subpage>")
def management(subpage):
    return render_template(f"management/{subpage}.html")

@app.route("/operation/<subpage>")
def operation(subpage):
    return render_template(f"operation/{subpage}.html")

@app.route("/recruit")
def recruit():
    return render_template("recruit.html")

@app.route("/management/board")
def board_home():
    return render_template("management/board/board_home.html", categories=CATEGORIES)

@app.route("/management/board/<category>")
def board_list(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404
    return render_template("management/board/board_list.html", category=category, category_name=CATEGORIES[category], posts=[])

@app.route("/management/board/<category>/check", methods=['GET', 'POST'])
def board_check(category):
    if request.method == 'POST':
        if request.form.get('password') == POST_PASSWORD:
            return redirect(url_for('board_write', category=category))
        flash("비밀번호가 틀렸습니다.", "error")
    return render_template("management/board/board_check.html", category=category, category_name=CATEGORIES.get(category, ""))

@app.route("/management/board/<category>/write", methods=['GET', 'POST'])
def board_write(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        image_files = request.files.getlist('images')
        attachment_files = request.files.getlist('files')
        image_urls = []
        file_urls = []

        for image in image_files:
            if image and allowed_file(image.filename) and is_image(image.filename):
                filename = secure_filename(image.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                new_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                image.save(filepath)
                image_urls.append(url_for('static', filename=f'uploads/{new_filename}'))

        for file in attachment_files:
            if file and allowed_file(file.filename) and not is_image(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                file_urls.append('/' + path.replace("\\", "/"))

        flash("게시글이 임시로 등록된 것으로 처리되었습니다. (DB 없음)", "success")
        return redirect(url_for('board_list', category=category))

    return render_template("management/board/board_write.html", category=category, category_name=CATEGORIES[category])

@app.route("/management/board/<category>/post/<int:post_id>")
def board_post(category, post_id):
    return "게시글 데이터가 없습니다. (DB 비활성화됨)", 404

@app.route("/notice")
def notice_list():
    return render_template("noticeboard/notice_list.html", posts=[])

@app.route("/notice/write", methods=['GET', 'POST'])
def notice_write():
    if request.method == 'POST':
        flash("공시 게시글이 임시로 등록된 것으로 처리되었습니다. (DB 없음)", "success")
        return redirect(url_for('notice_list'))
    return render_template("noticeboard/notice_write.html")

@app.route("/notice/<int:post_id>")
def notice_post(post_id):
    return "게시글 데이터가 없습니다. (DB 비활성화됨)", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)