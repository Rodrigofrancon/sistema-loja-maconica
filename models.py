from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =========================
# Pessoa (Maçom)
# =========================
class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cim = db.Column(db.String(50))
    data_nascimento = db.Column(db.String(20))
    naturalidade = db.Column(db.String(100))
    nacionalidade = db.Column(db.String(100))
    estado_civil = db.Column(db.String(50))
    sexo = db.Column(db.String(10))
    nome_pai = db.Column(db.String(150))
    nome_mae = db.Column(db.String(150))
    escolaridade = db.Column(db.String(100))
    conjuge = db.Column(db.String(150))
    data_casamento = db.Column(db.String(20))

    # RELACIONAMENTOS
    documento = db.relationship('Documento', backref='pessoa', uselist=False)
    maconico = db.relationship('DadosMaconicos', backref='pessoa', uselist=False)

    # CONTATOS (AGORA LISTA)
    contatos = db.relationship('Contato', backref='pessoa', lazy=True)

    familiares = db.relationship('Familiar', backref='pessoa', lazy=True)


# =========================
# Documentos
# =========================
class Documento(db.Model):
    __tablename__ = 'documento'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    cpf = db.Column(db.String(20), unique=True, nullable=True)
    rg = db.Column(db.String(20))
    titulo_eleitoral = db.Column(db.String(20))


# =========================
# Dados Maçônicos
# =========================
class DadosMaconicos(db.Model):
    __tablename__ = 'dados_maconicos'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    situacao = db.Column(db.String(50))
    forma_admissao = db.Column(db.String(50))
    data_admissao = db.Column(db.String(20))


# =========================
# Familiares
# =========================
class Familiar(db.Model):
    __tablename__ = 'familiar'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    nome = db.Column(db.String(150))
    parentesco = db.Column(db.String(50))
    data_nascimento = db.Column(db.String(20))

    # 🔥 DOCUMENTOS
    cpf = db.Column(db.String(20), nullable=True)
    rg = db.Column(db.String(20))

    # 🔗 RELACIONAMENTO COM CONTATO
    contatos = db.relationship('Contato', backref='familiar', lazy=True)


# =========================
# CONTATO (COMPARTILHADO)
# =========================
class Contato(db.Model):
    __tablename__ = 'contato'

    id = db.Column(db.Integer, primary_key=True)

    # RELAÇÃO FLEXÍVEL
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    familiar_id = db.Column(db.Integer, db.ForeignKey('familiar.id'), nullable=True)

    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(100))

# =========================
# ENDERECO (COMPARTILHADO)
# =========================

class Endereco(db.Model):
    __tablename__ = 'endereco'

    id = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    familiar_id = db.Column(db.Integer, db.ForeignKey('familiar.id'), nullable=True)

    rua = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(20))
    pais = db.Column(db.String(100))  # 🔥 NOVO