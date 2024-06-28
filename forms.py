from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo
from flask_wtf.file import FileField

class AddProduct(FlaskForm):
    name = StringField("Product name",validators=[DataRequired()])
    price = IntegerField("Product price",validators=[DataRequired()])
    image_url = StringField("Product image url")
    image = FileField("Upload image")
    text = StringField("Description")
    category_id = IntegerField("Ctategory id")
    
    submit = SubmitField("Submit")

class AddBlog(FlaskForm):
    name = StringField("Blog name",validators=[DataRequired()])
    image_url = StringField("Blog image url")
    image = FileField("Upload image")
    text = StringField("Blog description") 
    
    submit = SubmitField("Submit") 

class SignUp(FlaskForm):
    username = StringField("User",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Passsword",validators=[DataRequired()])
    confrim_password = PasswordField("Confrim Passsword",validators=[DataRequired(),EqualTo("password")])

    submit = SubmitField("Submit")  

class LogIn(FlaskForm):
    username = StringField("User",validators=[DataRequired()])
    password = PasswordField("Passsword",validators=[DataRequired()])

    submit = SubmitField("Submit") 