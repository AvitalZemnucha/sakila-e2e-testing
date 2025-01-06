from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

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
    films = db.relationship('Film', secondary='film_actor', back_populates='actors')


class Film(db.Model):
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey('language.language_id'), nullable=False)
    original_language_id = db.Column(db.Integer, db.ForeignKey('language.language_id'))
    rental_duration = db.Column(db.Integer, default=3)
    rental_rate = db.Column(db.Numeric(4, 2), default=4.99)
    length = db.Column(db.Integer)
    replacement_cost = db.Column(db.Numeric(5, 2), default=19.99)
    rating = db.Column(db.String(10))
    special_features = db.Column(db.String(255))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    language = db.relationship('Language', foreign_keys=[language_id])
    original_language = db.relationship('Language', foreign_keys=[original_language_id])
    actors = db.relationship('Actor', secondary='film_actor', back_populates='films')


class Language(db.Model):
    __tablename__ = 'language'
    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)


class FilmActor(db.Model):
    __tablename__ = 'film_actor'
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), primary_key=True)


@app.route('/')
def index():
    actors = Actor.query.all()
    return render_template('index.html', actors=actors)


@app.route('/top_rated_films')
def top_rated_films():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    films = Film.query.filter(Film.rating > 4.0).order_by(Film.rating.desc()).paginate(page=page, per_page=per_page,
                                                                                       error_out=False)

    return render_template('top_rated_films.html', films=films)


@app.route('/api/films/top_rated', methods=['GET'])
def api_top_rated_films():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    films = Film.query.order_by(Film.rating.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'films': [{
            'id': film.film_id,
            'title': film.title,
            'release_year': film.release_year,
            'rating': film.rating,
            'actors': [{'id': actor.actor_id, 'name': f"{actor.first_name} {actor.last_name}"} for actor in film.actors]
        } for film in films.items],
        'total': films.total,
        'pages': films.pages,
        'current_page': films.page
    })


@app.route('/api/films', methods=['POST'])
def api_create_film():
    data = request.json
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    allowed_features = ['Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes']
    special_features = data.get('special_features', '')
    if special_features:
        features = [f.strip() for f in special_features.split(',') if f.strip() in allowed_features]
        special_features = ','.join(features)
    new_film = Film(
        title=data['title'],
        description=data.get('description', ''),
        release_year=data.get('release_year'),
        language_id=data.get('language_id', 1),  # Default to 1 if not provided
        rental_duration=data.get('rental_duration', 3),
        rental_rate=data.get('rental_rate', 4.99),
        length=data.get('length'),
        replacement_cost=data.get('replacement_cost', 19.99),
        rating=data.get('rating', 'G'),
        special_features=data.get('special_features', '')
    )
    if 'actor_ids' in data:
        actors = Actor.query.filter(Actor.actor_id.in_(data['actor_ids'])).all()
        new_film.actors = actors
    db.session.add(new_film)
    db.session.commit()
    return jsonify({
        'id': new_film.film_id,
        'title': new_film.title,
        'release_year': new_film.release_year,
        'rating': new_film.rating
    }), 201


@app.route('/api/films/<int:film_id>', methods=['PUT'])
def api_update_film(film_id):
    film = Film.query.get_or_404(film_id)
    data = request.json
    film.title = data.get('title', film.title)
    film.release_year = data.get('release_year', film.release_year)
    film.rating = data.get('rating', film.rating)
    if 'actor_ids' in data:
        actors = Actor.query.filter(Actor.actor_id.in_(data['actor_ids'])).all()
        film.actors = actors
    db.session.commit()
    return jsonify({
        'id': film.film_id,
        'title': film.title,
        'release_year': film.release_year,
        'rating': film.rating
    })


@app.route('/api/films/<int:film_id>', methods=['DELETE'])
def api_delete_film(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return '', 204


@app.route('/api/films/<int:film_id>', methods=['GET'])
def api_get_film(film_id):
    film = Film.query.get_or_404(film_id)
    return jsonify({
        'id': film.film_id,
        'title': film.title,
        'release_year': film.release_year,
        'rating': film.rating,
        'actors': [{'id': actor.actor_id, 'name': f"{actor.first_name} {actor.last_name}"} for actor in film.actors]
    })


@app.route('/api/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify([{'id': a.actor_id, 'first_name': a.first_name, 'last_name': a.last_name} for a in actors])


@app.route('/api/actors/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    return jsonify({
        'id': actor.actor_id,
        'first_name': actor.first_name,
        'last_name': actor.last_name,
        'last_update': actor.last_update.isoformat()
    })


@app.route('/api/actors', methods=['POST'])
def api_create_actor():
    data = request.json
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name are required'}), 400
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
