from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/board")
def board():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    
    posts = [
        {"title": "예시 게시글 1", "author": "관리자", "date": "2025-07-01", "content": "이건 테스트용 게시글입니다."},
        {"title": "예시 게시글 2", "author": "회원", "date": "2025-07-02", "content": "안녕하세요."}
    ]

    return render_template("board.html", user=user, posts=posts)

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

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("이미 존재하는 아이디입니다.", "warning")
            return redirect(url_for("register"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("회원가입 완료! 로그인 후 승인될 때까지 기다려주세요.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# 필요 시 글쓰기 라우트 추가 가능

if __name__ == "__main__":
    app.run(debug=True, port=5001)