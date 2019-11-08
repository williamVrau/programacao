from app import app, login
from flask import render_template, redirect, url_for
from app.forms import CadastrarNotaForm, CadastrarUsuarioForm, LogarUsuarioForm, AtualizarUsuarioForm
from app import db, login
from app.models import NotaModel, UserModel
from flask_login import logout_user, login_required, login_user, current_user
from app import config
from werkzeug.security import generate_password_hash, check_password_hash
import os

def Nome_foto(nome_arquivo,email):
    extensao = nome_arquivo.split(".")
    extensao = "." + extensao[-1]
    nome_da_foto = email + extensao
    nome_da_foto = nome_da_foto.replace("@", "_arroba_")
    return nome_da_foto

@app.route("/editar_perfil",methods=['post','get'])
@login_required
def editar_perfil():
    form = AtualizarUsuarioForm()
    if form.validate_on_submit():
        usuario = UserModel.query.filter_by(email = current_user.email).first()
        usuario.nome = form.nome.data
        usuario.data_nascimento = form.data_nascimento.data
        
        if type(form.foto.data) != type(""):
            nome_da_foto = Nome_foto(form.foto.data.filename,current_user.email)
            nome_da_foto = nome_da_foto.replace(".jpeg","")
            nome_da_foto = nome_da_foto.replace(".jpg","") 
            nome_da_foto = nome_da_foto.replace(".png","")
        path = app.config['UPLOAD_FOLDER']
        files = []
        # r = root , d = diretorios, f = files
        for r, d , f in os.walk(path):
            for file in f:
                if nome_da_foto in file:
                    files.append(os.path.join(r, file))
        for f in files:
            for i in range(len(files)):
                os.remove(files[i])
        if type(form.foto.data) != type(""):
            nome_da_foto = Nome_foto(form.foto.data.filename, current_user.email)
            form.foto.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_da_foto))
            usuario.caminho_da_foto = "images/" + nome_da_foto
        usuario.senha_hash= generate_password_hash(form.senha.data)    
        db.session.merge(usuario)
        db.session.commit()
    return render_template("editar_perfil.html",form=form)

@app.route("/")
@app.route("/index",methods=['post','get'])
def executar_index():
    return render_template("index.html",title="Index")

@app.route("/remover_usuario",methods=['post','get'])
@login_required
def remover_usuario():
    db.session.delete(current_user)
    db.session.commit()
    return redirect("/index")

@app.route("/cadastro", methods=['get', 'post'])
def cadastrar_usuario():
    form = CadastrarUsuarioForm()
    if form.validate_on_submit():
        if form.foto.data:
            nome_da_foto = Nome_foto(form.foto.data.filename,form.email.data)
            form.foto.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_da_foto))
            usuario_cadastrado = UserModel(form.email.data,form.nome.data,form.data_nascimento.data,"images/" + nome_da_foto,form.senha.data)
        else:
            usuario_cadastrado = UserModel(form.email.data,form.nome.data,form.data_nascimento.data,"",form.senha.data)
        
        db.session.add(usuario_cadastrado)
        db.session.commit()
        login_user(usuario_cadastrado)
        return redirect("/perfil")
    return render_template('cadastro_usuario.html', form=form)

@app.route('/logar', methods=['get', 'post'])
def logar_usuario():
    form = LogarUsuarioForm()
    if form.validate_on_submit():
        print("teste")
        usuario = UserModel.query.filter_by(email=form.email.data).first()
        if usuario is not None:
            if usuario.verificar_senha(form.senha.data):
                login_user(usuario)
                return redirect("/perfil")
    else:
        print(form.email)
    return render_template("logar.html", form=form)

@app.route("/jogo", methods=['get', 'post'])
def jogo():
    jogo = request.args.get("jogo")
    nota_usuario = NotaModel.query.filter_by(usuario_id=current_user.email, nome_jogo=jogo)
    form = CadastrarNotaForm()
    if nota_usuario is None:    
        if form.validate_on_submit():
            db.session.add(NotaModel(form.nota.data,jogo))
            db.session.commit()
    else:
        if form.validate_on_submit():
            nota_usuario.comentar(form.comentario.data)
            db.session.merge(nota_usuario)
            db.session.commit()
    return(render_template(jogo+".html", form=form, nota_usuario=nota_usuario))




@app.route("/GTA_San_Andreas",methods=['get', 'post'])
@login_required
def GTA_San_andreas():
    nota_usuario = NotaModel.query.filter_by(usuario_id=current_user.email,nome_jogo="GTA_San_Andreas")
    form = CadastrarNotaForm()
    if nota_usuario is None:    
        if form.validate_on_submit():
            db.session.add(NotaModel(form.nota.data,"GTA_San_Andreas"))
            db.session.commit()
    else:
        if form.validate_on_submit():
            nota_usuario.comentar(form.comentario.data)
            db.session.merge(nota_usuario)
            db.session.commit()
    return(render_template("GTA_San_Andreas.html", form=form, nota_usuario=nota_usuario))



@app.route('/perfil', methods=['get','post'])
@login_required
def ver_perfil():
    return render_template("perfil.html")


@app.route('/logout',methods=['get','post'])
@login_required
def deslogar():
    logout_user()
    return redirect("/index")


@login.user_loader
def load_user(email):
    return UserModel.query.filter_by(email=email).first()