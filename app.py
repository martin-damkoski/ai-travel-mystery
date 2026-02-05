from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from database import session
from models import Game, Guess
from services.clues import create_new_game_payload
from services.ai_service import generate_text

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"
import os
print("STATIC PATH:", os.path.join(app.root_path, "static"))
print("STATIC EXISTS:", os.path.exists(os.path.join(app.root_path, "static")))
print("CSS EXISTS:", os.path.exists(os.path.join(app.root_path, "static", "css", "style.css")))

from dotenv import load_dotenv
import os

load_dotenv()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/games")
def games_list():
    games = session.execute(
        select(Game).order_by(Game.created_at.desc())
    ).scalars().all()
    return render_template("games_list.html", games=games)


@app.route("/games/new", methods=["GET", "POST"])
def games_new():
    if request.method == "POST":
        difficulty = (request.form.get("difficulty") or "easy").strip()
        if difficulty not in {"easy", "medium", "hard"}:
            difficulty = "easy"

        payload = create_new_game_payload(difficulty=difficulty)

        game = Game(
            target_country=payload["target_country"],
            target_city=payload["target_city"],
            clues_json=json_dumps(payload["clues"]),
            difficulty=difficulty,
            status="active",
        )
        session.add(game)
        session.commit()
        flash("Креиравте моментално нова игра", "success")
        return redirect(url_for("game_detail", game_id=game.id))

    return render_template("game_form.html")


@app.get("/games/<int:game_id>")
def game_detail(game_id: int):
    game = session.get(Game, game_id)
    if not game:
        return "Не постои игра со ова ID!", 404

    guesses = session.execute(
        select(Guess).where(Guess.game_id == game.id).order_by(Guess.created_at.asc())
    ).scalars().all()

    return render_template(
        "game_detail.html",
        game=game,
        guesses=guesses,
        clues=json.loads(game.clues_json),
    )


@app.post("/games/<int:game_id>/guess")
def submit_guess(game_id: int):
    game = session.get(Game, game_id)
    if not game:
        return "Не постои игра со ова ID!", 404

    if game.status != "active":
        flash("Играта е веќе завршена", "error")
        return redirect(url_for("game_detail", game_id=game.id))

    raw = (request.form.get("guess") or "").strip()
    if not raw:
        flash("Внеси одговор (држава или град): ", "error")
        return redirect(url_for("game_detail", game_id=game.id))

    guess_norm = normalize(raw)
    is_correct = guess_norm in {
        normalize(game.target_country),
        normalize(game.target_city),
    }

    g = Guess(
        game_id=game.id,
        guess_text=raw,
        is_correct=is_correct,
    )
    session.add(g)


    if is_correct:
        game.status = "won"
        flash("Одговорот е точен", "success")
    else:
        flash("Одговорот е неточен, обиди се повторно...", "error")

    session.commit()
    return redirect(url_for("game_detail", game_id=game.id))


@app.post("/ai/action")
def ai_action():

    game_id_raw = (request.form.get("game_id") or "").strip()
    if not game_id_raw.isdigit():
        flash("Невалидно game_id", "error")
        return redirect(url_for("games_list"))

    game = session.get(Game, int(game_id_raw))
    if not game:
        flash("Не постои игра со ова ID!", "error")
        return redirect(url_for("games_list"))

    clues = json.loads(game.clues_json)

    prompt = (
        "Ти си асистент за едукативна географска игра.\n"
        "НЕ СМЕЕШ експлицитно да го кажеш името на градот или државата.\n"
        "Објасни кратко (5–8 реченици) зошто точниот одговор е логичен според трагите.\n"
        "После тоа дај 3 кратки едукативни факти за местото.\n"
        "Пиши на македонски.\n\n"
        f"Траги: {clues}\n"
    )

    try:
        result = generate_text(prompt)
    except Exception as e:
        flash(f"AI грешка: {e}", "error")
        return redirect(url_for("game_detail", game_id=game.id))

    game.ai_explanation = result
    session.commit()
    flash("AI објаснувањето е додадено!", "success")
    return redirect(url_for("game_detail", game_id=game.id))




import json

def json_dumps(obj) -> str:  
    return json.dumps(obj, ensure_ascii=False)

def normalize(s: str) -> str:
    return " ".join(s.lower().split())


if __name__ == "__main__":
    app.run(debug=True)
