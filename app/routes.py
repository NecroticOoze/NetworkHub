from app import app,db,bcrypt
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, UploadedFile
from app.forms import LoginForm, RegisterForm, UploadFileForm
from uuid import uuid4
import os


@app.route('/')
def home():
    return render_template('home.html', active='home')

@app.route('/register-new-user', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('register.html', form=form,active='register')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', active='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You've successfully been logged out.","success")
    return redirect(url_for('home'))

def save_file(file):
    filename, f_ext = os.path.splitext(file.filename)
    random_uuid = str(uuid4())
    new_filename = random_uuid + f_ext
    file_path = os.path.join(app.root_path, 'static/uploads', new_filename)
    file.save(file_path)
    return (f"{filename}{f_ext}", f"{random_uuid}{f_ext}")

@app.route('/upload-file', methods=['GET','POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.is_submitted():
        # print(form.uploaded_file.data)
        if form.path.data == '':
            name_tuple = save_file(form.uploaded_file.data)
            file_obj = UploadedFile(path='/static/uploads/',drive='app.root_path',
                filename=name_tuple[0],uuid_name=name_tuple[1])
            db.session.add(file_obj)
            db.session.commit()
            
            flash('File has been uploaded successfully.','success')
            return redirect(url_for('view_files'))
        # file_object = UploadedFile(path=)
    return render_template('file_uploads.html', form=form, active='upload')

@login_required
@app.route('/view-files')
def view_files():
    files = UploadedFile.query.all()
    return render_template('view_files.html', files=files, active='view')