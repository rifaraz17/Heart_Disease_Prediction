from flask import render_template, url_for, flash, redirect,request,session
from Heart_Disease.predict_methods import predict_disease
from flask_login import login_user, current_user, logout_user

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.email}')"

class DoctorAdd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"DoctorAdd('{self.username}', '{self.email}')"

class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}')"
    
with app.app_context():
    db.create_all()

class DoctorLoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"placeholder": "Email address"})                    
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
	
class AdminLoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"placeholder": "Email address"})                    
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
    
    
class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Username"})
    email = StringField(validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email address"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        doctor =Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('This email is already registered.')
            
class AddDoctorForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(validators=[DataRequired(), Email()])                    
    submit = SubmitField('Add')
    def validate_email(self, email):
        doctor1 = DoctorAdd.query.filter_by(email=email.data).first()
        doctor2 = Doctor.query.filter_by(email=email.data).first()
        if doctor1:
            raise ValidationError('This email is already added.')
        if doctor2:
            raise ValidationError('This email is already registered.')
			
class ChangePassword(FlaskForm):                    
    current_password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Current Password"})
    new_password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "New Password"})
    submit = SubmitField('Change Password')

class DiseasePredict(FlaskForm):
    age=FloatField(validators=[DataRequired()])
    sex=SelectField(validators=[DataRequired()])
    cp =SelectField(validators=[DataRequired()])
    trestbps =FloatField(validators=[DataRequired()])
    chol =FloatField(validators=[DataRequired()])
    fbs=SelectField(validators=[DataRequired()])
    restecg=SelectField(validators=[DataRequired()])
    thalach=FloatField(validators=[DataRequired()])
    exang=SelectField(validators=[DataRequired()])
    oldpeak = FloatField(validators=[DataRequired()])
    slope = SelectField(validators=[DataRequired()])
    ca = SelectField(validators=[DataRequired()])
    thal = SelectField(validators=[DataRequired()])
    submit = SubmitField('Predict')

@app.route("/")
def home():
    if not Admin.query.all():
        pwd='Admin@HD'
        pswrd=bcrypt.generate_password_hash(pwd).decode('utf-8')
        user = Admin(email='admin@hd.com',password=pswrd)
        db.session.add(user)
        db.session.commit()
    return render_template('home.html', title='Home')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@hd.com' and form.password.data == 'Admin@HD':
        admin=Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            flash('hello Admin... \n You have been logged in!', 'success')
            return redirect(url_for('adminhome'))
        else:
            flash('Login Unsuccessful. Please check Email address and password', 'danger')
    return render_template('adminlogin.html', title='Login', form=form)

@app.route("/adminhome")
def adminhome():
    return render_template('adminhome.html', title='Home')

@app.route("/adminchangepassword",methods=['GET','POST'])
def adminchangepassword():
    form=ChangePassword()
    if form.validate_on_submit():
        record=Admin.query.all()[0]
        if bcrypt.check_password_hash(record.password,form.current_password.data):
            record.password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully..!', 'success')
            return redirect(url_for('adminhome'))
        else:
            flash('Please enter correct current password', 'danger')
    return render_template('adminchangepassword.html', title='Change Password',form=form)

@app.route("/adddoctor",methods=['GET','POST'])
def adddoctor():
    form=AddDoctorForm()
    if form.validate_on_submit():
        doctor = DoctorAdd(username=form.name.data, email=form.email.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully..!', 'success')
        return redirect(url_for('adddoctor'))
    return render_template('adddoctor.html', title="Doctor",form=form)

@app.route("/viewdoctor")
def viewdeletedoctor():
    result=Doctor.query.all()
    return render_template('viewdoctor.html', title='Doctor',result=result)

@app.route("/deletedoctor/<int:id>")
def deletedoctor(id):
    entry=Doctor.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Deleted successfully...!",'success')
    return redirect(url_for('viewdeletedoctor'))

@app.route("/adminlogout")
def adminlogout():
    return redirect(url_for('home'))


@app.route("/doctorlogin", methods=['GET', 'POST'])
def doctorlogin():
    if current_user.is_authenticated:
        return redirect(url_for('doctorhome'))
    form = DoctorLoginForm()
    if form.validate_on_submit():
        doctor_add=DoctorAdd.query.filter_by(email=form.email.data).first()
        doctor=Doctor.query.filter_by(email=form.email.data).first()
        if not doctor_add and not doctor:
            flash('You are not a Doctor, please contact admin.','info')
        elif doctor_add:
            flash('You are not registered.','info')
            return redirect(url_for('register'))
        elif doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            flash('Logged in successfully..!','success')
            return redirect(url_for('doctorhome'))
        else:
            flash('Please check your password..','danger')
            return redirect(url_for('doctorlogin'))
    return render_template('doctorlogin.html',title='Login',form=form)


@app.route("/doctorhome")
def doctorhome():
    return render_template('doctorhome.html', title='Home')

@app.route("/changepassword",methods=['GET','POST'])
def changepassword():
    form=ChangePassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password,form.current_password.data):
            current_user.password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully..!', 'success')
            return redirect(url_for('doctorhome'))
        else:
            flash('Please enter correct current password', 'danger')
    return render_template('changepassword.html', title='Change Password',form=form)

@app.route("/doctorlogout")
def doctorlogout():
    logout_user()
    session.pop('running',None)
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        doctor_add=DoctorAdd.query.filter_by(email=form.email.data,username=form.username.data).first()
        if not doctor_add:
            flash('You are not a doctor, please contact admin.','info')
            return redirect(url_for('register'))
        else:
            db.session.delete(doctor_add)
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            doctor = Doctor(username=form.username.data, email=form.email.data,password=hashed_password)
            db.session.add(doctor)
            db.session.commit()
            flash('Registration successfull..', 'success')
            return redirect(url_for('doctorlogin'))
    return render_template('register.html', title='Registration Form', form=form)

@app.route("/diseasepredict",methods=['GET','POST'])
def diseasepredict():
    form= DiseasePredict()
    if request.method=='POST':

        age=int(request.form['age'])
        sex_=request.form.get('sex')
        cp_ =request.form.get('cp')
        trestbps =int(request.form['trestbps'])
        chol =int(request.form['chol'])
        fbs_=request.form.get('fbs')
        restecg_=request.form.get('restecg')
        thalach=int(request.form['thalach'])
        exang_=request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope_ = request.form.get('slope')
        ca_ = request.form.get('ca')
        thal_ = request.form.get('thal')

        prediction = predict_disease(age,sex_,cp_,trestbps,chol,fbs_,restecg_,thalach,exang_,oldpeak,slope_,ca_,thal_)
        return render_template('diseaseresult.html', recommendation=prediction, title='Disease Prediction')
    return render_template('doctorhome.html', title='Home',form=form)

if __name__ == '__main__':
    app.run()