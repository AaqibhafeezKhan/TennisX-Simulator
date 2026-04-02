import random
import time

class Player:
    def __init__(self, name, power=80, agility=80, stamina=80, style="All-Court"):
        self.name = name
        self.style = style
        self.power = power
        self.agility = agility
        self.stamina = stamina
        self.points = 0
        self.games = 0
        self.sets = 0

    def get_score_label(self, other_player_points):
        scores = ["0", "15", "30", "40"]
        if self.points < 3:
            return scores[self.points]
        
        if self.points == other_player_points:
            return "40"
        if self.points > other_player_points:
            return "AD"
        return "40"

class TennisMatch:
    def __init__(self, p1_name, p2_name, p1_stats, p2_stats):
        self.p1 = Player(p1_name, **p1_stats)
        self.p2 = Player(p2_name, **p2_stats)
        self.serving = self.p1
        self.receiver = self.p1 if self.p1 == self.p2 else self.p2
        if p1_name == p2_name:
            self.p2.name = p2_name + " "
        self.serving = self.p1
        self.receiver = self.p2
        self.winner = None
        self.log = []

    def simulate_point(self):
        rally = []
        current_hitter = self.serving
        current_receiver = self.receiver
        
        rally.append({"hitter": current_hitter.name, "type": "serve"})
        
        while True:
            stamina_factor = (current_hitter.stamina / 100) * 0.5 + 0.5
            success_chance = ((current_hitter.power + current_hitter.agility) / 2) * stamina_factor
            
            pressure = (current_receiver.agility / 10)
            roll = random.randint(0, 100) + pressure
            
            if roll > success_chance:
                winner = current_receiver
                rally.append({"hitter": current_hitter.name, "type": "error", "winner": winner.name})
                winner.points += 1
                current_hitter.stamina = max(10, current_hitter.stamina - 2)
                self.check_scoring()
                return {"winner": winner, "rally": rally}
            
            winner_chance = (current_hitter.power / 15)
            if random.random() * 100 < winner_chance and len(rally) > 2:
                winner = current_hitter
                rally.append({"hitter": current_hitter.name, "type": "winner", "winner": winner.name})
                winner.points += 1
                current_hitter.stamina = max(10, current_hitter.stamina - 1)
                self.check_scoring()
                return {"winner": winner, "rally": rally}

            rally.append({"hitter": current_hitter.name, "type": "hit"})
            current_hitter.stamina = max(10, current_hitter.stamina - 0.5)
            current_hitter, current_receiver = current_receiver, current_hitter
            
            if len(rally) > 30:
                break

        winner = random.choice([self.p1, self.p2])
        winner.points += 1
        self.check_scoring()
        return {"winner": winner, "rally": rally}

    def check_scoring(self):
        p1, p2 = self.p1, self.p2
        
        if p1.games == 6 and p2.games == 6:
            self.handle_tiebreak()
            return

        if p1.points >= 4 and p1.points - p2.points >= 2:
            p1.games += 1
            self.reset_points()
            self.switch_server()
        elif p2.points >= 4 and p2.points - p1.points >= 2:
            p2.games += 1
            self.reset_points()
            self.switch_server()
        
        if p1.points >= 3 and p2.points >= 3 and p1.points == p2.points and p1.points > 3:
            p1.points = 3
            p2.points = 3
        
        if p1.games >= 6 and p1.games - p2.games >= 2:
            p1.sets += 1
            self.reset_games()
        elif p2.games >= 6 and p2.games - p1.games >= 2:
            p2.sets += 1
            self.reset_games()
            
        if p1.sets == 2:
            self.winner = p1
        elif p2.sets == 2:
            self.winner = p2

    def handle_tiebreak(self):
        p1, p2 = self.p1, self.p2
        if p1.points >= 7 and p1.points - p2.points >= 2:
            p1.sets += 1
            p1.games = 7
            p2.games = 6
            self.reset_points()
            self.reset_games()
        elif p2.points >= 7 and p2.points - p1.points >= 2:
            p2.sets += 1
            p1.games = 6
            p2.games = 7
            self.reset_points()
            self.reset_games()

    def reset_points(self):
        self.p1.points = 0
        self.p2.points = 0

    def reset_games(self):
        self.p1.games = 0
        self.p2.games = 0

    def switch_server(self):
        self.serving, self.receiver = self.receiver, self.serving

    def get_match_status(self):
        p1, p2 = self.p1, self.p2
        is_tiebreak = p1.games == 6 and p2.games == 6
        
        special_event = None
        if not self.winner:
            p1_needed = 2 - p1.sets
            p2_needed = 2 - p2.sets
            
            if (p1.games >= 5 and p1.points >= 3 and p1.points > p2.points and p1_needed == 1) or \
               (p2.games >= 5 and p2.points >= 3 and p2.points > p1.points and p2_needed == 1):
                special_event = "MATCH POINT"
            elif p1.games >= 5 or p2.games >= 5:
                if (p1.games >= 5 and p1.points >= 3 and p1.points > p2.points) or \
                   (p2.games >= 5 and p2.points >= 3 and p2.points > p1.points):
                    special_event = "SET POINT"
            elif (self.serving == p1 and p2.points >= 3 and p2.points > p1.points) or \
                 (self.serving == p2 and p1.points >= 3 and p1.points > p2.points):
                special_event = "BREAK POINT"

        return {
            "p1_score": str(p1.points) if is_tiebreak else p1.get_score_label(p2.points),
            "p2_score": str(p2.points) if is_tiebreak else p2.get_score_label(p1.points),
            "p1_games": p1.games,
            "p2_games": p2.games,
            "p1_sets": p1.sets,
            "p2_sets": p2.sets,
            "winner": self.winner.name if self.winner else None,
            "is_tiebreak": is_tiebreak,
            "special_event": special_event
        }
