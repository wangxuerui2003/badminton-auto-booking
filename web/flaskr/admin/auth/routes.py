from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from flaskr.admin import admin_bp
from flaskr.extensions import login_manager
from flaskr.models.admin import Admin
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flaskr.models.admin import Admin


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')


@login_manager.user_loader
def load_admin(admin_user_id):
    return Admin.query.get(admin_user_id)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        admin: Admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Login successful', 'success')
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('admin.index')
            return redirect(next)
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html', form=form)

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))