from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id}>'

@app.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handleMessage(data):
    print(f"Message from {data['username']}: {data['msg']}")
    message = Message(username=data['username'], text=data['msg'])
    db.session.add(message)
    db.session.commit()
    send({'username': data['username'], 'msg': data['msg']}, broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = 5000  
    print(f" Адрес://127.0.0.1:{port}/")
    socketio.run(app, port=port)
