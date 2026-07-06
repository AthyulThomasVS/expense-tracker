import time
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://admin:admin123@postgres-db:5432/expense_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)


'''with app.app_context():
    db.create_all()'''

for i in range(10):
    try:
        with app.app_context():
            db.create_all()
        print("Connected to PostgreSQL!")
        break
    except Exception:
        print(f"Waiting for PostgreSQL... ({i+1}/10)")
        time.sleep(2)


@app.route("/")
def home():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add_expense():
    expense = Expense(
        title=request.form["title"],
        amount=float(request.form["amount"]),
        category=request.form["category"]
    )

    db.session.add(expense)
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    expense = Expense.query.get_or_404(id)

    if request.method == "POST":
        expense.title = request.form["title"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]

        db.session.commit()

        return redirect("/")

    return render_template("edit.html", expense=expense)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)