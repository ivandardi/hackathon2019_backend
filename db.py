import sqlite3

db = sqlite3.connect('db.sqlite')

with db:
    db.execute("""
    INSERT INTO Aluno (nome, email, instituicao, credito, online)
    VALUES
        ("Nome 1", "nome1@email.com", "UNIFESP", 42.13, 0),
        ("Nome 2", "nome2@email.com", "USP", 107.78, 1),
        ("Nome 3", "nome3@email.com", "FATEC", 10.5, 1)
    """)
    alunos = [id for (id,) in db.execute("SELECT id_aluno FROM Aluno")]



    db.execute("""
    INSERT INTO Monitor (nome, email, instituicao, descricao, reais_por_minuto, online)
    VALUES
        ("Monitor 1", "monitor1@email.com", "UNIVAP", "Oi Eu sou o Goku", 0.2, 1),
        ("Monitor 2", "monitor2@email.com", "FAPONE", "Eu gosto de trens :|", 0.5, 0),
        ("Monitor 3", "monitor3@email.com", "FAFOFO", "WEEEEEEEEEEEEEEEE", 0.35, 1)
    """)
    monitores = [id for (id,) in db.execute("SELECT id_monitor FROM Monitor")]


    db.execute("""
    INSERT INTO Topico (nome, materia)
    VALUES
        ("Segunda Revolucao Industrial", "Historia"),
        ("Holocausto", "Historia"),
        ("Terceira Guerra Mundial", "Historia"),
        ("Funcoes Lineares", "Matematica"),
        ("Sistemas Lineares", "Matematica"),
        ("Derivadas", "Matematica")
    """)
    topicos = [id for (id,) in db.execute("SELECT id_topico FROM Topico")]

    db.executemany("""
    INSERT INTO TopicoAluno (id_aluno, id_topico)
    VALUES (?, ?)
    """,
        [(alunos[0], topicos[0]),
        (alunos[0], topicos[1]),
        (alunos[0], topicos[2]),
        (alunos[1], topicos[4]),
        (alunos[2], topicos[1]),
        (alunos[2], topicos[5])]
    )

    db.executemany("""
    INSERT INTO TopicoMonitor (id_monitor, id_topico)
    VALUES (?, ?)
    """,
        [(monitores[0], topicos[0]),
        (monitores[0], topicos[2]),
        (monitores[1], topicos[4]),
        (monitores[1], topicos[5]),
        (monitores[2], topicos[0]),
        (monitores[2], topicos[3]),
        (monitores[2], topicos[4]),
        (monitores[2], topicos[5])]
    )

    db.executemany("""
    INSERT INTO Atendimento (id_aluno, id_monitor, id_topico, datetime_inicio, datetime_fim, avaliacao)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        [(alunos[0], monitores[0], topicos[0], "2019-05-20 16:40:53", "2019-05-20 16:20:16", 9),
        (alunos[0], monitores[0], topicos[2], "2019-05-25 09:15:37", "2019-05-25 09:55:56", 9.3),
        (alunos[1], monitores[1], topicos[4], "2019-05-06 05:52:42", "2019-05-06 06:15:34", 10),
        (alunos[1], monitores[2], topicos[4], "2019-05-13 17:24:15", "2019-05-13 17:32:36", 5),
        (alunos[2], monitores[2], topicos[5], "2019-05-23 10:35:16", "2019-05-23 10:51:47", 7)]
    )

db.close()
