from flask import Blueprint, request, g, jsonify
from .models import Idea, IdeaVotes
from app import basicauth

idea_bp = Blueprint('idea_bp', __name__, url_prefix='/ideas')


@idea_bp.route('/add', methods=('POST', 'GET'))
@basicauth.login_required
def add():
    title = request.form['title']
    content = request.form['content']
    try:
        Idea.create(
            title=title,
            content=content,
            user=g.user.user_id
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@idea_bp.route('/vote', methods=('POST'))
@basicauth.login_required
def vote():
    if IdeaVotes.select().where((IdeaVotes.user == g.user) & (IdeaVotes.idea == request.form['idea'])).exists():
        return jsonify({'success': False, 'message': 'You have already voted'})
    idea = Idea.get(Idea.id == request.form['idea'])
    increment = 1 if request.form['vote'] else -1
    idea.votes += increment
    idea.save()
    IdeaVotes.create(
        user=g.user,
        idea=idea
    )
    return jsonify({'success': True})


@idea_bp.route('/next')
@basicauth.login_required
def next():
    voted_on = [iv.id for iv in IdeaVotes.select().where(IdeaVotes.user == g.user)]
    idea = Idea.select().where(Idea.id.not_in(voted_on)).limit(1)
    x = None
    for i in idea:
        x = i
    if x is None:
        return jsonify({'success': False, 'message': 'No ideas left! :('})
    return jsonify({'success': True, 'idea': x})


@idea_bp.route('/top')
@basicauth.login_required
def top():
    ideas = Idea.select().order_by(Idea.votes.desc()).limit(10)
    data = []
    for idea in ideas:
        data.append(idea)
    return jsonify(data)