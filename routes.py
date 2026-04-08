from flask import Blueprint, render_template, request, redirect
from models import db, Pessoa, Documento, DadosMaconicos, Familiar, Contato, Endereco

main = Blueprint('main', __name__)


# =========================
# LISTAGEM
# =========================
@main.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)


# =========================
# ➕ CADASTRO
# =========================
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':

        # =========================
        # PESSOA
        # =========================
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

        # =========================
        # DOCUMENTO
        # =========================
        cpf = request.form.get('cpf') or None

        documento = Documento(
            pessoa_id=pessoa.id,
            cpf=cpf,
            rg=request.form.get('rg'),
            titulo_eleitoral=request.form.get('titulo')
        )

        db.session.add(documento)

        # =========================
        #CONTATO
        # =========================
        if request.form.get('telefone') or request.form.get('celular') or request.form.get('email'):
            contato_pessoa = Contato(
                pessoa_id=pessoa.id,
                telefone=request.form.get('telefone'),
                celular=request.form.get('celular'),
                whatsapp=request.form.get('whatsapp'),
                email=request.form.get('email')
            )
            db.session.add(contato_pessoa)

        # =========================
        # DADOS MAÇÔNICOS
        # =========================
        dados = DadosMaconicos(
            pessoa_id=pessoa.id,
            situacao=request.form.get('situacao'),
            forma_admissao=request.form.get('forma'),
            data_admissao=request.form.get('data_admissao')
        )

        db.session.add(dados)

        # =========================
        #ENDEREÇO 
        # =========================
        if request.form.get('cep') or request.form.get('rua'):
            endereco = Endereco(
                pessoa_id=pessoa.id,
                cep=request.form.get('cep'),
                rua=request.form.get('rua'),
                numero=request.form.get('numero'),
                bairro=request.form.get('bairro'),
                cidade=request.form.get('cidade'),
                estado=request.form.get('estado'),
                pais=request.form.get('pais')
            )
            db.session.add(endereco)

        # =========================
        # FAMILIAR
        # =========================
        if request.form.get('familiar_nome'):
            familiar = Familiar(
                pessoa_id=pessoa.id,
                nome=request.form.get('familiar_nome'),
                parentesco=request.form.get('familiar_parentesco'),
                data_nascimento=request.form.get('familiar_nascimento'),
                cpf=request.form.get('familiar_cpf'),
                rg=request.form.get('familiar_rg')
            )

            db.session.add(familiar)
            db.session.commit()  # necessário para obter ID

            # =========================
            # CONTATO DO FAMILIAR
            # =========================
            if request.form.get('familiar_telefone') or request.form.get('familiar_celular') or request.form.get('familiar_email'):
                contato_familiar = Contato(
                    familiar_id=familiar.id,
                    telefone=request.form.get('familiar_telefone'),
                    celular=request.form.get('familiar_celular'),
                    email=request.form.get('familiar_email')
                )
                db.session.add(contato_familiar)

        # =========================
        # COMMIT FINAL
        # =========================
        db.session.commit()

        return redirect('/')

    return render_template('cadastro.html')

# =========================
# EDITAR
# =========================
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':
        pessoa.nome = request.form.get('nome')
        pessoa.cim = request.form.get('cim')
        pessoa.data_nascimento = request.form.get('data_nascimento')

        db.session.commit()
        return redirect('/')

    return render_template('editar.html', pessoa=pessoa)

# =========================
# EXCLUIR
# =========================
@main.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)

    Documento.query.filter_by(pessoa_id=id).delete()
    DadosMaconicos.query.filter_by(pessoa_id=id).delete()
    Contato.query.filter_by(pessoa_id=id).delete()
    Endereco.query.filter_by(pessoa_id=id).delete()

    familiares = Familiar.query.filter_by(pessoa_id=id).all()
    for f in familiares:
        Contato.query.filter_by(familiar_id=f.id).delete()
        db.session.delete(f)

    db.session.delete(pessoa)
    db.session.commit()

    return redirect('/')

