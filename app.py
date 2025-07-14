from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')

# 게시판 카테고리 정의
CATEGORIES = {
    'policy': '개인채무자보호법 관련 내부 기준',
    'auction': '경매 예정 통기서',
    'notice': '개인 채무자보호 관련 공고',
    'privacy': '개인정보 처리방침',
    'assets': '기타 유동화 자산관련 공고',
    'qna': 'QnA'
}
posts = []

# 기본 페이지
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

@app.route("/notice")
def notice():
    return render_template("notice.html")

@app.route("/recruit")
def recruit():
    return render_template("recruit.html")

@app.route("/board")
def board_home():
    return render_template("board_home.html", categories=CATEGORIES)

@app.route("/board/<category>")
def board_list(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404
    category_name = CATEGORIES[category]
    category_posts = [p for p in posts if p['category'] == category]
    return render_template("board_list.html", category=category, category_name=category_name, posts=category_posts)

@app.route("/board/<category>/check", methods=['GET', 'POST'])
def board_check(category):
    if request.method == 'POST':
        password = request.form.get('password')
        if password == POST_PASSWORD:
            return redirect(url_for('board_write', category=category))
        flash("비밀번호가 틀렸습니다.", "error")
    return render_template("board_check.html", category=category, category_name=CATEGORIES.get(category, ""))

@app.route("/board/<category>/write", methods=['GET', 'POST'])
def board_write(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = {
            'id': len(posts) + 1,
            'category': category,
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        posts.append(post)
        flash("게시글이 등록되었습니다.", "success")
        return redirect(url_for('board_list', category=category))
    return render_template("board_write.html", category=category, category_name=CATEGORIES[category])

@app.route("/board/<category>/post/<int:post_id>")
def board_post(category, post_id):
    post = next((p for p in posts if p['id'] == post_id and p['category'] == category), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("board_post.html", post=post, category=category, category_name=CATEGORIES[category])

# 비밀번호 확인 후 게시글 작성
@app.route('/write-secret', methods=['GET', 'POST'])
def write_secret():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == POST_PASSWORD:
            return render_template('write_form.html')
        else:
            flash('비밀번호가 틀렸습니다.', 'error')
    return render_template('password_check.html')

# 게시글 제출
@app.route('/submit-secret', methods=['POST'])
def submit_secret():
    title = request.form.get('title')
    content = request.form.get('content')
    with open("secret_posts.txt", "a", encoding='utf-8') as f:
        f.write(f"제목: {title}\n내용: {content}\n{'-'*40}\n")
    flash('게시글이 성공적으로 등록되었습니다!', 'success')
    return redirect('/')

# 게시글 보기
@app.route('/posts')
def view_posts():
    posts = []
    if os.path.exists("secret_posts.txt"):
        with open("secret_posts.txt", "r", encoding='utf-8') as f:
            content = f.read()
        raw_posts = content.strip().split('-' * 40)
        for post in raw_posts:
            lines = post.strip().split('\n')
            if len(lines) >= 2:
                title = lines[0].replace('제목: ', '')
                content = '\n'.join(lines[1:]).replace('내용: ', '')
                posts.append({'title': title, 'content': content})
    return render_template('posts.html', posts=posts)

# 실행
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)