from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Programs/Apps/Python/gamegrove.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='user', lazy=True)
    favorites = db.relationship('Game', secondary='favorites', backref='favorited_by')
    game_lists = db.relationship('GameList', backref='user', lazy=True)
    playtime_records = db.relationship('PlaytimeRecord', backref='user', lazy=True)
    achievements = db.relationship('Achievement', secondary='user_achievements', backref='users')
    friends = db.relationship(
        'User', 
        secondary='friendship',
        primaryjoin='User.id==Friendship.user_id',
        secondaryjoin='User.id==Friendship.friend_id',
        backref='friend_of'
    )
    activities = db.relationship('ActivityFeed', backref='user', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(200))
    reviews = db.relationship('Review', backref='game', lazy=True)
    achievements = db.relationship('Achievement', backref='game', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

class GameList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20))  # playing, completed, wishlist
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    games = db.relationship('Game', secondary='list_games')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PlaytimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    minutes_played = db.Column(db.Integer, default=0)
    last_played = db.Column(db.DateTime)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(200))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20))  # pending, accepted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Association Tables
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.UniqueConstraint('user_id', 'game_id', name='unique_user_game')
)

list_games = db.Table('list_games',
    db.Column('list_id', db.Integer, db.ForeignKey('game_list.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

user_achievements = db.Table('user_achievements',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    genre = request.args.get('genre')
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'rating')

    query = Game.query

    if genre:
        query = query.filter(Game.genre == genre)
    if search:
        query = query.filter(Game.title.ilike(f'%{search}%'))

    if sort == 'rating':
        query = query.order_by(Game.rating.desc())
    elif sort == 'title':
        query = query.order_by(Game.title)
    elif sort == 'release':
        query = query.order_by(Game.release_date.desc())

    games = query.all()
    genres = db.session.query(Game.genre).distinct().all()
    return render_template('home.html', games=games, genres=genres, current_genre=genre, search=search, sort=sort)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    reviews = Review.query.filter_by(game_id=game_id).order_by(Review.created_at.desc()).all()
    achievements = Achievement.query.filter_by(game_id=game_id).all()
    return render_template('game_detail.html', game=game, reviews=reviews, achievements=achievements)

@app.route('/list/<int:list_id>')
@login_required
def view_list(list_id):
    game_list = GameList.query.get_or_404(list_id)
    
    # Calculate average rating using existing game.rating attribute
    ratings = [game.rating for game in game_list.games if game.rating]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return render_template('game_list.html', 
                         list=game_list,
                         average_rating=average_rating)

@app.route('/add_to_list/<int:game_id>/<string:list_type>', methods=['POST'])
@login_required
def add_to_list(game_id, list_type):
    game = Game.query.get_or_404(game_id)
    game_list = GameList.query.filter_by(user_id=current_user.id, type=list_type).first()
    
    if not game_list:
        game_list = GameList(name=f"My {list_type.capitalize()}", type=list_type, user_id=current_user.id)
        db.session.add(game_list)
    
    if game not in game_list.games:
        game_list.games.append(game)
        
        activity = ActivityFeed(
            user_id=current_user.id,
            activity_type=f"added_to_{list_type}",
            content=f"Added {game.title} to {list_type}"
        )
        db.session.add(activity)
        db.session.commit()
        
    return jsonify({'message': f'Added to {list_type}'})

@app.route('/update_playtime/<int:game_id>', methods=['POST'])
@login_required
def update_playtime(game_id):
    minutes = request.json.get('minutes', 0)
    record = PlaytimeRecord.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    
    if not record:
        record = PlaytimeRecord(user_id=current_user.id, game_id=game_id)
        db.session.add(record)
    
    record.minutes_played += minutes
    record.last_played = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'total_playtime': record.minutes_played})

@app.route('/friends')
@login_required
def friends():
    pending_requests = Friendship.query.filter_by(friend_id=current_user.id, status='pending').all()
    return render_template('friends.html', user=current_user, pending_requests=pending_requests)

@app.route('/add_friend/<int:friend_id>', methods=['POST'])
@login_required
def add_friend(friend_id):
    if friend_id == current_user.id:
        return jsonify({'error': 'Cannot add yourself as friend'})
    
    friendship = Friendship(user_id=current_user.id, friend_id=friend_id, status='pending')
    db.session.add(friendship)
    db.session.commit()
    
    return jsonify({'message': 'Friend request sent'})

@app.route('/accept_friend/<int:friendship_id>', methods=['POST'])
@login_required
def accept_friend(friendship_id):
    friendship = Friendship.query.get_or_404(friendship_id)
    if friendship.friend_id != current_user.id:
        return jsonify({'error': 'Unauthorized'})
    
    friendship.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Friend request accepted'})

@app.route('/activity')
@login_required
def activity_feed():
    activities = ActivityFeed.query.filter_by(user_id=current_user.id).order_by(ActivityFeed.created_at.desc()).all()
    return render_template('activity_feed.html', activities=activities)

@app.route('/profile')
@login_required
def profile():
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    game_lists = GameList.query.filter_by(user_id=current_user.id).all()
    playtime_records = PlaytimeRecord.query.filter_by(user_id=current_user.id).all()
    activities = ActivityFeed.query.filter_by(user_id=current_user.id).order_by(ActivityFeed.created_at.desc()).limit(10).all()
    return render_template('profile.html', 
                         user=current_user, 
                         reviews=user_reviews, 
                         game_lists=game_lists,
                         playtime_records=playtime_records,
                         activities=activities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=request.form.get('username')).first():
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'))
        )
        db.session.add(user)
        db.session.commit()
        
        # Create default lists for new user
        default_lists = ['Playing', 'Completed', 'Wishlist']
        for list_type in default_lists:
            game_list = GameList(
                name=f"My {list_type}",
                type=list_type.lower(),
                user_id=user.id
            )
            db.session.add(game_list)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/add_review/<int:game_id>', methods=['POST'])
