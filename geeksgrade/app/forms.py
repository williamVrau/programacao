from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField ,TextField, TextAreaField, SubmitField, FileField, PasswordField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed, FileRequired


class CadastrarUsuarioForm(FlaskForm):
    email = StringField("E-mail", validators=[InputRequired(message="Campo obrigatório."),
                                              Email(message="Insira um endereço de e-mail válido, usando '@'.")])
    nome = StringField("Nome do usuário", validators=[InputRequired(message="Campo obrigatório.")])
    data_nascimento = DateField("Data de nascimento", validators=[InputRequired(message="Campo obrigatório.")])
    foto = FileField("Escolher foto de perfil", validators=[FileAllowed(['jpg', 'png', 'jpeg'],message='Somente imagens jpg e png!')])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    senha_verificadora = PasswordField("Digite novamente sua senha",validators=[InputRequired(message="Campo obrigatório"),
                                                                                EqualTo('senha')])
    submit = SubmitField("Registrar")

class LogarUsuarioForm(FlaskForm):
    email = StringField("Email do usuário", validators=[InputRequired(message="Campo obrigatório."),Email(message="Insira um endereço de e-mail válido, usando '@'.")])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    submit = SubmitField("Logar")

class AtualizarUsuarioForm(FlaskForm):
    nome = StringField("Nome do usuário", validators=[InputRequired(message="Campo obrigatório.")])
    data_nascimento = DateField("Data de nascimento", validators=[InputRequired(message="Campo obrigatório.")])
    foto = FileField("Escolher foto de perfil", validators=[FileAllowed(['jpg', 'png', 'jpeg'],message='Somente imagens jpg e png!')])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    senha_verificadora = PasswordField("Digite novamente sua senha",validators=[InputRequired(message="Campo obrigatório"),
                                                                                EqualTo('senha')])
    submit = SubmitField("Salvar alteraçao")

class CadastrarNotaForm(FlaskForm):
    nota = SelectField("Nota", choices=[('0',0),('1',1),('2',4),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9),('10',10)], validators=InputRequired(message='Campo obrigatório.'))
    comentario = TextAreaField("Comentário")
    submit = SubmitField("Postar")

