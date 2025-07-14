from flask import Flask, render_template, request, flash, redirect
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')  # 실제 배포 시 환경변수 설정 권장
POST_PASSWORD = os.environ.get('POST_PASSWORD', 'bestern_pw')    # 작성용 비밀번호

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

@app.route("/management/resources")
def management_resources():
    return render_template("management/resources.html")

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

# 🔐 비밀번호 확인 페이지
@app.route('/write-secret', methods=['GET', 'POST'])
def write_secret():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == POST_PASSWORD:
            return render_template('write_form.html')  # 비공개 글 작성 페이지
        else:
            flash('비밀번호가 틀렸습니다.', 'error')
    return render_template('password_check.html')  # 비밀번호 입력 화면

# 📝 비공개 게시글 제출 처리
@app.route('/submit-secret', methods=['POST'])
def submit_secret():
    title = request.form.get('title')
    content = request.form.get('content')

    # 파일에 저장
    with open("secret_posts.txt", "a", encoding='utf-8') as f:
        f.write(f"제목: {title}\n내용: {content}\n{'-'*40}\n")

    flash('게시글이 성공적으로 등록되었습니다!', 'success')
    return redirect('/')

@app.route('/posts')
def view_posts():
    posts = []

    if os.path.exists("secret_posts.txt"):
        with open("secret_posts.txt", "r", encoding='utf-8') as f:
            content = f.read()

        # 게시글을 구분선으로 분리
        raw_posts = content.strip().split('-' * 40)
        for post in raw_posts:
            lines = post.strip().split('\n')
            if len(lines) >= 2:
                title = lines[0].replace('제목: ', '')
                content = '\n'.join(lines[1:]).replace('내용: ', '')
                posts.append({'title': title, 'content': content})

    return render_template('posts.html', posts=posts)

# 앱 실행
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)