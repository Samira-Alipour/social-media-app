from flask import render_template, url_for, redirect, flash, request, Blueprint, abort
from mapapp import db
from mapapp.posts.forms import PostForm
from mapapp.models import Post
from flask_login import current_user, login_required



posts = Blueprint('posts', __name__)

@login_required
@posts.route("/post", methods=['GET', 'POST'])
def post():
	form=PostForm()
	return render_template('post.html', title='Post Comment', form=form)



@login_required
@posts.route("/update_post/<int:post_id>", methods=['GET', 'POST'])
def update_post(post_id):
	form=PostForm()
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	if form.validate_on_submit():
		flash('post Updated')
		post.content = form.content.data
		post.title = form.title.data
		db.session.commit()
		return redirect(url_for('main.home'))
	elif request.method =='GET':
		form.content.data = post.content
		form.title.data = post.title
	return render_template('update_post.html', title='Update_Post', form=form)



@login_required
@posts.route("/delete_post/<int:post_id>")
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for("main.home"))

