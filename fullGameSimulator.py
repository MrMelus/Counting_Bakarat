import random
import pandas as pd

# Baseline calcolata
EV0 = -0.26

def run_simulation_without_card(n, card_to_remove=None):
    game_state = {
        "deck": [0] * 13,
        "cards": 52 * 8,
        "p1": 0,
        "p2": 0,
        "banco": 0,
        "betValue": 10,
        "balance": 0,
        "totalBalance": 0,
        "mani": 0
    }
    
    for _ in range(n):
        game_state["deck"] = [0] * 13
        game_state["cards"] = 52 * 8
        game_state["balance"] = 0
        
        # Se dobbiamo rimuovere una carta, escludiamo tutte le 32 copie
        if card_to_remove is not None:
            game_state["deck"][card_to_remove] = 32
            game_state["cards"] -= 32

        play(game_state)

    ev_rimozione = game_state["totalBalance"] / game_state["mani"]
    return ev_rimozione

def play(gs):
    while gs["cards"] > 9:
        gs["p1"] = 0
        gs["p2"] = 0
        gs["banco"] = 0
        deal(gs) 
        winners(gs)
        gs["mani"] += 1
    gs["totalBalance"] += gs["balance"]

def deal(gs):
    for _ in range(2):
        val = pick(gs) + 1
        if val >= 10: val = 0
        gs["p1"] += val

        val = pick(gs) + 1
        if val >= 10: val = 0
        gs["p2"] += val

        val = pick(gs) + 1
        if val >= 10: val = 0
        gs["banco"] += val

    gs["p1"] %= 10
    gs["p2"] %= 10
    gs["banco"] %= 10
    decision(gs)

def decision(gs):
    carte = [0] * 2
    if gs["banco"] < 8:
        if gs["p1"] <= 4:
            carte[0] = pick(gs) + 1
            if carte[0] >= 10: carte[0] = 0
            gs["p1"] += carte[0]
        if gs["p2"] <= 4:
            carte[1] = pick(gs) + 1
            if carte[1] >= 10: carte[1] = 0
            gs["p2"] += carte[1]
        if gs["banco"] <= 5:
            if banco_playstyle(gs, carte[0], carte[1]) == 1:
                val = pick(gs) + 1
                if val >= 10: val = 0
                gs["banco"] += val

    gs["p1"] %= 10
    gs["p2"] %= 10
    gs["banco"] %= 10

def pick(gs):
    value = random.randint(0, 12)
    while gs["deck"][value] > 31:
        value = random.randint(0, 12)
    gs["deck"][value] += 1
    gs["cards"] -= 1
    return value

def banco_playstyle(gs, c1, c2):
    if gs["p1"] <= 4 and c1 <= 2 and gs["p2"] <= 4 and c2 <= 2 and gs["banco"] == 4: return 0
    elif gs["p1"] >= 5 and gs["p2"] >= 5 and gs["banco"] == 5: return 1
    elif gs["p1"] >= 8 and gs["p2"] >= 8 and gs["banco"] <= 7: return 1
    elif gs["banco"] <= 4: return 1
    else: return 0

def winners(gs):
    res1 = "vince" if gs["p1"] > gs["banco"] else ("come" if gs["p1"] == gs["banco"] else "perde")
    if res1 == "vince": 
        gs["balance"] += gs["betValue"]
    elif res1 == "perde": 
        gs["balance"] -= gs["betValue"]

def main():
    n_sabot = 50000 
    nomi_carte = ['Asso', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    print(f"{'Carta Rimossa':<12} | {'EV con rimozione':<18} | {'EoR (Delta)':<14} | {'Segno Suggerito'}")
    print("-" * 65)

    risultati_eor = []

    for rango in range(13):
        ev_c = run_simulation_without_card(n_sabot, card_to_remove=rango)
        delta = ev_c - EV0  # EV_senza - EV0
        
        if delta > 0.03:
            segno = "+1 (Favorevole al Banco)"
        elif delta < -0.03:
            segno = "-1 (Favorevole a P1)"
        else:
            segno = " 0 (Neutro)"
            
        print(f"{nomi_carte[rango]:<12} | {ev_c:<18.4f} | {delta:<+14.4f} | {segno}")
        
        risultati_eor.append({
            "Rango": rango,
            "Carta": nomi_carte[rango],
            "EV_Senza": ev_c,
            "EoR": delta,
            "Segno_Suggerito": segno
        })

    # Esportazione rapida dei dati grezzi
    df_eor = pd.DataFrame(risultati_eor)
    df_eor.to_excel("report_metodi/risultati_EoR.xlsx", index=False)
    print("\nRisultati salvati su report_metodi/risultati_EoR.xlsx")

if __name__ == "__main__":
    main()