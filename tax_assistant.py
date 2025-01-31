# Ioannis Iliopoulos
import os
from flask import Flask, json, jsonify, message_flashed, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import except_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
import openai

class TaxBase(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=TaxBase)

taxBot = Flask(__name__)
taxBot.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxbot_data.db'

## database setup area
db.init_app(taxBot)

class TaxData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    income: Mapped[float] = mapped_column(nullable=True)
    expenses: Mapped[float] = mapped_column(nullable=True)
    prompt: Mapped[str]
    ai_resp: Mapped[str]

    def __init__(self, income, expenses, prompt, ai_resp):
        self.income = income
        self.expenses = expenses
        self.prompt = prompt
        self.ai_resp = ai_resp

with taxBot.app_context():
    db.create_all()

# OpenAI - TaxBot integration
if os.environ.get("OPENAI_API_KEY") is None: 
    try:
        with open('api_key','r') as file:
            openai.api_key = file.read().strip()
    except FileNotFoundError:
        print("OPENAI key not provided, Application will not have AI integration")
elif os.environ.get("OPENAI_API_KEY") is not None:
    openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(prompt, past_interactions):
    try:
        messages = [
            {"role": "system", "content": """You are a digital assistant designed to help people do their Taxes. You will recieve messages in the following format income=Number expenses=Number, prompt=Text. Sometimes the values income and expenses may not be set, in that case just ignore them, in addition to that you will recieve context about previous interactions before the current prompt"""}
        ]
        
        # NOT EFFICIENT AT ALL
        for interaction in past_interactions:
            messages.append({"role":"user","content": interaction.prompt})
            messages.append({"role":"assistant", "content": interaction.ai_resp})
        
        messages.append({"role":"user","content": prompt})

        response = openai.chat.completions.create(
            model = "gpt-4o",
            messages = messages
        )
        return response.choices[0].message.content
    
    except Exception:
        return "Error getting response from taxbot, check your openAI key and or internet connection"



def data_integrity_database(income,expenses,prompt,ai_resp):

    tax_data = TaxData(income=income,expenses=expenses,prompt=prompt, ai_resp=ai_resp)
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


## various RESTFUL stuff here
# Get all data for recovery 
@taxBot.route('/log', methods=['GET'])
def get_log():
    log = []
    all_data = TaxData.query.all()
    for tax_data in all_data:
        log.append({
        'id': tax_data.id,
        'income': tax_data.income,
        'expenses': tax_data.expenses,
        'prompt': tax_data.prompt,
        'ai_resp': tax_data.ai_resp
        })
    return jsonify(log)


@taxBot.route('/submit', methods=['POST'])
def submit():
    try:
        income = float(request.form['income'])
    except ValueError:
        income = None
    
    try:
        expenses = float(request.form['expenses'])
    except ValueError:
        expenses = None
    
    try:
        prompt = request.form['prompt']
    except ValueError:
        return jsonify({'error':'Unknown issue with text field'}),400

    past_interactions = TaxData.query.all()
    final_prompt = 'income={} expenses={}, prompt={}'.format(income,expenses,prompt)
    ai_response = get_ai_response(final_prompt, past_interactions)

    data_integrity_database(income,expenses,prompt,ai_response)

    return jsonify({
        'income': income,
        'expenses': expenses,
        'prompt': prompt,
        'ai_response': ai_response
    })

# data indexing
@taxBot.route('/data/<int:id>', methods=['GET'])
def get_data(id):
    tax_data = TaxData.query.get(id)
    if tax_data:
        return jsonify({
            'id': tax_data.id,
        'income': tax_data.income,
        'expenses': tax_data.expenses,
        'prompt': tax_data.prompt,
        'ai_resp': tax_data.ai_resp
    })
    else:
        return jsonify({'error':'Data Not Found'}),404

# data deletion
@taxBot.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    tax_data = TaxData.query.get(id)
    if tax_data:
        db.session.delete(tax_data)
        db.session.commit()
        message = 'Data ID:{} deleted'.format(tax_data.id)
        return jsonify({'message': message})
    else:
        return jsonify({'error':'Data Not Found'}),404

if __name__ == '__main__':
    # something funny for docker testing
    taxBot.run(debug=True, host="0.0.0.0")
