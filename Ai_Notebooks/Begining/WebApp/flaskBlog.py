from flask import Flask, render_template, url_for, flash,redirect
from form import RegistrationForm,LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '4ad79017536d1d53e47d58130dcbd6be'
posts = [
    {
        'author': 'Corey schafer',
        'title': 'Blog post 1',
        'content': 'First post content',
        'data_posted': ' April 17 -  1996'
    },
    {
        'author': 'Pedro ospina',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'data_posted': ' April 17 -  2019'
    },
    {
        'author': 'Test athor ',
        'title': 'Blog post 3',
        'content': 'thrid post content',
        'data_posted': ' April 17 -  1996'
    },
    {
        'author': 'schafer',
        'title': 'test post 4',
        'content': 'fourth post content',
        'data_posted': ' April 17 -  1996'
    }
]

@app.route("/")
@app.route("/home") #bind two or more rotues to the same method.
def home():
    return render_template("home.html", posts=posts)

@app.route("/about") # To create a endpoint
def about():
    return render_template("about.html", title="about") # method to render an html 

@app.route("/register", methods=['GET','POST']) 
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.userName.data}!',category="success")
        return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form)

@app.route("/login", methods=['GET','POST'])  
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login', form=form)

if( __name__ == "__main__"): # to execute the web server 
    app.run(debug=True)