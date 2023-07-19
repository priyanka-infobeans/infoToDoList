# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from book_app import db
from book_app.models import User
from book_app.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from book_app.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        try:
            db.session.commit()
            flash('Thanks for registration!', 'success')
            return redirect(url_for('users.login'))
        except:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')

    return render_template('register.html', form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success!', 'success')

            next_url = request.args.get('next')

            if not next_url or not next_url.startswith('/'):
                next_url = url_for('core.index')

            return redirect(next_url)
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html', form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account (update UserForm)
@login_required
@users.route('/account')
def account():
    # Check if the user is logged in
    if 'user_id' in session:
        # Assuming you have a User model and the user details are available in the session
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        user = None

    return render_template('account.html', user=user)



















# user's list of Blog posts
