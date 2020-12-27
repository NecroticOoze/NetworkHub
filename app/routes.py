from app import app,db,bcrypt
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, UploadedFile
from app.forms import LoginForm, RegisterForm, UploadFileForm
from app.mount import list_media_devices, mount, is_mounted, unmount, get_device_name, get_media_path
from uuid import uuid4
import os

if not os.path.exists("app/static/uploads"):
    os.makedirs("app/static/uploads")

@app.before_request
def checkIfBruteForce():
    # print("checking")
    # print(request.full_path)
    if 'static/uploads' in request.full_path and not current_user.is_authenticated:
        return redirect(url_for('login', next=request.url))

@app.route('/')
def home():
    return render_template('home.html', active='home')

@app.route('/register-new-user', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.is_submitted():
        print(form.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('That username is taken. Please choose a different one.','danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,password=hashed_password,is_active=False)
            db.session.add(user)
            db.session.commit()
            flash('Account information submitted. Please wait for an admin to approve your account.','info')
            return redirect(url_for('login'))
    return render_template('register.html', form=form,active='register')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user.is_active == False:
            flash('Login Unsuccessful. Your account is not yet activated.', 'danger')
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', active='login', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You've successfully been logged out.","success")
    else:
        flash("You're currently not logged in.",'info')
    return redirect(url_for('home'))

def save_file(file, path='static/uploads', drive=app.root_path):
    filename, f_ext = os.path.splitext(file.filename)
    random_uuid = str(uuid4())
    new_filename = random_uuid + f_ext
    file_path = os.path.join(drive, path, new_filename)
    file.save(file_path)
    return (f"{filename}{f_ext}", f"{random_uuid}{f_ext}")

@login_required
@app.route('/upload-file', methods=['GET','POST'])
def upload_file():
    # os.listdir('/Volumes') lists drives on MacOS
    form = UploadFileForm()
    if form.is_submitted():
        # print(form.data)
        if form.path.data == '':
            name_tuple = save_file(file=form.uploaded_file.data)
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

@login_required
@app.route('/approve_user')
def approve_user():
    if current_user.role != 'admin':
        flash('You do not have rights to this section','danger')
        return redirect(url_for('home'))
    token = current_user.get_valid_token()
    users = User.query.all()
    return render_template('approve_user.html',active='approve_user',users=users,token=token)

@login_required
@app.route('/approve_user/edit_user',methods=['POST'])
def edit_user():
    if current_user.role != 'admin':
        return "Denied."
    else:
        user = current_user.verify_valid_token(request.form["token"])
        if user == None:
            return "Invalid Token. Please refresh page."
        elif len(User.query.filter_by(role='admin').all()) == 1 and request.form["role"] == "admin" and request.form["is_active"] == "false":
            return "You cannot disable the only admin account."
        try:
            updatedUser = User.query.filter_by(username=request.form["username"]).first()
            active = False if request.form["is_active"] == "false" else True 
            updatedUser.is_active = active
            db.session.commit()
            if active:
                return f"User '{request.form['username']}' is active."
            else:
                return f"User '{request.form['username']}' is not active."
        except(err):
            print(err)
            return "error"