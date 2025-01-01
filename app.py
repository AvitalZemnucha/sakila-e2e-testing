from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:avitalz@127.0.0.1/sakila'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Actor(db.Model):
    __tablename__ = 'actor'
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)


@app.route('/')
def index():
    actors = Actor.query.all()
    return render_template('index.html', actors=actors)


@app.route('/api/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([{'id': a.actor_id, 'first_name': a.first_name, 'last_name': a.last_name} for a in actors])


@app.route('/api/actors/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    actor = Actor.query.get_or_404(actor_id)  # Returns 404 if actor not found
    return jsonify({
        'id': actor.actor_id,
        'first_name': actor.first_name,
        'last_name': actor.last_name,
        'last_update': actor.last_update.isoformat()  # Format datetime for JSON
    })


@app.route('/api/actors', methods=['POST'])
def api_create_actor():
    data = request.json
    new_actor = Actor(
        first_name=data['first_name'],
        last_name=data['last_name'],
        last_update=datetime.now()
    )
    db.session.add(new_actor)
    db.session.commit()
    return jsonify(
        {'id': new_actor.actor_id, 'first_name': new_actor.first_name, 'last_name': new_actor.last_name}), 201


@app.route('/api/actors/<int:actor_id>', methods=['PUT'])
def api_update_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    data = request.json
    actor.first_name = data.get('first_name', actor.first_name)
    actor.last_name = data.get('last_name', actor.last_name)
    actor.last_update = datetime.now()
    db.session.commit()
    return jsonify({'id': actor.actor_id, 'first_name': actor.first_name, 'last_name': actor.last_name})


@app.route('/api/actors/<int:actor_id>', methods=['DELETE'])
def api_delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return '', 204


@app.route('/create', methods=['GET', 'POST'])
def create_actor():
    if request.method == 'POST':
        new_actor = Actor(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            last_update=datetime.now()
        )
        db.session.add(new_actor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:actor_id>', methods=['GET', 'POST'])
def edit_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    if request.method == 'POST':
        actor.first_name = request.form['first_name']
        actor.last_name = request.form['last_name']
        actor.last_update = datetime.now()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', actor=actor)


@app.route('/delete/<int:actor_id>', methods=['POST'])
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
