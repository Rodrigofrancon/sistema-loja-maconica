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
    cpf = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    titulo = db.Column(db.String(20))
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
    maconico = db.relationship('DadosMaconicos', backref='pessoa', uselist=False)
    contatos = db.relationship('Contato', backref='pessoa', lazy=True)
    familiares = db.relationship('Familiar', backref='pessoa', lazy=True)
    documentos = db.relationship('DocumentoArquivo', backref='pessoa', lazy=True)
    cargos = db.relationship('CargoMaconico', backref='pessoa', lazy=True)


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
    grau = db.Column(db.String(20))
    loja_origem = db.Column(db.String(150))
    data_saida = db.Column(db.String(20))
    motivo_saida = db.Column(db.String(200))
    
class CargoMaconico(db.Model):
    __tablename__ = 'cargo_maconico'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    cargo = db.Column(db.String(100))
    data_inicio = db.Column(db.String(20))
    data_fim = db.Column(db.String(20))

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

    cpf = db.Column(db.String(20), nullable=True)
    rg = db.Column(db.String(20))

    contatos = db.relationship('Contato', backref='familiar', lazy=True)


# =========================
# CONTATO (COMPARTILHADO)
# =========================
class Contato(db.Model):
    __tablename__ = 'contato'

    id = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    familiar_id = db.Column(db.Integer, db.ForeignKey('familiar.id'), nullable=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=True)

    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(100))
    principal = db.Column(db.Boolean, default=False)


# =========================
# ENDEREÇO (COMPARTILHADO)
# =========================
class Endereco(db.Model):
    __tablename__ = 'endereco'

    id = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    familiar_id = db.Column(db.Integer, db.ForeignKey('familiar.id'), nullable=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=True)

    rua = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(20))
    pais = db.Column(db.String(100))


# =========================
# CANDIDATO
# =========================
class Candidato(db.Model):
    __tablename__ = 'candidato'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    titulo = db.Column(db.String(20))

    data_candidatura = db.Column(db.String(20))
    situacao = db.Column(db.String(50))

    contatos = db.relationship('Contato', backref='candidato', lazy=True)
    enderecos = db.relationship('Endereco', backref='candidato', lazy=True)
    documentos = db.relationship('DocumentoArquivo', backref='candidato', lazy=True)
    
    ativo = db.Column(db.Boolean, default=True)
    data_exclusao = db.Column(db.DateTime, nullable=True)


# =========================
# DOCUMENTOS (ÚNICO MODELO)
# =========================
class DocumentoArquivo(db.Model):
    __tablename__ = 'documento_arquivo'

    id = db.Column(db.Integer, primary_key=True)

    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=True)

    nome = db.Column(db.String(150))  # descrição livre
    data_documento = db.Column(db.Date)

    nome_arquivo = db.Column(db.String(200))
    caminho = db.Column(db.String(300))