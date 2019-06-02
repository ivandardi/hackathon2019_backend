CREATE TABLE Aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    instituicao TEXT NOT NULL,
    credito FLOAT NOT NULL,
    online INTEGER NOT NULL
);

CREATE TABLE Monitor (
    id_monitor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    instituicao TEXT NOT NULL,
    descricao TEXT NOT NULL,
    reais_por_minuto FLOAT NOT NULL,
    online INTEGER NOT NULL
);

CREATE TABLE Topico (
    id_topico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    materia TEXT NOT NULL
);

CREATE TABLE TopicoAluno (
    id_topico INTEGER REFERENCES Topico (id_topico),
    id_aluno INTEGER REFERENCES Aluno (id_aluno)
);

CREATE TABLE TopicoMonitor (
    id_topico INTEGER REFERENCES Topico (id_topico),
    id_monitor INTEGER REFERENCES Monitor (id_monitor)
);

CREATE TABLE Atendimento (
    id_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER REFERENCES Aluno (id_aluno),
    id_monitor INTEGER REFERENCES Monitor (id_monitor),
    id_topico INTEGER REFERENCES Topico (id_topico),
    datetime_inicio TEXT NOT NULL,
    datetime_fim TEXT NOT NULL,
    avaliacao INTEGER NOT NULL
);
