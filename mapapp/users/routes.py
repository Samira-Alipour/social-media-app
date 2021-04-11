from flask import render_template, url_for, redirect, flash, request, Blueprint
from mapapp import db, bcrypt
from mapapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from mapapp.models import User
from flask_login import login_user, current_user, logout_user, login_required
from mapapp.users.utils import save_picture


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	else:

		form = RegistrationForm()
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(username=form.username.data, email=form.email.data, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			flash(f'Your account has been created successfully', 'success')
			return redirect(url_for('users.login'))
	
	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('The user logged in successfully')
			return redirect(url_for('main.home'))
	return render_template('login.html', title='Log In', form=form)


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@login_required
@users.route("/account", methods=['GET', 'POST'])
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		if form.picture.data:
			current_user.image_file = save_picture(form.picture.data)
		db.session.commit()
		flash('User account updated successfully')
		return redirect(url_for('main.home'))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='images/' + current_user.image_file)
	flash(image_file)
	return render_template('account.html', title='account', form=form, image_file=image_file)
