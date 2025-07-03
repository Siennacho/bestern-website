# ✅ 1. 모듈 import
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User

# ✅ 2. Flask 앱 설정
app = Flask(__name__)
app.secret_key = "your-secret-key"  # 세션 사용 시 필요

# ✅ 3. 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ✅ 4. DB 테이블 생성
with app.app_context():
    db.create_all()


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ✅ 5. 라우팅
@app.route("/")
def home():
    return render_template("index.html")

# ✅ 로그인 라우팅 (추가)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("로그인 성공!", "success")
            return redirect(url_for("home"))
        else:
            flash("아이디 또는 비밀번호가 틀렸습니다.", "danger")

    return render_template("login.html")


@app.route("/board")
def board():
    return render_template("board.html")


# ✅ 로그아웃 라우팅 (선택)
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("home"))

# ✅ 실행
if __name__ == "__main__":
    app.run(debug=True, port=5001)