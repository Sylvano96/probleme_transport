from flask import Flask, request, jsonify
from flask_cors import CORS
import copy


app = Flask(__name__)
CORS(app)


def nb_minitab(couts):
    """
    Trouve la valeur minimale non nulle dans la matrice des coûts.
    """
    x = []
    for cout_row in couts:
        for val in cout_row:
            if val > 0:
                x.append(val)
    if not x:
        return float('inf') 
    nb_mini_tab = min(x)
    return nb_mini_tab

def Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients):
   
    couts = [[int(c) for c in row] for row in couts]
    quantite_demande = [int(q) for q in quantite_demande]
    quantite_stocke = [int(q) for q in quantite_stocke]

    if sum(quantite_demande) != sum(quantite_stocke):
        return 'La somme des quantités demandées et stockées doit être égale.'

    initial_couts = [row[:] for row in couts] 
    
    tab = [[0 for _ in range(len(clients))] for _ in range(len(entrepots))]

    current_couts = [row[:] for row in couts] 
    current_quantite_demande = quantite_demande[:]
    current_quantite_stocke = quantite_stocke[:]

    while sum(current_quantite_stocke) > 0 and sum(current_quantite_demande) > 0:
        min_val = float('inf')
        min_coords = []

        for i in range(len(current_couts)):
            for j in range(len(current_couts[i])):
                if current_couts[i][j] > 0 and current_quantite_stocke[i] > 0 and current_quantite_demande[j] > 0:
                    if current_couts[i][j] < min_val:
                        min_val = current_couts[i][j]
                        min_coords = [[i, j]]
                    elif current_couts[i][j] == min_val:
                        min_coords.append([i, j])
        
        if not min_coords: 
            break

        i, j = min_coords[0]

        transfer_amount = min(current_quantite_stocke[i], current_quantite_demande[j])
        
        tab[i][j] = transfer_amount
        current_quantite_stocke[i] -= transfer_amount
        current_quantite_demande[j] -= transfer_amount

        if current_quantite_stocke[i] == 0:
            for col in range(len(current_couts[i])):
                current_couts[i][col] = 0 
        
        if current_quantite_demande[j] == 0:
            for row in range(len(current_couts)):
                current_couts[row][j] = 0 

    solution_base_cost = 0
    for i in range(len(initial_couts)):
        for j in range(len(initial_couts[i])):
            solution_base_cost += initial_couts[i][j] * tab[i][j]
    
    initial_assignments = []
    for r_idx, row in enumerate(tab):
        for c_idx, val in enumerate(row):
            if val > 0:
                initial_assignments.append({'source': entrepots[r_idx], 'destination': clients[c_idx], 'amount': val})

    values = {
        'solution_base_cost': solution_base_cost,
        'solution_table': tab,
        'initial_assignments': initial_assignments
    }
    return values


def find_closed_loop(start_row, start_col, basic_cells, num_rows, num_cols):
    temp_basic_cells = set(basic_cells) 
    
    queue = [(start_row, start_col, [(start_row, start_col)])]
    visited_states = set() 
    
    while queue:
        r, c, path = queue.pop(0)

        path_tuple = tuple(path)
        if (r, c, path_tuple) in visited_states:
            continue
        visited_states.add((r, c, path_tuple))

        for next_c in range(num_cols):
            if next_c == c: continue 
            
            if (r, next_c) in temp_basic_cells or (r, next_c) == (start_row, start_col):
                if len(path) >= 2 and path[-2] == (r, next_c): 
                    continue

                new_path = path + [(r, next_c)]
                
                if (r, next_c) == (start_row, start_col) and len(new_path) >= 5: 
                    return new_path[:-1] 

                queue.append((r, next_c, new_path))
    
        for next_r in range(num_rows):
            if next_r == r: continue 
            if (next_r, c) in temp_basic_cells or (next_r, c) == (start_row, start_col):
                if len(path) >= 2 and path[-2] == (next_r, c): 
                    continue

                new_path = path + [(next_r, c)]
                
                if (next_r, c) == (start_row, start_col) and len(new_path) >= 5:
                    return new_path[:-1]

                queue.append((next_r, c, new_path))
    
    return None 


