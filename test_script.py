
import asyncio
import random
import json
from engine import TennisMatch, Player
from pyscript import document, display, when
from js import localStorage, console

match = None
p1_score_el = document.getElementById("p1-score")
p2_score_el = document.getElementById("p2-score")
p1_games_el = document.getElementById("p1-games")
p2_games_el = document.getElementById("p2-games")
p1_sets_el = document.getElementById("p1-sets")
p2_sets_el = document.getElementById("p2-sets")
commentary_el = document.getElementById("commentary-feed")
ball_el = document.getElementById("ball")
loader_el = document.getElementById("loader")
history_el = document.getElementById("match-history")
event_el = document.getElementById("special-event")

def update_vals(e):
    el_id = e.target.id
    val = e.target.value
    document.getElementById(f"{el_id}-val").innerText = val

for slider in document.querySelectorAll('input[type="range"]'):
    if "-power" in slider.id or "-agility" in slider.id or "-stamina" in slider.id:
        slider.oninput = update_vals
        
def get_comment_variety(msg_type, player_name=""):
    phrases = {
        "winner": [
            f"STUNNING! {player_name} fires a clean winner!",
            f"WHAT A SHOT! {player_name} finds the line!",
            f"Unbelievable angle! {player_name} takes the point in style.",
            f"Too good! {player_name} is dominating the court."
        ],
        "error": [
            f"Tough break. {player_name} misses and gives up the point.",
            f"Wide! {player_name} couldn't keep it in play.",
            f"Into the net! A costly unforced error by {player_name}.",
            f"Pressure mounting. {player_name} fails to find the court."
        ],
        "BREAK POINT": [
            "🚨 MASSIVE OPPORTUNITY! It's BREAK POINT! 🚨",
            "A potential turning point... BREAK POINT!",
            "Can the receiver break through? BREAK POINT!"
        ],
        "SET POINT": [
            "🏆 THE SET IS ON THE LINE! SET POINT! 🏆",
            "One point away from the set! Here we go.",
            "High stakes tennis! IT'S SET POINT!"
        ],
        "MATCH POINT": [
            "👑 CHAMPIONSHIP MOMENT! MATCH POINT! 👑",
            "A historic moment? IT'S MATCH POINT!",
            "CAN THEY CLOSE IT OUT? MATCH POINT!"
        ]
    }
    if msg_type in phrases:
        return random.choice(phrases[msg_type])
    return msg_type
        
def load_history():
    try:
        stored = localStorage.getItem("tennis_history")
        if stored:
            data = json.loads(stored)
            for item in data: render_history_item(item)
    except: pass

def render_history_item(data):
    div = document.createElement("div")
    div.className = "history-item"
    winner_name = data['winner']
    score_summary = data['score']
    div.innerHTML = f"<span class='winner-name'>{winner_name}</span><span class='score-summary'>{score_summary}</span>"
    history_el.prepend(div)

def save_match(winner, score):
    try:
        stored = localStorage.getItem("tennis_history")
        data = json.loads(stored) if stored else []
        data.append({"winner": winner, "score": score})
        if len(data) > 10: data.pop(0)
        localStorage.setItem("tennis_history", json.dumps(data))
        render_history_item({"winner": winner, "score": score})
    except: pass

loader_el.classList.add("hidden")
load_history()

def add_commentary(text, type="info"):
    p = document.createElement("p")
    p.className = f"msg {type}"
    p.innerText = text
    commentary_el.prepend(p)

async def move_ball(to_side):
    speed = int(document.getElementById("match-speed").value)
    t = (speed / 1000) * 0.5
    ball_el.style.transition = f"left {t}s linear, top {t}s linear"
    
    top_pos = random.randint(20, 80)
    if to_side == 1:
        ball_el.style.left = "40px"
        ball_el.style.top = f"{top_pos}%"
        document.getElementById("racket-1").style.top = f"{top_pos}%"
    else:
        ball_el.style.left = "calc(100% - 40px)"
        ball_el.style.top = f"{top_pos}%"
        document.getElementById("racket-2").style.top = f"{top_pos}%"
    
    ball_el.animate([{'transform':'scale(1)'},{'transform':'scale(1.5)','offset':0.5},{'transform':'scale(1)'}],{'duration':t*1000})
    await asyncio.sleep(t)

async def start_match(e):
    global match
    p1_n = document.getElementById("p1-name").value
    p2_n = document.getElementById("p2-name").value
    
    p1_s = {"power": int(document.getElementById("p1-power").value), "agility": int(document.getElementById("p1-agility").value), "stamina": int(document.getElementById("p1-stamina").value)}
    p2_s = {"power": int(document.getElementById("p2-power").value), "agility": int(document.getElementById("p2-agility").value), "stamina": int(document.getElementById("p2-stamina").value)}

    document.getElementById("p1-display").innerText = p1_n
    document.getElementById("p2-display").innerText = p2_n
    
    match = TennisMatch(p1_n, p2_n, p1_s, p2_s)
    add_commentary(f"Battle: {p1_n} vs {p2_n}", "success")
    
    p1_score_el.innerText = "0"
    p2_score_el.innerText = "0"
    p1_games_el.innerText = "0"
    p2_games_el.innerText = "0"
    p1_sets_el.innerText = "0 Sets"
    p2_sets_el.innerText = "0 Sets"

    while not match.winner:
        data = match.simulate_point()
        for hit in data["rally"]:
            side = 2 if hit["hitter"] == match.p1.name else 1
            await move_ball(side)
        
        status = match.get_match_status()
        p1_score_el.innerText = status["p1_score"]
        p2_score_el.innerText = status["p2_score"]
        p1_games_el.innerText = status["p1_games"]
        p2_games_el.innerText = status["p2_games"]
        p1_sets_el.innerText = f"{status['p1_sets']} Sets"
        p2_sets_el.innerText = f"{status['p2_sets']} Sets"

        last_hit = data["rally"][-1]
        if last_hit["type"] == "winner":
            add_commentary(get_comment_variety("winner", last_hit['hitter']), "success")
        elif last_hit["type"] == "error":
            add_commentary(get_comment_variety("error", last_hit['hitter']), "info")

        if status["special_event"]:
            event_el.innerText = status["special_event"]
            event_el.classList.add("active")
            add_commentary(get_comment_variety(status["special_event"]), "winner")
        else:
            event_el.classList.remove("active")

        if match.serving == match.p1:
            document.getElementById("p1-serving").classList.add("active")
            document.getElementById("p2-serving").classList.remove("active")
        else:
            document.getElementById("p2-serving").classList.add("active")
            document.getElementById("p1-serving").classList.remove("active")

        speed = int(document.getElementById("match-speed").value)
        await asyncio.sleep(speed/1000)

    add_commentary(f"🏆 CHAMPIONSHIP POINT CONVERTED! {match.winner.name} takes the match! 🏆", "winner")
    save_match(match.winner.name, f"{match.p1.sets}-{match.p2.sets}")
