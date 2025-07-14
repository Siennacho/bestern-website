from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')  # 실제 배포 시 환경변수 설정 권장
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')    # 작성용 비밀번호

# 카테고리 정의
CATEGORIES = {
    'policy': '개인채무자보호법 관련 내부 기준',
    'auction': '경매 예정 통기서',
    'notice': '개인 채무자보호 관련 공고',
    'privacy': '개인정보 처리방침',
    'assets': '기타 유동화 자산관련 공고',
    'qna': 'QnA'
}

# 게시글 저장 리스트
posts = []

# 기본 페이지 라우팅
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/company")
def company():
    return render_template("company.html")

@app.route("/company/greeting")
def company_greeting():
    return render_template("company/greeting.html")

@app.route("/company/overview")
def company_overview():
    return render_template("company/overview.html")

@app.route("/company/orgchart")
def company_orgchart():
    return render_template("company/orgchart.html")

@app.route("/company/contact")
def company_contact():
    return render_template("company/contact.html")

@app.route("/management")
def management():
    return render_template("management.html")

@app.route("/management/overview")
def management_overview():
    return render_template("management/overview.html")

@app.route("/management/orgchart")
def management_orgchart():
    return render_template("management/orgchart.html")

@app.route("/management/secured")
def management_secured():
    return render_template("management/secured.html")

@app.route("/management/unsecured")
def management_unsecured():
    return render_template("management/unsecured.html")

@app.route("/management/performance")
def management_performance():
    return render_template("management/performance.html")

@app.route("/operation")
def operation():
    return render_template("operation.html")

@app.route("/operation/orgchart")
def operation_orgchart():
    return render_template("operation/orgchart.html")

@app.route("/operation/philosophy")
def operation_philosophy():
    return render_template("operation/philosophy.html")

@app.route("/notice")
def notice():
    return render_template("notice.html")

@app.route("/recruit")
def recruit():
    return render_template("recruit.html")

# 게시판 홈
@app.route("/board")
def board_home():
    return render_template("board_home.html", categories=CATEGORIES)

# 카테고리별 게시글 목록
@app.route("/board/<category>")
def board_list(category):
    if category not in CATEGORIES:
        return "존재하지 않는 게시판입니다.", 404
    category_name = CATEGORIES[category]
    category_posts = [p for p in posts if p['category'] == category]
    return render_template("board_list.html", category=category, category_name=category_name, posts=category_posts)

# 비밀번호 확인 후 글쓰기 진입
@app.route("/board/<category>/check", methods=['GET', 'POST'])
def board_check(category):
    if request.method == 'POST':
        password = request.form.get('password')
        if password == POST_PASSWORD:
            return redirect(url_for('board_write', category=category))
        flash("비밀번호가 틀렸습니다.", "error")
    return render_template("board_check.html", category=category, category_name=CATEGORIES.get(category, ""))

# 게시글 작성
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

# 게시글 보기
@app.route("/board/<category>/post/<int:post_id>")
def board_post(category, post_id):
    post = next((https://bestern-website.onrender.com/p for p in posts if p['id'] == post_id and p['category'] == category), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("board_post.html", post=post, category=category, category_name=CATEGORIES[category])

# 앱 실행
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)