def Stepping_Stone(costs, solution_table, entrepots, clients):
    
    num_rows = len(costs)
    num_cols = len(costs[0])

    solution_table = [[int(x) for x in row] for row in solution_table]
    costs = [[int(x) for x in row] for row in costs]

    while True:
        basic_cells = set()
        for r in range(num_rows):
            for c in range(num_cols):
                if solution_table[r][c] > 0:
                    basic_cells.add((r, c))

        non_basic_cells = []
        for r in range(num_rows):
            for c in range(num_cols):
                if (r, c) not in basic_cells:
                    non_basic_cells.append((r, c))

        penalties = {}
        most_negative_penalty = 0 
        most_negative_cell = None

        for r_nb, c_nb in non_basic_cells:
            path = find_closed_loop(r_nb, c_nb, basic_cells, num_rows, num_cols)
            
            if path:
                penalty = 0
                for i, (r_p, c_p) in enumerate(path):
                    sign = 1 if i % 2 == 0 else -1 
                    penalty += sign * costs[r_p][c_p]
                
                penalties[(r_nb, c_nb)] = penalty
                if penalty < most_negative_penalty:
                    most_negative_penalty = penalty
                    most_negative_cell = (r_nb, c_nb)
        
        if most_negative_penalty >= 0:
            break 

        pivot_r, pivot_c = most_negative_cell
        path_to_adjust = find_closed_loop(pivot_r, pivot_c, basic_cells, num_rows, num_cols)

        if not path_to_adjust:
            print(f"Attention: Aucun chemin fermé trouvé pour la cellule pivot {pivot_cell}. "
                  "L'optimisation pourrait être incomplète ou nécessiter une recherche de chemin plus complexe. "
                  "Sortie de la boucle d'optimisation.")
            break

        min_transfer_amount = float('inf')
        for i, (r_p, c_p) in enumerate(path_to_adjust):
            if i % 2 != 0: 
                min_transfer_amount = min(min_transfer_amount, solution_table[r_p][c_p])
        
        for i, (r_p, c_p) in enumerate(path_to_adjust):
            if i % 2 == 0: 
                solution_table[r_p][c_p] += min_transfer_amount
            else: 
                solution_table[r_p][c_p] -= min_transfer_amount
        
        for r in range(num_rows):
            for c in range(num_cols):
                if solution_table[r][c] < 0.001: 
                    solution_table[r][c] = 0
    optimal_cost = 0
    final_assignments = []
    for r in range(num_rows):
        for c in range(num_cols):
            optimal_cost += costs[r][c] * solution_table[r][c]
            if solution_table[r][c] > 0:
                final_assignments.append({'source': entrepots[r], 'destination': clients[c], 'amount': solution_table[r][c]})

    return {
        'optimal_cost': optimal_cost,
        'optimal_solution_table': solution_table,
        'final_assignments': final_assignments
    }


@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json

        if not all(isinstance(x, str) and x.strip() for x in data['tableEntrepots']):
            return jsonify({'error': 'Tous les entrepôts doivent être des chaînes non vides.'}), 400
        if not all(isinstance(x, str) and x.strip() for x in data['tableClients']):
            return jsonify({'error': 'Tous les clients doivent être des chaînes non vides.'}), 400
        
        try:
            costs_input = [[int(x) for x in row] for row in data['tableCouts']]
            if any(x < 0 for row in costs_input for x in row):
                raise ValueError("Les coûts doivent être des nombres entiers positifs.")
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Tous les coûts doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
        try:
            demand_input = [int(x) for x in data['tableQuantiteDemande']]
            if any(x <= 0 for x in demand_input):
                raise ValueError("Toutes les quantités demandées doivent être des nombres entiers positifs.")
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Toutes les quantités demandées doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
        try:
            supply_input = [int(x) for x in data['tableQuantiteStocke']]
            if any(x <= 0 for x in supply_input):
                raise ValueError("Toutes les quantités stockées doivent être des nombres entiers positifs.")
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Toutes les quantités stockées doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
        if sum(supply_input) != sum(demand_input):
            return jsonify({'error': 'La somme des quantités stockées doit être égale à la somme des quantités demandées.'}), 400
        
        entrepots = data['tableEntrepots']
        clients = data['tableClients']
        
        minitab_result = Mini_tab(costs_input, demand_input, supply_input, entrepots, clients)

        if isinstance(minitab_result, str): 
            return jsonify({'error': minitab_result}), 400

        initial_solution_table = [row[:] for row in minitab_result['solution_table']] 
        initial_solution_result = {
            'initial_assignments' : minitab_result["initial_assignments"],
            'solution_base_cost' : minitab_result["solution_base_cost"],
            'solution_table' : minitab_result["solution_table"],
        }

        stepping_stone_result = Stepping_Stone(costs_input, initial_solution_table, entrepots, clients)

        return jsonify(initial_solution_result, stepping_stone_result)
    
    except Exception as e:
        print(f"Erreur serveur: {str(e)}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500
    

if __name__ == '__main__':
    
    # Esorina fotsiny ny commentaire raha raha te hi teste ilay application.
    # If it's work, don't touch this code 

    #****************************************************************************************************************
    #
    # example_couts = [
    #     [24, 22, 61, 49, 83, 35], 
    #      [23, 39, 78, 28, 65, 42], 
    #      [67, 56, 92, 24, 53, 54], 
    #      [71, 43, 91, 67, 40, 49]
    # ]
    # example_entrepots = ['A', 'B', 'C', 'D']
    # example_clients = ['1', '2', '3', '4', '5', '6']
    # example_quantite_stocke = [18, 32, 14, 9]
    # example_quantite_demande = [9, 11, 28, 6, 14, 5]

    # print("--- Calcul de la solution initiale (Méthode du Coût Minimum) ---")
    # initial_sol = Mini_tab(
    #     copy.deepcopy(example_couts),
    #     example_quantite_demande, 
    #     example_quantite_stocke, 
    #     example_entrepots, 
    #     example_clients
    # )
    # if isinstance(initial_sol, str):
    #     print(f"Erreur lors du calcul de la solution initiale: {initial_sol}")
    # else:
    #     print(f"Coût de la solution initiale: {initial_sol['solution_base_cost']}")
    #     print("Tableau d'allocation initial:")
    #     for row in initial_sol['solution_table']:
    #         print(row)
    #     print("\n--- Application de l'algorithme Stepping Stone ---")
        

    #     optimal_sol = Stepping_Stone(
    #         example_couts, 
    #         copy.deepcopy(initial_sol['solution_table']), 
    #         example_entrepots, 
    #         example_clients
    #     )
    #     print(f"Coût de la solution optimale: {optimal_sol['optimal_cost']}")
    #     print("Tableau d'allocation optimal:")
    #     for row in optimal_sol['optimal_solution_table']:
    #         print(row)
    #     print("\n--- Fin de l'exemple ---")
    #
    # *********************************************************************************************************
    app.run(debug=True)
