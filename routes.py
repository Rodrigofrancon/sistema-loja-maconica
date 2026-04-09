from flask import Blueprint, render_template, request, redirect, current_app
from models import db, Pessoa, DadosMaconicos, Familiar, Contato, Endereco, Candidato, DocumentoArquivo 
from werkzeug.utils import secure_filename
import os
from datetime import datetime

main = Blueprint('main', __name__)

# =========================
# HOME
# =========================
@main.route('/')
def home():
    return render_template('index.html')


# =========================
# LISTA MAÇONS
# =========================
@main.route('/macons')
def macons():
    pessoas = Pessoa.query.all()
    return render_template('macons.html', pessoas=pessoas)


# =========================
# CADASTRO MAÇOM
# =========================
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':

        pessoa = Pessoa(
            nome=request.form['nome'],
            data_nascimento=request.form.get('data_nascimento'),
            naturalidade=request.form.get('naturalidade'),
            nacionalidade=request.form.get('nacionalidade'),
            estado_civil=request.form.get('estado_civil'),
            sexo=request.form.get('sexo'),
            nome_pai=request.form.get('nome_pai'),
            nome_mae=request.form.get('nome_mae'),
            escolaridade=request.form.get('escolaridade'),
            cim=request.form.get('cim'),
            conjuge=request.form.get('conjuge'),
            data_casamento=request.form.get('data_casamento'),
        )

        db.session.add(pessoa)
        db.session.commit()

        # CONTATO
        if request.form.get('telefone') or request.form.get('celular'):
            db.session.add(Contato(
                pessoa_id=pessoa.id,
                telefone=request.form.get('telefone'),
                celular=request.form.get('celular'),
                email=request.form.get('email')
            ))

        # DADOS MAÇÔNICOS
        db.session.add(DadosMaconicos(
            pessoa_id=pessoa.id,
            situacao=request.form.get('situacao'),
            forma_admissao=request.form.get('forma'),
            data_admissao=request.form.get('data_admissao')
        ))

        # ENDEREÇO
        if request.form.get('cep'):
            db.session.add(Endereco(
                pessoa_id=pessoa.id,
                cep=request.form.get('cep'),
                rua=request.form.get('rua'),
                numero=request.form.get('numero'),
                bairro=request.form.get('bairro'),
                cidade=request.form.get('cidade'),
                estado=request.form.get('estado'),
                pais=request.form.get('pais')
            ))

        # 📄 DOCUMENTO (UPLOAD)
        file = request.files.get('arquivo')

        if file and file.filename:
            filename = secure_filename(file.filename)

            pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'macons')
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, filename)
            file.save(caminho)

            data_doc = request.form.get('doc_data')

            db.session.add(DocumentoArquivo(
                pessoa_id=pessoa.id,
                nome=request.form.get('doc_nome'),
                data_documento=datetime.strptime(data_doc, '%Y-%m-%d') if data_doc else None,
                nome_arquivo=filename,
                caminho=caminho
            ))

        db.session.commit()
        return redirect('/macons')

    return render_template('cadastro.html')


# =========================
# EDITAR MAÇOM
# =========================
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':
        pessoa.nome = request.form.get('nome')
        pessoa.cim = request.form.get('cim')
        pessoa.data_nascimento = request.form.get('data_nascimento')

        db.session.commit()
        return redirect('/macons')

    return render_template('editar.html', pessoa=pessoa)


# =========================
# EXCLUIR MAÇOM
# =========================
@main.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)

    DadosMaconicos.query.filter_by(pessoa_id=id).delete()
    Contato.query.filter_by(pessoa_id=id).delete()
    Endereco.query.filter_by(pessoa_id=id).delete()
    DocumentoArquivo.query.filter_by(pessoa_id=id).delete()

    db.session.delete(pessoa)
    db.session.commit()

    return redirect('/macons')


# =========================
# CADASTRO CANDIDATO
# =========================
@main.route('/candidato', methods=['GET', 'POST'])
def candidato():
    if request.method == 'POST':

        candidato = Candidato(
            nome=request.form.get('nome'),
            cpf=request.form.get('cpf'),
            rg=request.form.get('rg'),
            titulo=request.form.get('titulo'),
            data_candidatura=request.form.get('data_candidatura'),
            situacao=request.form.get('situacao')
        )

        db.session.add(candidato)
        db.session.commit()

        # CONTATO
        if request.form.get('telefone'):
            db.session.add(Contato(
                candidato_id=candidato.id,
                telefone=request.form.get('telefone'),
                celular=request.form.get('celular'),
                email=request.form.get('email')
            ))

        # ENDEREÇO
        if request.form.get('cep'):
            db.session.add(Endereco(
                candidato_id=candidato.id,
                cep=request.form.get('cep'),
                rua=request.form.get('rua'),
                numero=request.form.get('numero'),
                bairro=request.form.get('bairro'),
                cidade=request.form.get('cidade'),
                estado=request.form.get('estado'),
                pais=request.form.get('pais')
            ))

        # 📄 DOCUMENTO (UPLOAD)
        file = request.files.get('arquivo')

        if file and file.filename:
            filename = secure_filename(file.filename)

            pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'candidatos')
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, filename)
            file.save(caminho)

            data_doc = request.form.get('doc_data')

            db.session.add(DocumentoArquivo(
                candidato_id=candidato.id,
                nome=request.form.get('doc_nome'),
                data_documento=datetime.strptime(data_doc, '%Y-%m-%d') if data_doc else None,
                nome_arquivo=filename,
                caminho=caminho
            ))

        db.session.commit()
        return redirect('/candidatos')

    return render_template('candidato.html')


# =========================
# LISTA CANDIDATOS
# =========================
@main.route('/candidatos')
def lista_candidatos():
    candidatos = Candidato.query.all()
    return render_template('candidatos.html', candidatos=candidatos)


# =========================
# EXCLUIR CANDIDATO
# =========================
@main.route('/excluir-candidato/<int:id>')
def excluir_candidato(id):
    candidato = Candidato.query.get_or_404(id)

    Contato.query.filter_by(candidato_id=id).delete()
    Endereco.query.filter_by(candidato_id=id).delete()
    DocumentoArquivo.query.filter_by(candidato_id=id).delete()

    db.session.delete(candidato)
    db.session.commit()

    return redirect('/candidatos')