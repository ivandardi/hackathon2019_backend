import sqlite3
import random
import math

QTD = 35

db = sqlite3.connect('db.sqlite')

instituicoes = ["USP", "UNICAMP", "UNIFESP", "FAPONE", "FAFOFO", "UNIVAP", "UFMG", "UFRJ"]


def decode(i):
    k = math.floor((1 + math.sqrt(1 + 8 * i)) / 2)
    return k, i - k * (k - 1) // 2


def rand_pair(n):
    return decode(random.uniform(n * (n - 1) // 2))


def rand_pairs(n, m):
    return [decode(i) for i in random.sample(range(n * (n - 1) // 2), m)]


with db:
    db.execute("""
    CREATE TABLE Aluno (
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        instituicao TEXT NOT NULL,
        credito FLOAT NOT NULL,
        online INTEGER NOT NULL)
    """)

    db.execute("""
    CREATE TABLE Monitor (
        id_monitor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        instituicao TEXT NOT NULL,
        descricao TEXT NOT NULL,
        reais_por_minuto FLOAT NOT NULL,
        online INTEGER NOT NULL)
    """)

    db.execute("""
    CREATE TABLE Topico (
        id_topico INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        materia TEXT NOT NULL)
    """)

    db.execute("""
    CREATE TABLE TopicoAluno (
        id_topico INTEGER REFERENCES Topico (id_topico),
        id_aluno INTEGER REFERENCES Aluno (id_aluno))
    """)

    db.execute("""
    CREATE TABLE TopicoMonitor (
        id_topico INTEGER REFERENCES Topico (id_topico),
        id_monitor INTEGER REFERENCES Monitor (id_monitor))
    """)

    db.execute("""
    CREATE TABLE Atendimento (
        id_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER REFERENCES Aluno (id_aluno),
        id_monitor INTEGER REFERENCES Monitor (id_monitor),
        id_topico INTEGER REFERENCES Topico (id_topico),
        datetime_inicio TEXT NOT NULL,
        datetime_fim TEXT NOT NULL,
        avaliacao INTEGER NOT NULL)
    """)

    for i in range(QTD):
        db.execute("""
        INSERT INTO Aluno (nome, email, instituicao, credito, online)
        VALUES (?, ?, ?, ?, ?)
        """,
                   ("Aluno {}".format(i), "aluno{}@email.com".format(i), random.choice(instituicoes),
                    random.uniform(100.0, 700.0), random.randint(0, 1))
                   )
    alunos = [id for (id,) in db.execute("SELECT id_aluno FROM Aluno")]

    for i in range(QTD):
        db.execute("""
        INSERT INTO Monitor (nome, email, instituicao, descricao, reais_por_minuto, online)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
                   ("Monitor {}".format(i), "monitor{}@email.com".format(i), random.choice(instituicoes),
                    "Terças e Quintas às 14h00", random.uniform(0.15, 0.50), random.randint(0, 1))
                   )
    monitores = [id for (id,) in db.execute("SELECT id_monitor FROM Monitor")]

    db.execute("""
    INSERT INTO Topico (nome, materia)
    VALUES
        ("Segunda Revolucao Industrial", "Historia"),
        ("Holocausto", "Historia"),
        ("Atenas", "Historia"),
        ("Esparta", "Historia"),
        ("Pre-Historia", "Historia"),
        ("Idade Antiga", "Historia"),
        ("Idade Media", "Historia"),
        ("Guerra Fria", "Historia"),
        ("Reforma Protestante", "Historia"),
        ("Segunda Guerra Mundial", "Historia"),
        ("Terceira Guerra Mundial", "Historia"),
        ("Funcoes Lineares", "Matematica"),
        ("Sistemas Lineares", "Matematica"),
        ("Derivadas", "Matematica"),
        ("Integrais", "Matematica"),
        ("Conjuntos", "Matematica"),
        ("Progressoes", "Matematica"),
        ("Analise Combinatoria", "Matematica"),
        ("Trigonometria", "Matematica"),
        ("Geometria Plana", "Matematica"),
        ("Origem da Vida", "Biologia"),
        ("Citologia", "Biologia"),
        ("Reproducao", "Biologia"),
        ("Embriologia", "Biologia"),
        ("Histologia", "Biologia"),
        ("Seres Vivos", "Biologia"),
        ("Genetica", "Biologia"),
        ("Evolucao", "Biologia"),
        ("Ecologia", "Biologia"),
        ("Projeteis", "Fisica"),
        ("Eletrodinamica", "Fisica"),
        ("Termodinamica", "Fisica"),
        ("Eletromagnetismo", "Fisica"),
        ("Acustica", "Fisica"),
        ("Optica", "Fisica"),
        ("Eletrostatica", "Fisica"),
        ("Hidrostatica", "Fisica"),
        ("Mecanica", "Fisica"),
        ("Pneumatica", "Fisica"),
        ("Fluidos", "Fisica"),
        ("Movimento Uniforme", "Fisica"),
        ("Movimento Uniformemente Acelerado", "Fisica"),
        ("Vocabulario", "Portugues"),
        ("Gramatica", "Portugues"),
        ("Verbos", "Portugues"),
        ("Pronomes", "Portugues"),
        ("Substantivos", "Portugues"),
        ("Adjetivos", "Portugues")
    """)
    topicos = [id for (id,) in db.execute("SELECT id_topico FROM Topico")]

    for a, b in rand_pairs(QTD, 75):
        db.execute("""
        INSERT INTO TopicoAluno (id_aluno, id_topico)
        VALUES (?, ?)
    """, (alunos[a], random.choice(topicos)))

    for a, b in rand_pairs(QTD, 75):
        db.execute("""
        INSERT INTO TopicoMonitor (id_monitor, id_topico)
        VALUES (?, ?)
        """, (monitores[a], random.choice(topicos)))

    for _ in range(300):
        db.execute("""
        INSERT INTO Atendimento (id_aluno, id_monitor, id_topico, datetime_inicio, datetime_fim, avaliacao)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (random.choice(alunos), random.choice(monitores), random.choice(topicos), "2019-05-20 16:40:53", "2019-05-20 17:15:17", random.uniform(0, 10)))


db.close()
