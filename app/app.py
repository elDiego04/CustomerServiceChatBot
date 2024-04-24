from flask import Flask, render_template, url_for
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
"""app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) """

""" class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id  """

@app.route('/')
def index():
    # Crea las tablas de la base de datos cuando se acceda a la página de inicio
    return render_template('index.html')

@app.route('/carrito')
def carrito():
    # Crea las tablas de la base de datos cuando se acceda a la página de inicio
    return render_template('carrito.html')

if __name__ == "__main__":
    app.run(debug=True)