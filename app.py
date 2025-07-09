from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/operation/returns")
def operation_returns():
    return render_template("operation/returns.html")

@app.route("/notice")
def notice():
    return render_template("notice.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)