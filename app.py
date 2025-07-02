from flask import Flask, render_template
from models import db  # 추가

app = Flask(__name__)

# DB 설정 추가
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 라우팅
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# DB 테이블 생성
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)