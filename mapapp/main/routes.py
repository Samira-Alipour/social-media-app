from flask import render_template, url_for, redirect, flash, request, Blueprint
from mapapp import db
from mapapp.posts.forms import PostForm
from mapapp.models import Post
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
	form = PostForm()
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Comment was added successfully', 'success')
		return redirect(url_for('main.home'))
	return render_template('home.html', title='Home', form=form, posts=posts)

