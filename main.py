from flask import Flask, jsonify, g, request
import sqlite3
from dateutil.parser import parse
import time

DATABASE = 'db.sqlite'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, *args):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return [{key: row[key] for key in row.keys()} for row in rv]


@app.route("/alunos/")
def api_alunos():
    with app.app_context():
        alunos = query_db("SELECT * FROM Aluno")
        for aluno in alunos:
            topicos = query_db(
                """SELECT Topico.id_topico, Topico.nome, Topico.materia FROM Topico, TopicoAluno, Aluno
                    WHERE TopicoAluno.id_topico = Topico.id_topico
                      AND TopicoAluno.id_aluno = Aluno.id_aluno   
                      AND Aluno.id_aluno = ?
                """, aluno["id_aluno"])
            aluno["topicos"] = topicos
        return jsonify(alunos)


@app.route("/aluno/<int:id_aluno>/")
def api_aluno(id_aluno):
    with app.app_context():
        aluno = query_db("SELECT * FROM Aluno WHERE id_aluno = ?", id_aluno)[0]
        topicos = query_db(
            """SELECT Topico.id_topico, Topico.nome, Topico.materia FROM Topico, TopicoAluno, Aluno
                WHERE TopicoAluno.id_topico = Topico.id_topico
                  AND TopicoAluno.id_aluno = Aluno.id_aluno   
                  AND Aluno.id_aluno = ?
            """, id_aluno)
        aluno["topicos"] = topicos
        return jsonify(aluno)


@app.route("/monitores/")
def api_monitores():
    with app.app_context():
        monitores = query_db("SELECT * FROM Monitor")
        for monitor in monitores:
            topicos = query_db(
                """SELECT Topico.id_topico, Topico.nome, Topico.materia FROM Topico, TopicoMonitor, Monitor
                    WHERE TopicoMonitor.id_topico = Topico.id_topico
                      AND TopicoMonitor.id_monitor = Monitor.id_monitor   
                      AND Monitor.id_monitor = ?
                """, monitor["id_monitor"])
            monitor["topicos"] = topicos
            monitor["media"] = query_db("SELECT AVG(avaliacao) AS media FROM Atendimento NATURAL JOIN Monitor WHERE id_monitor = ?", monitor["id_monitor"])[0]["media"]
        return jsonify(monitores)


@app.route("/monitor/<int:id_monitor>/")
def api_monitor(id_monitor):
    with app.app_context():
        monitor = query_db("SELECT * FROM Monitor WHERE id_monitor = ?", id_monitor)[0]
        topicos = query_db(
            """SELECT Topico.id_topico, Topico.nome, Topico.materia FROM Topico, TopicoMonitor, Monitor
                WHERE TopicoMonitor.id_topico = Topico.id_topico
                  AND TopicoMonitor.id_monitor = Monitor.id_monitor   
                  AND Monitor.id_monitor = ?
            """, id_monitor)
        monitor["topicos"] = topicos
        monitor["media"] = query_db("SELECT AVG(avaliacao) AS media FROM Atendimento NATURAL JOIN Monitor WHERE id_monitor = ?", id_monitor)[0]["media"]
        return jsonify(monitor)


@app.route("/topicos/")
def api_topicos():
    with app.app_context():
        aluno = query_db("SELECT * FROM Topico")
        return jsonify(aluno)


@app.route("/topico/<int:id_topico>/")
def api_topico(id_topico):
    with app.app_context():
        aluno = query_db("SELECT * FROM Topico WHERE id_topico = ?", id_topico)[0]
        return jsonify(aluno)


# POST precisa de: id_aluno, id_monitor, id_topico, datetime_inicio, datetime_fim, avaliacao
@app.route("/atendimentos/", methods=["GET", "POST"])
def api_atendimentos():
    if request.method == "POST":
        with app.app_context():
            query_db(
                "INSERT INTO Atendimento (id_aluno, id_monitor, id_topico, datetime_inicio, datetime_fim, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                request.form["id_aluno"],
                request.form["id_monitor"],
                request.form["id_topico"],
                request.form["datetime_inicio"],
                request.form["datetime_fim"],
                request.form["avaliacao"],
            )

            dt_inicio = parse(request.form["datetime_inicio"])
            dt_fim = parse(request.form["datetime_fim"])

            unix_inicio = time.mktime(dt_inicio.timetuple())
            unix_fim = time.mktime(dt_fim.timetuple())

            tempo_total = int(unix_fim - unix_inicio) / 60

            rpm = query_db("SELECT reais_por_minuto FROM Monitor WHERE id_monitor = ?", request.form["id_monitor"])

            custo_total = tempo_total * rpm

            query_db("UPDATE Aluno SET credito = credito - ? WHERE id_aluno = ?", custo_total, request.form["id_aluno"])
    else:
        with app.app_context():
            atendimento = query_db("SELECT * FROM Atendimento")
            return jsonify(atendimento)


if __name__ == "__main__":
    app.run(debug=False)
