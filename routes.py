from flask import Blueprint, render_template, request, redirect, current_app, send_file
from models import db, Pessoa, DadosMaconicos, Familiar, Contato, Endereco, Candidato, DocumentoArquivo, CargoMaconico
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
            cpf=request.form.get('cpf'),
            rg=request.form.get('rg'),
            titulo=request.form.get('titulo')
        )

        db.session.add(pessoa)
        db.session.commit()

        # CONTATO
        telefones = request.form.getlist('telefone[]')
        celulares = request.form.getlist('celular[]')
        whatsapps = request.form.getlist('whatsapp[]')
        emails = request.form.getlist('email[]')

        for i in range(len(telefones)):
            if telefones[i] or celulares[i] or emails[i]:
                db.session.add(Contato(
                    pessoa_id=pessoa.id,
                    telefone=telefones[i],
                    celular=celulares[i] if i < len(celulares) else None,
                    whatsapp=whatsapps[i] if i < len(whatsapps) else None,
                    email=emails[i] if i < len(emails) else None
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

        # DADOS MAÇÔNICOS
        db.session.add(DadosMaconicos(
            pessoa_id=pessoa.id,
            situacao=request.form.get('situacao'),
            forma_admissao=request.form.get('forma'),
            data_admissao=request.form.get('data_admissao'),
            grau=request.form.get('grau'),
            data_saida=request.form.get('data_saida'),
            loja_origem=request.form.get('loja_origem')
        ))

        # =========================
        # 📄 DOCUMENTOS
        # =========================
        files = request.files.getlist('arquivo[]')
        nomes = request.form.getlist('doc_nome[]')
        datas = request.form.getlist('doc_data[]')

        pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'macons')
        os.makedirs(pasta, exist_ok=True)

        for i in range(len(files)):
            file = files[i]

            if file and file.filename:
                filename = secure_filename(file.filename)
                caminho = os.path.join(pasta, filename)
                file.save(caminho)

                data_doc = datas[i] if i < len(datas) else None

                db.session.add(DocumentoArquivo(
                    pessoa_id=pessoa.id,
                    nome=nomes[i] if i < len(nomes) else '',
                    data_documento=datetime.strptime(data_doc, '%Y-%m-%d') if data_doc else None,
                    nome_arquivo=filename,
                    caminho=caminho
                ))

        # =========================
        # 🏛️ CARGOS
        # =========================
        cargos = request.form.getlist('cargo_nome[]')
        datas_inicio = request.form.getlist('cargo_inicio[]')
        datas_fim = request.form.getlist('cargo_fim[]')

        for i in range(len(cargos)):
            if cargos[i]:
                db.session.add(CargoMaconico(
                    pessoa_id=pessoa.id,
                    cargo=cargos[i],
                    data_inicio=datas_inicio[i] if i < len(datas_inicio) else None,
                    data_fim=datas_fim[i] if i < len(datas_fim) else None
                ))

        db.session.commit()
        return redirect('/macons')

    return render_template('cadastro.html')

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

        # =========================
        # CONTATO
        # =========================
        if request.form.get('telefone') or request.form.get('celular'):
            db.session.add(Contato(
                candidato_id=candidato.id,
                telefone=request.form.get('telefone'),
                celular=request.form.get('celular'),
                email=request.form.get('email')
            ))

        # =========================
        # ENDEREÇO
        # =========================
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

        db.session.commit()

        return redirect('/candidatos')

    return render_template('candidato.html')

# =========================
# LISTA CANDIDATOS
# =========================
@main.route('/candidatos')
def candidatos():
    candidatos = Candidato.query.all()
    return render_template('candidatos.html', candidatos=candidatos)

# =========================
# EDITAR CANDIDATO
# =========================
@main.route('/editar-candidato/<int:id>', methods=['GET', 'POST'])
def editar_candidato(id):
    candidato = Candidato.query.get_or_404(id)

    if request.method == 'POST':

        # DADOS
        candidato.nome = request.form.get('nome')
        candidato.cpf = request.form.get('cpf')
        candidato.rg = request.form.get('rg')
        candidato.titulo = request.form.get('titulo')
        candidato.data_candidatura = request.form.get('data_candidatura')
        candidato.situacao = request.form.get('situacao')

        # CONTATO (remove e recria)
        Contato.query.filter_by(candidato_id=candidato.id).delete()

        db.session.add(Contato(
            candidato_id=candidato.id,
            telefone=request.form.get('telefone'),
            celular=request.form.get('celular'),
            email=request.form.get('email')
        ))

        # ENDEREÇO (remove e recria)
        Endereco.query.filter_by(candidato_id=candidato.id).delete()

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

        db.session.commit()

        return redirect('/candidatos')

    return render_template('editar_candidato.html', candidato=candidato)

# =========================
# EDITAR MAÇOM
# =========================
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':

        # DADOS
        pessoa.nome = request.form.get('nome')
        pessoa.cim = request.form.get('cim')
        pessoa.data_nascimento = request.form.get('data_nascimento')
        pessoa.naturalidade = request.form.get('naturalidade')
        pessoa.nacionalidade = request.form.get('nacionalidade')
        pessoa.estado_civil = request.form.get('estado_civil')
        pessoa.sexo = request.form.get('sexo')
        pessoa.nome_pai = request.form.get('nome_pai')
        pessoa.nome_mae = request.form.get('nome_mae')
        pessoa.escolaridade = request.form.get('escolaridade')
        pessoa.conjuge = request.form.get('conjuge')
        pessoa.data_casamento = request.form.get('data_casamento')
        pessoa.cpf = request.form.get('cpf')
        pessoa.rg = request.form.get('rg')
        pessoa.titulo = request.form.get('titulo')

        # CONTATO
        contato = pessoa.contatos[0] if pessoa.contatos else Contato(pessoa_id=pessoa.id)
        contato.telefone = request.form.get('telefone')
        contato.celular = request.form.get('celular')
        contato.email = request.form.get('email')
        if not pessoa.contatos:
            db.session.add(contato)

        # ENDEREÇO
        endereco = pessoa.enderecos[0] if pessoa.enderecos else Endereco(pessoa_id=pessoa.id)
        endereco.cep = request.form.get('cep')
        endereco.rua = request.form.get('rua')
        endereco.numero = request.form.get('numero')
        endereco.bairro = request.form.get('bairro')
        endereco.cidade = request.form.get('cidade')
        endereco.estado = request.form.get('estado')
        endereco.pais = request.form.get('pais')
        if not pessoa.enderecos:
            db.session.add(endereco)

        # MAÇÔNICO
        maconico = pessoa.maconico if pessoa.maconico else DadosMaconicos(pessoa_id=pessoa.id)
        maconico.situacao = request.form.get('situacao')
        maconico.forma_admissao = request.form.get('forma')
        maconico.data_admissao = request.form.get('data_admissao')
        maconico.grau = request.form.get('grau')
        maconico.data_saida = request.form.get('data_saida')
        maconico.loja_origem = request.form.get('loja_origem')

        if not pessoa.maconico:
            db.session.add(maconico)

        # CARGOS (recria histórico)
        CargoMaconico.query.filter_by(pessoa_id=pessoa.id).delete()

        cargos = request.form.getlist('cargo_nome[]')
        datas_inicio = request.form.getlist('cargo_inicio[]')
        datas_fim = request.form.getlist('cargo_fim[]')

        for i in range(len(cargos)):
            if cargos[i]:
                db.session.add(CargoMaconico(
                    pessoa_id=pessoa.id,
                    cargo=cargos[i],
                    data_inicio=datas_inicio[i] if i < len(datas_inicio) else None,
                    data_fim=datas_fim[i] if i < len(datas_fim) else None
                ))

        db.session.commit()
        return redirect('/macons')

    return render_template('editar.html', pessoa=pessoa)


# =========================
# EXCLUIR
# =========================
@main.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)

    DadosMaconicos.query.filter_by(pessoa_id=id).delete()
    Endereco.query.filter_by(pessoa_id=id).delete()
    DocumentoArquivo.query.filter_by(pessoa_id=id).delete()
    CargoMaconico.query.filter_by(pessoa_id=id).delete()
    
    telefones = request.form.getlist('telefone[]')
    celulares = request.form.getlist('celular[]')
    whatsapps = request.form.getlist('whatsapp[]')
    emails = request.form.getlist('email[]')

    for i in range(len(telefones)):
        if telefones[i] or celulares[i] or emails[i]:
            db.session.add(Contato(
                pessoa_id=pessoa.id,
                telefone=telefones[i],
                celular=celulares[i] if i < len(celulares) else None,
                whatsapp=whatsapps[i] if i < len(whatsapps) else None,
                email=emails[i] if i < len(emails) else None
            ))

    db.session.delete(pessoa)
    db.session.commit()

    return redirect('/macons')


# =========================
# DOCUMENTOS
# =========================
@main.route('/documentos/pessoa/<int:id>')
def documentos_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    return render_template('documentos.html', documentos=pessoa.documentos)


# =========================
# DOWNLOAD
# =========================
@main.route('/download/<int:id>')
def download(id):
    doc = DocumentoArquivo.query.get_or_404(id)

    if not os.path.exists(doc.caminho):
        return "Arquivo não encontrado", 404

    return send_file(doc.caminho, as_attachment=True)