@login_required
def add_review(game_id):
    content = request.form.get('content')
    rating = request.form.get('rating')
    
    if not content or not rating:
        flash('Review content and rating are required', 'error')
        return redirect(url_for('game_detail', game_id=game_id))
    
    review = Review(
        content=content,
        rating=int(rating),
        user_id=current_user.id,
        game_id=game_id
    )
    db.session.add(review)
    
    # Create activity feed entry
    activity = ActivityFeed(
        user_id=current_user.id,
        activity_type='new_review',
        content=f"Reviewed {review.game.title}"
    )
    db.session.add(activity)
    db.session.commit()
    
    # Update game rating
    game = Game.query.get(game_id)
    reviews = Review.query.filter_by(game_id=game_id).all()
    game.rating = sum(r.rating for r in reviews) / len(reviews)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/toggle_favorite/<int:game_id>', methods=['POST'])
@login_required
def toggle_favorite(game_id):
    game = Game.query.get_or_404(game_id)
    if game in current_user.favorites:
        current_user.favorites.remove(game)
        message = 'Game removed from favorites'
        activity_type = 'remove_favorite'
    else:
        current_user.favorites.append(game)
        message = 'Game added to favorites'
        activity_type = 'add_favorite'
    
    activity = ActivityFeed(
        user_id=current_user.id,
        activity_type=activity_type,
        content=f"{message}: {game.title}"
    )
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'message': message})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    games = Game.query.filter(
        (Game.title.ilike(f'%{query}%')) |
        (Game.description.ilike(f'%{query}%')) |
        (Game.genre.ilike(f'%{query}%'))
    ).all()
    return render_template('search_results.html', games=games, query=query)

@app.route('/achievements/<int:game_id>')
@login_required
def achievements(game_id):
    game = Game.query.get_or_404(game_id)
    achievements = Achievement.query.filter_by(game_id=game_id).all()
    return render_template('achievements.html', game=game, achievements=achievements)

@app.route('/unlock_achievement/<int:achievement_id>', methods=['POST'])
@login_required
def unlock_achievement(achievement_id):
    achievement = Achievement.query.get_or_404(achievement_id)
    if achievement not in current_user.achievements:
        current_user.achievements.append(achievement)
        
        activity = ActivityFeed(
            user_id=current_user.id,
            activity_type='achievement_unlocked',
            content=f"Unlocked achievement: {achievement.name} in {achievement.game.title}"
        )
        db.session.add(activity)
        db.session.commit()
        
    return jsonify({'message': 'Achievement unlocked!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
