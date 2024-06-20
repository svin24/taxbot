from flask import Flask, jsonify, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
import openai
from sqlalchemy.sql.sqltypes import NullType

class TaxBase(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=TaxBase)

taxBot = Flask(__name__)
taxBot.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxbot_data.db'

## database setup araea
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

# OpenAI - TaxBot integration
with open('api_key','r') as file:
    openai.api_key = file.read().strip()

def get_ai_response(prompt):
    try:
        response = openai.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {"role": "system", "content": """You are a digital assistant designed to help people do their Taxes. You will recieve messages in the following format income=Number expenses=Number, prompt=Text. Sometimes income and expenses might be undefined, if that is the case ignore them completely and focus on the prompt."""},
                {"role": "user", "content": prompt }
            ]
        )
        return response.choices[0].message.content
    except Exception:
        return "Error getting response from taxbot"

# data integrity income and expenses MAY be null
def data_integrity(income,expenses,prompt):
    try:
        income = float(income)
        expenses = float(expenses)
    except ValueError:
        # error is handled with an alert box right now. It's fine for an assignment but not a real world program
        return jsonify({'error': 'Income and Expenses must be numbers'}),400
    
    tax_data = TaxData(income=income,expenses=expenses,prompt=prompt)
    db.session.add(tax_data)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occured'}),500
    
    return None

# Flask routing
@taxBot.route('/')
def home():
    return render_template("index.html")

@taxBot.route('/submit', methods=['POST'])
def submit():
    income = None
    expenses = None

    income = request.form['income']
    expenses = request.form['expenses']
    prompt = request.form['prompt']

    data_integrity(income,expenses,prompt)
    
    final_prompt = 'income={} expenses={}, prompt={}'.format(income,expenses,prompt)

    ai_response = get_ai_response(final_prompt)

    return jsonify({
        'income': income,
        'expenses': expenses,
        'prompt': prompt,
        'ai_response': ai_response
    })

if __name__ == '__main__':
    taxBot.run(debug=True)
