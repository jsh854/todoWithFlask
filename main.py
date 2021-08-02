from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(200), nullable=False)
    def __repr__(self) :
        return "{} is the title and {} is the description".format(self.title,self.description)

@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo(title=title ,description=description)
        db.session.add(todo)
        db.session.commit()
    alltodos=Todo.query.all()
    return render_template('index.html',todos=alltodos)


@app.route("/delete/<int:sno>")
def delete(sno):
    deletetodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>",methods=['PATCH','POST','GET'])
def main_route(sno):
    if request.method == 'POST':
        updatetodo = Todo.query.filter_by(sno=sno).first()
        title = request.form['title']
        description = request.form['description']
        updatetodo.title = title
        updatetodo.description = description
        db.session.commit()
        return redirect("/")
    else:
        updatetodo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', updatetodo=updatetodo)

# @app.route("/updatetodo/<int:sno>",methods=['POST'])
# def update_todo(sno):
#     if request.method == 'POST':
#         updatetodo = Todo.query.filter_by(sno=sno).first()
#         title = request.form['title']
#         description = request.form['description']
#         updatetodo.title=title
#         updatetodo.description=description
#         db.session.commit()
#         return redirect("/")
#     updatetodo = Todo.query.filter_by(sno=sno).first()
#     return render_template('update.html', updatetodo=updatetodo)

if __name__ == "__main__":
    app.run(debug=False)