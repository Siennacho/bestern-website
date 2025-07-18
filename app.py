from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# ✅ PostgreSQL로 변경
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://bestern_db_user:NGhsgwMRfFRJiVifjxpWoMbqktWM3pTMf@dpg-d1ssn5idbo4c73f1qpeg-a:5432/bestern_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'hwp', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image_urls = db.Column(db.Text)
    file_urls = db.Column(db.Text)
    date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'image_urls': json.loads(self.image_urls or '[]'),
            'file_urls': json.loads(self.file_urls or '[]'),
            'date': self.date
        }

with app.app_context():
    db.create_all()

CATEGORIES = {
    'policy': '개인채무자보호법 관련 내부 기준',
    'auction': '경매 예정 통지서',
    'notice': '개인 채무자보호 관련 공고',
    'privacy': '개인정보 처리방침',
    'assets': '기타 유동화 자산관련 공고',
    'qna': 'QnA'
}

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
    posts = Post.query.filter_by(category=category).order_by(Post.date.desc()).all()
    post_dicts = [post.to_dict() for post in posts]
    return render_template("management/board/board_list.html", category=category, category_name=CATEGORIES[category], posts=post_dicts)

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

        new_post = Post(category=category, title=title, content=content, author=author,
                        image_urls=json.dumps(image_urls), file_urls=json.dumps(file_urls),
                        date=datetime.now().strftime('%Y-%m-%d'))
        db.session.add(new_post)
        db.session.commit()

        flash("게시글이 등록되었습니다.", "success")
        return redirect(url_for('board_list', category=category))

    return render_template("management/board/board_write.html", category=category, category_name=CATEGORIES[category])

@app.route("/management/board/<category>/post/<int:post_id>")
def board_post(category, post_id):
    post = Post.query.filter_by(id=post_id, category=category).first()
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("management/board/board_post.html", post=post.to_dict(), category=category, category_name=CATEGORIES[category])

@app.route("/notice")
def notice_list():
    posts = Post.query.filter_by(category='notice_announcement').order_by(Post.date.desc()).all()
    post_dicts = [post.to_dict() for post in posts]
    return render_template("noticeboard/notice_list.html", posts=post_dicts)

@app.route("/notice/write", methods=['GET', 'POST'])
def notice_write():
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

        new_post = Post(category='notice_announcement', title=title, content=content, author=author,
                        image_urls=json.dumps(image_urls), file_urls=json.dumps(file_urls),
                        date=datetime.now().strftime('%Y-%m-%d'))
        db.session.add(new_post)
        db.session.commit()

        flash("공시 게시글이 등록되었습니다.", "success")
        return redirect(url_for('notice_list'))

    return render_template("noticeboard/notice_write.html")

@app.route("/notice/<int:post_id>")
def notice_post(post_id):
    post = Post.query.filter_by(id=post_id, category='notice_announcement').first()
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("noticeboard/notice_post.html", post=post.to_dict())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)