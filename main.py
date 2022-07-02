from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:04041954-@localhost/testing_question'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Question(db.Model):
  __tablename__ = 'question'
  id_question = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.String(300))
  category = db.Column(db.String(100))
  type = db.Column(db.Integer)

  def __init__(self, question, category, type):
    self.question = question
    self.category = category
    self.type = type


class QuestionSchema(ma.Schema):
  class Meta:
    fields = ('id_question', 'question', 'category', 'type')


question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)


#Create a question
@app.route('/question/create', methods=['POST'])
def add_question():
  question = request.json['question']
  category = request.json['category']
  type = request.json['type']
  new_question = Question(question, category, type)
  db.session.add(new_question)
  db.session.commit()
  return question_schema.jsonify(new_question)


#Get All new_questions
@app.route('/question/show', methods=['GET'])
def get_questions():
  all_question = Question.query.all()
  result = questions_schema.dump(all_question)
  return jsonify(result)


#Get Single question
@app.route('/question/show/<id_question>', methods=['GET'])
def get_question(id_question):
  question_name = Question.query.get(id_question)
  return question_schema.jsonify(question_name)


#Update a question
@app.route('/question/update/<id_question>', methods=['PUT'])
def update_question(id_question):
  question_name = Question.query.get(id_question)
  question = request.json['question']
  category = request.json['category']
  type = request.json['type']
  question_name.question = question
  question_name.category = category
  question_name.type = type
  db.session.commit()
  return question_schema.jsonify(question_name)


#Delete question
@app.route('/question/delete/<id_question>', methods=['DELETE'])
def delete_question(id_question):
  question_name = Question.query.get(id_question)
  db.session.delete(question_name)
  db.session.commit()
  return question_schema.jsonify(question_name)


#Run server
if __name__ == '__main__':
  app.run(debug=True)
