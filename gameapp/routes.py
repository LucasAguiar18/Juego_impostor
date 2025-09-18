from flask import Blueprint, render_template, request, redirect, session, url_for

main_bp = Blueprint("main", __name__)


# Página inicial: botón para ingresar
@main_bp.route("/")
def lobby():
    return render_template("lobby.html")

# Formulario de nickname
@main_bp.route("/nickname")
def nickname():
    return render_template("nickname.html")

# Recibe nickname y redirige a sala principal
@main_bp.route("/join", methods=["POST"])
def join():
    nickname = request.form.get("nickname")
    if not nickname:
        return redirect(url_for("main.nickname"))
    session["nickname"] = nickname
    return redirect(url_for("main.sala"))

# Sala principal
@main_bp.route("/sala")
def sala():
    nickname = session.get("nickname")
    if not nickname:
        return redirect(url_for("main.nickname"))
    return render_template("sala.html", nickname=nickname)
