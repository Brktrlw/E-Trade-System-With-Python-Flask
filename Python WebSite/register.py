from wtforms import Form,StringField,TextAreaField,PasswordField,validators

class RegisterForm(Form):
    customerName=StringField("Adınızı Giriniz",validators=[validators.Length(min=5)])
    customerUserName=StringField("Kullanıcı Adı Giriniz",validators=[validators.Length(min=5,max=30)])
    customerMail=StringField("E Postanızı Giriniz",validators=[validators.Length(min=5)])
    customerPassword=PasswordField("Parolanızı Giriniz",validators=[validators.DataRequired(message="Lütfen parola giriniz"),validators.Length(min=7)])
class LoginForm(Form):
    customerUserName=StringField("Kullanıcı Adınızı Giriniz")
    customerPassword=PasswordField("Şifrenizi giriniz")