from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')

# 업로드 설정
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'doc', 'docx', 'hwp', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return '.' in filename and (ext in ALLOWED_IMAGE_EXTENSIONS or ext in ALLOWED_FILE_EXTENSIONS)

def is_image(filename):
    return filename.rsplit('.', 1)[-1].lower() in ALLOWED_IMAGE_EXTENSIONS

# 카테고리
CATEGORIES = {
    'policy': '개인채무자보호법 관련 내부 기준',
    'auction': '경매 예정 통기서',
    'notice': '개인 채무자보호 관련 공고',
    'privacy': '개인정보 처리방침',
    'assets': '기타 유동화 자산관련 공고',
    'qna': 'QnA'
}

posts = []

# 기본 라우트
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

# 게시판 홈
@app.route("/management/board")
def board_home():
    return render_template("management/board/board_home.html", categories=CATEGORIES)

# 게시판 목록
@app.route("/management/board/<category>")
def board_list(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404
    category_posts = sorted(
        [p for p in posts if p['category'] == category],
        key=lambda x: x['date'],
        reverse=True
    )
    return render_template("management/board/board_list.html",
                           category=category,
                           category_name=CATEGORIES[category],
                           posts=category_posts)

# 글쓰기 비밀번호 확인
@app.route("/management/board/<category>/check", methods=['GET', 'POST'])
def board_check(category):
    if request.method == 'POST':
        if request.form.get('password') == POST_PASSWORD:
            return redirect(url_for('board_write', category=category))
        flash("비밀번호가 틀렸습니다.", "error")
    return render_template("management/board/board_check.html",
                           category=category,
                           category_name=CATEGORIES.get(category, ""))

# 게시글 작성
@app.route("/management/board/<category>/write", methods=['GET', 'POST'])
def board_write(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        file = request.files.get('file')

        image_url = None
        file_url = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            url = '/' + path.replace("\\", "/")
            if is_image(filename):
                image_url = url
            else:
                file_url = url

        post = {
            'id': len(posts) + 1,
            'category': category,
            'title': title,
            'content': content,
            'author': author,
            'image_url': image_url,
            'file_url': file_url,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        posts.append(post)
        flash("게시글이 등록되었습니다.", "success")
        return redirect(url_for('board_list', category=category))

    return render_template("management/board/board_write.html",
                           category=category,
                           category_name=CATEGORIES[category])

# 게시글 상세보기
@app.route("/management/board/<category>/post/<int:post_id>")
def board_post(category, post_id):
    post = next((p for p in posts if p['id'] == post_id and p['category'] == category), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("management/board/board_post.html",
                           post=post,
                           category=category,
                           category_name=CATEGORIES[category])

# 게시글 수정
@app.route("/management/board/<category>/edit/<int:post_id>", methods=['GET', 'POST'])
def board_edit(category, post_id):
    post = next((p for p in posts if p['id'] == post_id and p['category'] == category), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        flash("게시글이 수정되었습니다.", "success")
        return redirect(url_for('board_post', category=category, post_id=post_id))

    return render_template("management/board/board_edit.html",
                           post=post,
                           category=category,
                           category_name=CATEGORIES[category])

# 게시글 삭제
@app.route("/management/board/<category>/delete/<int:post_id>", methods=['POST'])
def board_delete(category, post_id):
    global posts
    posts = [p for p in posts if not (p['id'] == post_id and p['category'] == category)]
    flash("게시글이 삭제되었습니다.", "success")
    return redirect(url_for('board_list', category=category))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)