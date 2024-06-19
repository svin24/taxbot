from flask import Flask, jsonify, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

class TaxBase(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=TaxBase)

taxBot = Flask(__name__)
taxBot.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxbot_data.db'

db.init_app(taxBot)

class TaxData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    income: Mapped[float] = mapped_column(nullable=True)
    expenses: Mapped[float] = mapped_column(nullable=True)
    prompt: Mapped[str]

    def __init__(self, income, expenses, prompt):
        self.income = income
        self.expenses = expenses
        self.prompt = prompt

with taxBot.app_context():
    db.create_all()

@taxBot.route('/')
def home():
    return render_template("index.html")

@taxBot.route('/submit', methods=['POST'])
def submit():
    income = request.form['income']
    expenses = request.form['expenses']
    prompt = request.form['prompt']

    try:
        income = float(income)
        expenses = float(expenses)
    except ValueError:
        return jsonify({'error': 'Income and Expenses must be numbers'}),400
    # error is handled with an alert box right now. It's fine for an assignment but not a real world program

    # insert data into database
    tax_data = TaxData(income=income,expenses=expenses,prompt=prompt)
    db.session.add(tax_data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occured'}),500
    

    # AI not integrated yet
    ai_response = "Not Integrated"

    return jsonify({
        'income': income,
        'expenses': expenses,
        'prompt': prompt,
        'ai_response': ai_response
    })

if __name__ == '__main__':
    taxBot.run(debug=True)
