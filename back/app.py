from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

def nb_minitab(couts):
    x = []
    for cout in couts:
        for val in cout:
            if val > 0:
                x.append(val)
    return min(x) if x else float('inf')

def find_cycle(basic_cells, new_cell, m, n):
    """Trouve un cycle fermé pour la cellule d'entrée (new_cell), en tenant compte des ε."""
    cycle = [new_cell]
    visited = set([(new_cell[0], new_cell[1])])
    direction = 'row'

    while True:
        last = cycle[-1]
        i, j = last
        found = False

        if direction == 'row':
            for col in range(n):
                if (i, col) in basic_cells and (i, col) not in visited and (i, col) != last:
                    cycle.append((i, col))
                    visited.add((i, col))
                    direction = 'col'
                    found = True
                    break
        else:
            for row in range(m):
                if (row, j) in basic_cells and (row, j) not in visited and (row, j) != last:
                    cycle.append((row, j))
                    visited.add((row, j))
                    direction = 'row'
                    found = True
                    break

        if not found:
            cycle.pop()
            if not cycle:
                return None
            direction = 'col' if direction == 'row' else 'row'
            continue

        if len(cycle) > 2 and (cycle[-1][0], new_cell[1]) in basic_cells:
            cycle.append((cycle[-1][0], new_cell[1]))
            return cycle
        if len(cycle) > 2 and (new_cell[0], cycle[-1][1]) in basic_cells:
            cycle.append((new_cell[0], cycle[-1][1]))
            return cycle

def Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients, tableau_primary):
    if sum(quantite_demande) != sum(quantite_stocke):
        return f'Erreur : La quantité demandée ({sum(quantite_demande)}) et stockée ({sum(quantite_stocke)}) doivent être égales.'

    m, n = len(couts), len(couts[0])
    tableau_minitab = [[0] * n for _ in range(m)]
    quantite_stocke = quantite_stocke.copy()
    quantite_demande = quantite_demande.copy()
    couts1 = [row[:] for row in couts]
    basic_cells = []

    # Étape 1 : Solution initiale (méthode du moindre coût)
    print("\nConstruction de la solution initiale (méthode du moindre coût) :")
    while sum(quantite_stocke) > 0 and sum(quantite_demande) > 0:
        min_cost = nb_minitab(couts1)
        if min_cost == float('inf'):
            break
        indices = []
        for i in range(m):
            for j in range(n):
                if couts1[i][j] == min_cost and quantite_stocke[i] > 0 and quantite_demande[j] > 0:
                    indices.append((i, j))
        if not indices:
            break
        i, j = indices[0]  # Choisir la première occurrence valide
        qty = min(quantite_stocke[i], quantite_demande[j])
        tableau_minitab[i][j] = qty
        basic_cells.append((i, j))
        quantite_stocke[i] -= qty
        quantite_demande[j] -= qty
        print(f"Allocation : {qty} de {entrepots[i]} à {clients[j]} (coût = {couts[i][j]})")
        print(f"Offre restante : {quantite_stocke}")
        print(f"Demande restante : {quantite_demande}")
        if quantite_stocke[i] == 0:
            for col in range(n):
                couts1[i][col] = float('inf')
        if quantite_demande[j] == 0:
            for row in range(m):
                couts1[row][j] = float('inf')

    # Gérer le cas dégénéré : ajouter une allocation ε si nécessaire
    expected_basic_cells = m + n - 1
    if len(basic_cells) < expected_basic_cells:
        # Trouver une cellule non de base avec coût minimum pour ajouter ε
        min_cost = float('inf')
        epsilon_cell = None
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic_cells and tableau_minitab[i][j] == 0 and couts[i][j] < min_cost:
                    min_cost = couts[i][j]
                    epsilon_cell = (i, j)
        if epsilon_cell:
            basic_cells.append(epsilon_cell)
            tableau_minitab[epsilon_cell[0]][epsilon_cell[1]] = 'ε'
            print(f"Ajout d'une allocation ε à {entrepots[epsilon_cell[0]]} vers {clients[epsilon_cell[1]]} (coût = {couts[epsilon_cell[0]][epsilon_cell[1]]})")

    # Sauvegarder la solution initiale
    solutions = [{
        'solution_base': sum(couts[i][j] * (tableau_minitab[i][j] if isinstance(tableau_minitab[i][j], (int, float)) else 0) for i in range(m) for j in range(n)),
        'tableau': [row[:] for row in tableau_minitab],
        'direction_client': [(entrepots[i], clients[j]) for i, j in basic_cells],
        'negative_gains': []  # Pas de gains négatifs à l'initialisation
    }]

    # Afficher la solution initiale
    print("\nPremier tableau_minitab (solution initiale) :")
    for row in tableau_minitab:
        print(row)
    print(f"Coût initial : {solutions[0]['solution_base']}")
    print(f"Cellules de base : {solutions[0]['direction_client']}")

    # Étape 2 : Algorithme du Stepping Stone
    iteration = 1
    while True:
        print(f"\n--- Itération {iteration} du Stepping Stone ---")
        # Calcul des potentiels vx et vy
        vx = [None] * m
        vy = [None] * n
        vx[0] = 0
        equations = [(i, j) for i, j in basic_cells]
        while None in vx or None in vy:
            for i, j in equations:
                if vx[i] is not None and vy[j] is None:
                    vy[j] = couts[i][j] - vx[i]
                elif vy[j] is not None and vx[i] is None:
                    vx[i] = couts[i][j] - vy[j]
        print(f"Potentiels vx : {vx}")
        print(f"Potentiels vy : {vy}")

        # Calcul des gains pour les cellules non dans la base
        posNegGains = []
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic_cells and tableau_minitab[i][j] == 0:
                    gain = couts[i][j] - (vx[i] + vy[j])
                    posNegGains.append((gain, (i, j)))
        print(f"Gains potentiels : {[(f'({entrepots[i]}, {clients[j]})={gain}', (i, j)) for gain, (i, j) in posNegGains]}")

        # Sauvegarder les gains négatifs
        negative_gains = [(gain, entrepots[i], clients[j]) for gain, (i, j) in posNegGains if gain < 0]
        print(f"Gains négatifs : {negative_gains}")

        # Vérifier l'optimalité sans négatif
        if not posNegGains or all(gain >= 0 for gain, _ in posNegGains):
            print("Solution optimale trouvée (tous les gains sont positifs ou nuls).")
            break

        # Sélectionner la cellule avec le gain négatif le plus important
        min_gain, (new_i, new_j) = min(posNegGains, key=lambda x: x[0])
        print(f"Cellule choisie : ({entrepots[new_i]}, {clients[new_j]}) avec gain = {min_gain}")

        # Trouver le cycle fermé
        cycle = find_cycle(basic_cells, (new_i, new_j), m, n)
        if not cycle:
            print("Erreur : Aucun cycle fermé trouvé.")
            break
        print(f"Cycle fermé : {[(entrepots[i], clients[j]) for i, j in cycle]}")

        # Identifier les quantités à ajuster (ignorer ε pour min_qty)
        cycle_indices = cycle + [cycle[0]]
        min_qty = float('inf')
        for k in range(1, len(cycle_indices), 2):
            i, j = cycle_indices[k]
            val = tableau_minitab[i][j]
            if isinstance(val, (int, float)):
                min_qty = min(min_qty, val)
        print(f"Quantité minimale à ajuster : {min_qty}")

        # Ajuster les quantités dans le cycle
        for k in range(len(cycle_indices) - 1):
            i, j = cycle_indices[k]
            val = tableau_minitab[i][j]
            if val == 'ε':
                val = 0
            if k % 2 == 0:
                new_val = val + min_qty
            else:
                new_val = val - min_qty
            if new_val < 0:
                new_val = 0
            tableau_minitab[i][j] = new_val

        # Mettre à jour la base
        basic_cells.append((new_i, new_j))
        for i, j in basic_cells[:]:
            if tableau_minitab[i][j] == 0 or tableau_minitab[i][j] == 'ε':
                basic_cells.remove((i, j))

        # Sauvegarder la solution après chaque itération avec les gains négatifs
        solutions.append({
            'solution_base': sum(couts[i][j] * (tableau_minitab[i][j] if isinstance(tableau_minitab[i][j], (int, float)) else 0) for i in range(m) for j in range(n)),
            'tableau': [row[:] for row in tableau_minitab],
            'direction_client': [(entrepots[i], clients[j]) for i, j in basic_cells],
            'negative_gains': negative_gains
        })

        # Recalculer le coût
        solution_base = sum(couts[i][j] * (tableau_minitab[i][j] if isinstance(tableau_minitab[i][j], (int, float)) else 0) for i in range(m) for j in range(n))
        print(f"Nouveau tableau_minitab :")
        for row in tableau_minitab:
            print(row)
        print(f"Nouveau coût : {solution_base}")
        print(f"Nouvelles cellules de base : {[(entrepots[i], clients[j]) for i, j in basic_cells]}")
        iteration += 1

    # Afficher le tableau final
    print("\nTableau final (solution optimale) :")
    for i, row in enumerate(solutions[-1]['tableau']):
        print(f"{entrepots[i]}: {row}")
    print(f"Coût total final : {solutions[-1]['solution_base']}")

    return solutions

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        
        # Validation des données
        if not all(isinstance(x, str) and x.strip() for x in data['tableEntrepots']):
            return jsonify({'error': 'Tous les entrepôts doivent être des chaînes non vides.'}), 400
        if not all(isinstance(x, str) and x.strip() for x in data['tableClients']):
            return jsonify({'error': 'Tous les clients doivent être des chaînes non vides.'}), 400
        try:
            costs = [[int(x) for x in row] for row in data['tableCouts']]
            if any(x < 0 for row in costs for x in row):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Tous les coûts doivent être des nombres entiers positifs.'}), 400
        try:
            demand = [int(x) for x in data['tableQuantiteDemande']]
            if any(x <= 0 for x in demand):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Toutes les quantités demandées doivent être des nombres entiers positifs.'}), 400
        try:
            supply = [int(x) for x in data['tableQuantiteStocke']]
            if any(x <= 0 for x in supply):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Toutes les quantités stockées doivent être des nombres entiers positifs.'}), 400
        
        if sum(supply) != sum(demand):
            return jsonify({'error': 'La somme des quantités stockées doit être égale à la somme des quantités demandées.'}), 400
        
        entrepots = data['tableEntrepots']
        clients = data['tableClients']
        quantite_demande = demand
        quantite_stocke = supply
        couts = costs
        
        result = Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients, couts)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)