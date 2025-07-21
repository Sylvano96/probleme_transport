#  ************************   First Code without algo Stepping Stone (Test)   ****************************

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# couts = [
#     [45, 60, 45, 30, 45, 50],
#     [35, 15, 35, 35, 25, 25],
#     [30, 25, 45, 55, 15, 55],
#     [30, 40, 55, 10, 10, 50]
# ]

# entrepots = ['A', 'B', 'C', 'D']
# clients = ['1', '2', '3', '4', '5', '6']
# quantite_stocke = [25, 10, 30, 45]
# quantite_demande = [20, 15, 35, 10, 20, 10]


# couts = [
#          [24, 22, 61, 49, 83, 35], 
#          [23, 39, 78, 28, 65, 42], 
#          [67, 56, 92, 24, 53, 54], 
#          [71, 43, 91, 67, 40, 49]
#]

# entrepots = ['A', 'B', 'C', 'D']

# clients = ['1', '2', '3', '4', '5', '6']

# quantite_stocke = [18, 32, 14, 9]
# quantite_demande = [9, 11, 28, 6, 14, 5]

# couts1 = couts
#***************************************************************
# couts = [
#     [9, 12, 9, 6, 9, 10],
#     [7, 3, 7, 7, 5, 5],
#     [6, 5, 9, 11, 3, 11],
#     [6, 8, 11, 2, 2, 10]
# ]
# entrepots = ['A', 'B', 'C', 'D']
# clients = ['1', '2', '3', '4', '5', '6']
# quantite_stocke = [50, 60, 20, 90]
# quantite_demande = [40, 30, 70, 20, 40, 20]

def nb_minitab(couts) :
    x = []
    for cout in couts:
        for i in range(len(cout)):
            if cout[i] > 0:
                x.append(cout[i])
    
    nb_mini_tab = min(x)
    return nb_mini_tab

def Mini_tab(couts,quantite_demande, quantite_stocke, entrepots, clients):
    print(couts)
    tab = []
    if sum(quantite_demande) == sum(quantite_stocke):
        couts1 = couts
        indices = []
        tab = []
        y = []
        for i in range(len(couts1)):
            a = []
            for j in range(len(couts1[i])):
                a.append(couts1[i][j])
            y.append(a)



        for i in range(len(quantite_demande)):
            for j in range(len(quantite_stocke)):
                while (sum(quantite_stocke) != 0 and sum(quantite_demande)!=0):
                    for i in range(len(couts1)):
                        a = []
                        for j in range(len(couts1[i])):
                            a.append(0)
                        
                        tab.append(a)

                    indices = []
                    for i in range(len(couts1)):
                        for j in range(len(couts1[i])):
                            if couts[i][j] == nb_minitab(couts1):
                                indices.append([i, j])
                    if quantite_demande[indices[0][1]] > quantite_stocke[indices[0][0]] :
                        tab[indices[0][0]][indices[0][1]] = quantite_stocke[indices[0][0]]
                        quantite_demande[indices[0][1]] = quantite_demande[indices[0][1]]  - quantite_stocke[indices[0][0]] 
                        quantite_stocke[indices[0][0]] = 0

                        for i in range(len(couts1)):
                            for j in range(len(couts1[i])):
                                couts1[indices[0][0]][j] = 0


                    else :
                        tab[indices[0][0]][indices[0][1]] = quantite_demande[indices[0][1]]
                        quantite_stocke[indices[0][0]] = quantite_stocke[indices[0][0]]  - quantite_demande[indices[0][1]] 
                        quantite_demande[indices[0][1]] = 0

                        for i in range(len(couts1)):
                            for j in range(len(couts1[i])):
                                couts1[i][indices[0][1]] = 0

        x = []

        for i in range(len(quantite_stocke)) :
            x.append(tab[i])
        
        solution_base = 0
        tab_val=[]

        for i in range(len(couts)):
            for j in range(len(couts[i])):
                if x[i][j] > 0:
                    # print(f"calcul de {y[i][j]} et {x[i][j]} : {y[i][j] * x[i][j]}")
                    tab_val.append(y[i][j] * x[i][j])  
        solution_base=sum(tab_val)

        tableau = []

        for i in range(len(entrepots)):
            for j in range(len(x)):
                for k in range(len(x[j])):
                    if i == j :
                        if x[j][k] > 0:
                            tableau.append([entrepots[i], clients[k]])

        values = {
            'solution_base' : solution_base,
            'tableau' : x,
            'direction_client' : tableau,
        }        

        return values
    else:
        return 'la quantité demandé et la quantité stocké doivent être de la même somme ....'

    

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
        quantite_demande = data['tableQuantiteDemande']
        quantite_stocke = data['tableQuantiteStocke']
        couts = data['tableCouts']
        
        return jsonify(Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients))
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500
    

if __name__ == '__main__':
    app.run(debug=True)






#      ***************************   Second code with algo Stepping Stone (Test)   *****************************

from flask import Flask, request, jsonify
from flask_cors import CORS
import math

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
        return float('inf') # Retourne l'infini si tous les coûts sont nuls ou négatifs
    nb_mini_tab = min(x)
    return nb_mini_tab

def Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients):
    """
    Implémente la méthode du coût minimal pour trouver une solution de base initiale.
    """
    # Convertir les coûts, quantités demandées et stockées en entiers
    couts = [[int(c) for c in row] for row in couts]
    quantite_demande = [int(q) for q in quantite_demande]
    quantite_stocke = [int(q) for q in quantite_stocke]

    if sum(quantite_demande) != sum(quantite_stocke):
        return 'La somme des quantités demandées et stockées doit être égale.'

    initial_couts = [row[:] for row in couts] # Copie des coûts initiaux pour le calcul final
    
    # Initialiser le tableau de la solution de base avec des zéros
    tab = [[0 for _ in range(len(clients))] for _ in range(len(entrepots))]

    current_couts = [row[:] for row in couts] # Copie des coûts pour les modifications pendant l'algorithme

    # Créer des copies modifiables des quantités
    current_quantite_demande = quantite_demande[:]
    current_quantite_stocke = quantite_stocke[:]

    while sum(current_quantite_stocke) > 0 and sum(current_quantite_demande) > 0:
        min_val = float('inf')
        min_coords = []

        # Trouver le coût minimal actuel (non-zéro) et ses coordonnées
        for i in range(len(current_couts)):
            for j in range(len(current_couts[i])):
                if current_couts[i][j] > 0 and current_couts[i][j] < min_val:
                    min_val = current_couts[i][j]
                    min_coords = [[i, j]]
                elif current_couts[i][j] == min_val:
                    min_coords.append([i, j])
        
        if not min_coords: # Plus de coûts positifs à considérer
            break

        # Utiliser la première coordonnée minimale trouvée (peut être amélioré pour gérer les ex aequo)
        i, j = min_coords[0]

        transfer_amount = min(current_quantite_stocke[i], current_quantite_demande[j])
        
        tab[i][j] = transfer_amount
        current_quantite_stocke[i] -= transfer_amount
        current_quantite_demande[j] -= transfer_amount

        # Mettre à zéro les lignes ou colonnes satisfaites
        if current_quantite_stocke[i] == 0:
            for col in range(len(current_couts[i])):
                current_couts[i][col] = 0 # Marque la ligne comme non disponible
        
        if current_quantite_demande[j] == 0:
            for row in range(len(current_couts)):
                current_couts[row][j] = 0 # Marque la colonne comme non disponible

    solution_base_cost = 0
    for i in range(len(initial_couts)):
        for j in range(len(initial_couts[i])):
            solution_base_cost += initial_couts[i][j] * tab[i][j]
    
    # Préparer la liste des affectations initiales pour l'étape suivante
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


def find_path(start_row, start_col, basic_cells, visited, path):
    """
    Trouve un chemin fermé à partir d'une cellule non basique en utilisant les cellules basiques.
    """
    visited[start_row][start_col] = True
    path.append((start_row, start_col))

    # Trouver la dernière cellule ajoutée au chemin
    current_row, current_col = path[-1]

    # Essayer de se déplacer horizontalement
    for col in range(len(visited[0])):
        if (current_row, col) in basic_cells and not visited[current_row][col] and col != current_col:
            if find_path(current_row, col, basic_cells, visited, path):
                return True

    # Essayer de se déplacer verticalement
    for row in range(len(visited)):
        if (row, current_col) in basic_cells and not visited[row][current_col] and row != current_row:
            if find_path(row, current_col, basic_cells, visited, path):
                return True
    
    # Vérifier si on a un cycle (retour au début avec au moins 4 cellules)
    if len(path) >= 4 and path[0][0] == current_row and path[0][1] == current_col:
        return True

    path.pop() # Retirer la cellule si aucun chemin n'est trouvé
    return False


def get_cycle(start_row, start_col, basic_cells, num_rows, num_cols):
    """
    Tente de trouver un cycle fermé pour une cellule non basique donnée.
    Retourne le cycle sous forme de liste de (ligne, colonne).
    """
    # Créer un graphe à partir des cellules basiques
    adj = { (r, c): [] for r, c in basic_cells }
    for r, c in basic_cells:
        # Voisins horizontaux
        for nc in range(num_cols):
            if nc != c and (r, nc) in basic_cells:
                adj[(r, c)].append((r, nc))
        # Voisins verticaux
        for nr in range(num_rows):
            if nr != r and (nr, c) in basic_cells:
                adj[(r, c)].append((nr, c))
    
    # Ajouter la cellule non basique au graphe pour trouver le cycle
    adj[(start_row, start_col)] = []
    # Voisins horizontaux de la cellule non basique
    for nc in range(num_cols):
        if nc != start_col and (start_row, nc) in basic_cells:
            adj[(start_row, start_col)].append((start_row, nc))
            adj[(start_row, nc)].append((start_row, start_col)) # Ajouter aussi le lien inverse
    # Voisins verticaux de la cellule non basique
    for nr in range(num_rows):
        if nr != start_row and (nr, start_col) in basic_cells:
            adj[(start_row, start_col)].append((nr, start_col))
            adj[(nr, start_col)].append((nr, start_col)) # Ajouter aussi le lien inverse

    
    # Utiliser un BFS ou DFS pour trouver un cycle
    queue = [(start_row, start_col, [(start_row, start_col)])]
    visited_paths = set()
    
    while queue:
        r, c, current_path = queue.pop(0)

        # Si le chemin actuel est déjà visité, continuer
        path_tuple = tuple(current_path)
        if path_tuple in visited_paths:
            continue
        visited_paths.add(path_tuple)

        for neighbor_r, neighbor_c in adj.get((r,c), []):
            if (neighbor_r, neighbor_c) == start_path[0] and len(current_path) >= 4:
                return current_path + [(neighbor_r, neighbor_c)] # Cycle trouvé
            
            if (neighbor_r, neighbor_c) not in current_path: # Eviter les boucles immédiates
                queue.append((neighbor_r, neighbor_c, current_path + [(neighbor_r, neighbor_c)]))
    
    return None # Pas de cycle trouvé


def find_closed_path_dfs(r_start, c_start, current_path, visited, basic_cells, num_rows, num_cols):
    """
    Fonction récursive DFS pour trouver un chemin fermé à partir de (r_start, c_start).
    """
    current_path.append((r_start, c_start))
    visited[r_start][c_start] = True

    # Vérifier si on a un cycle (plus de 4 cellules et retour au point de départ)
    if len(current_path) > 1 and current_path[-1] == current_path[0] :
        # Le cycle doit alterner entre mouvements horizontaux et verticaux
        # et ne pas avoir de "zigzag" immédiat (ex: A-B-A)
        if len(current_path) >= 4: # Un cycle doit avoir au moins 4 sommets
            # Vérifier l'alternance des mouvements (horiz/vert)
            is_valid_cycle = True
            for i in range(len(current_path) - 1):
                r1, c1 = current_path[i]
                r2, c2 = current_path[i+1]
                if i % 2 == 0: # Mouvement horizontal
                    if r1 != r2:
                        is_valid_cycle = False
                        break
                else: # Mouvement vertical
                    if c1 != c2:
                        is_valid_cycle = False
                        break
            if is_valid_cycle:
                 # Vérifier qu'il n'y a pas de répétition immédiate des deux dernières cellules
                if len(current_path) >= 3:
                    if current_path[-1] == current_path[-3]:
                        is_valid_cycle = False
                
                # S'assurer que le chemin est simple (pas de self-intersections, sauf au début/fin)
                # On ne veut pas de chemins comme A-B-C-B-A
                if len(set(current_path[:-1])) < len(current_path) - 1: # Si des cellules sont répétées avant la fin
                    is_valid_cycle = False

            if is_valid_cycle:
                return current_path

    # Essayer de se déplacer horizontalement
    for c_next in range(num_cols):
        if c_next == c_start: continue
        if (r_start, c_next) in basic_cells and not visited[r_start][c_next]:
            path = find_closed_path_dfs(r_start, c_next, current_path, visited, basic_cells, num_rows, num_cols)
            if path:
                return path

    # Essayer de se déplacer verticalement
    for r_next in range(num_rows):
        if r_next == r_start: continue
        if (r_next, c_start) in basic_cells and not visited[r_next][c_start]:
            path = find_closed_path_dfs(r_next, c_start, current_path, visited, basic_cells, num_rows, num_cols)
            if path:
                return path

    current_path.pop()
    visited[r_start][c_start] = False
    return None

def find_closed_loop(start_row, start_col, basic_cells, num_rows, num_cols):
    """
    Trouve un cycle fermé unique pour une cellule non basique.
    """
    # Exclure la cellule de départ des cellules basiques pour la recherche initiale
    temp_basic_cells = set(basic_cells)
    
    # Un dictionnaire pour stocker les chemins possibles et les "parents" pour reconstruire le chemin
    parent_map = {}
    
    # Utiliser une file pour BFS
    queue = [(start_row, start_col, [(start_row, start_col)])] # (row, col, path_so_far)
    
    # Empêche les cycles immédiats
    visited_states = set() 
    
    while queue:
        r, c, path = queue.pop(0)

        # Marquer ce point comme visité pour ce chemin
        if (r, c, tuple(path)) in visited_states:
            continue
        visited_states.add((r, c, tuple(path)))

        # Voisins horizontaux
        for next_c in range(num_cols):
            if next_c == c: continue
            if (r, next_c) in temp_basic_cells or (r, next_c) == (start_row, start_col): # Peut passer par la cellule de départ
                if len(path) >= 2 and path[-2][0] == r and path[-2][1] == next_c: # Éviter de revenir en arrière
                    continue
                new_path = path + [(r, next_c)]
                if (r, next_c) == (start_row, start_col) and len(new_path) >= 5: # Au moins 4 cellules dans le cycle
                    return new_path[:-1] # Retourne le cycle sans la répétition du point de départ

                queue.append((r, next_c, new_path))
        
        # Voisins verticaux
        for next_r in range(num_rows):
            if next_r == r: continue
            if (next_r, c) in temp_basic_cells or (next_r, c) == (start_row, start_col):
                if len(path) >= 2 and path[-2][1] == c and path[-2][0] == next_r: # Éviter de revenir en arrière
                    continue
                new_path = path + [(next_r, c)]
                if (next_r, c) == (start_row, start_col) and len(new_path) >= 5:
                    return new_path[:-1]

                queue.append((next_r, c, new_path))
    
    return None


def Stepping_Stone(costs, solution_table, entrepots, clients):
    """
    Implémente l'algorithme de Stepping Stone pour trouver la solution optimale.
    """
    num_rows = len(costs)
    num_cols = len(costs[0])

    # Convertir la solution_table et les coûts en entiers
    solution_table = [[int(x) for x in row] for row in solution_table]
    costs = [[int(x) for x in row] for row in costs]

    while True:
        # 1. Identifier les cellules basiques (affectées)
        basic_cells = set()
        for r in range(num_rows):
            for c in range(num_cols):
                if solution_table[r][c] > 0:
                    basic_cells.add((r, c))

        # 2. Calculer les pénalités pour les cellules non basiques
        non_basic_cells = []
        for r in range(num_rows):
            for c in range(num_cols):
                if (r, c) not in basic_cells:
                    non_basic_cells.append((r, c))

        penalties = {}
        most_negative_penalty = 0
        most_negative_cell = None

        for r_nb, c_nb in non_basic_cells:
            # Trouver un chemin fermé pour chaque cellule non basique
            # Le chemin doit alterner entre cellules basiques et la cellule non basique,
            # et doit former un cycle fermé
            
            # Utilisation d'une version simplifiée ou d'une recherche plus robuste de cycle
            path = find_closed_loop(r_nb, c_nb, basic_cells, num_rows, num_cols)
            
            if path:
                penalty = 0
                for i, (r_p, c_p) in enumerate(path):
                    sign = 1 if i % 2 == 0 else -1 # Commence par + pour la cellule non basique
                    penalty += sign * costs[r_p][c_p]
                
                penalties[(r_nb, c_nb)] = penalty
                if penalty < most_negative_penalty:
                    most_negative_penalty = penalty
                    most_negative_cell = (r_nb, c_nb)
        
        # 3. Vérifier l'optimalité
        if most_negative_penalty >= 0:
            break # La solution est optimale

        # 4. Améliorer la solution
        pivot_r, pivot_c = most_negative_cell
        path_to_adjust = find_closed_loop(pivot_r, pivot_c, basic_cells, num_rows, num_cols)

        # Déterminer la plus petite quantité à soustraire
        min_transfer_amount = float('inf')
        for i, (r_p, c_p) in enumerate(path_to_adjust):
            if i % 2 != 0: # Cellules avec un signe négatif dans le cycle
                min_transfer_amount = min(min_transfer_amount, solution_table[r_p][c_p])
        
        # Ajuster les quantités dans le tableau de solution
        for i, (r_p, c_p) in enumerate(path_to_adjust):
            if i % 2 == 0: # Ajouter la quantité
                solution_table[r_p][c_p] += min_transfer_amount
            else: # Soustraire la quantité
                solution_table[r_p][c_p] -= min_transfer_amount
        
        # Nettoyer les cellules qui sont devenues nulles
        for r in range(num_rows):
            for c in range(num_cols):
                if solution_table[r][c] < 0.001: # Utiliser une petite tolérance pour les flottants
                    solution_table[r][c] = 0

    # Calculer le coût total optimal
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
        
        # Validation des données
        if not all(isinstance(x, str) and x.strip() for x in data['tableEntrepots']):
            return jsonify({'error': 'Tous les entrepôts doivent être des chaînes non vides.'}), 400
        if not all(isinstance(x, str) and x.strip() for x in data['tableClients']):
            return jsonify({'error': 'Tous les clients doivent être des chaînes non vides.'}), 400
        try:
            costs_input = [[int(x) for x in row] for row in data['tableCouts']]
            if any(x < 0 for row in costs_input for x in row):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Tous les coûts doivent être des nombres entiers positifs.'}), 400
        try:
            demand_input = [int(x) for x in data['tableQuantiteDemande']]
            if any(x <= 0 for x in demand_input):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Toutes les quantités demandées doivent être des nombres entiers positifs.'}), 400
        try:
            supply_input = [int(x) for x in data['tableQuantiteStocke']]
            if any(x <= 0 for x in supply_input):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Toutes les quantités stockées doivent être des nombres entiers positifs.'}), 400
        
        if sum(supply_input) != sum(demand_input):
            return jsonify({'error': 'La somme des quantités stockées doit être égale à la somme des quantités demandées.'}), 400
        
        entrepots = data['tableEntrepots']
        clients = data['tableClients']
        
        # Calcul de la solution de base en utilisant la méthode du coût minimal
        minitab_result = Mini_tab(costs_input, demand_input, supply_input, entrepots, clients)

        if isinstance(minitab_result, str): # Gérer les messages d'erreur de Mini_tab
            return jsonify({'error': minitab_result}), 400

        initial_solution_table = minitab_result['solution_table']
        initial_solution_result = {
            'initial_assignments' : minitab_result["initial_assignments"],
            'solution_base_cost' : minitab_result["solution_base_cost"],
            'solution_table' : minitab_result["solution_table"],
        }

        # Application de l'algorithme de Stepping Stone pour l'optimisation
        stepping_stone_result = Stepping_Stone(costs_input, initial_solution_table, entrepots, clients)
        
        return jsonify(initial_solution_result, stepping_stone_result)
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500
    

if __name__ == '__main__':
    app.run(debug=True)


#*******************************************************************************************************************
#***********************************   Third code with algo Stepping Stone   (Ampiasaina @ zao)     ************************************************
#*******************************************************************************************************************




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import copy
# import math # Ajouté car la fonction nb_minitab pourrait l'utiliser (bien que non utilisée dans Mini_tab principale)

# app = Flask(__name__)
# CORS(app)

# # La fonction nb_minitab n'est pas utilisée directement dans la nouvelle Mini_tab
# # mais est conservée si vous aviez l'intention de l'utiliser ailleurs ou pour référence.
# def nb_minitab(couts):
#     """
#     Trouve la valeur minimale non nulle dans la matrice des coûts.
#     """
#     x = []
#     for cout_row in couts:
#         for val in cout_row:
#             if val > 0:
#                 x.append(val)
#     if not x:
#         return float('inf') # Retourne l'infini si tous les coûts sont nuls ou négatifs
#     nb_mini_tab = min(x)
#     return nb_mini_tab

# def Mini_tab(couts, quantite_demande, quantite_stocke, entrepots, clients):
#     """
#     Implémente la méthode du coût minimal pour trouver une solution de base initiale.
#     """
#     # Convertir les coûts, quantités demandées et stockées en entiers
#     # S'assure que les entrées sont manipulables comme des nombres entiers.
#     couts = [[int(c) for c in row] for row in couts]
#     quantite_demande = [int(q) for q in quantite_demande]
#     quantite_stocke = [int(q) for q in quantite_stocke]

#     # Vérification de l'équilibre du problème de transport
#     if sum(quantite_demande) != sum(quantite_stocke):
#         return 'La somme des quantités demandées et stockées doit être égale.'

#     initial_couts = [row[:] for row in couts] # Copie des coûts initiaux pour le calcul final de la solution de base
    
#     # Initialiser le tableau de la solution de base (allocations) avec des zéros
#     tab = [[0 for _ in range(len(clients))] for _ in range(len(entrepots))]

#     # Copie modifiable des coûts pour marquer les lignes/colonnes épuisées
#     current_couts = [row[:] for row in couts] 

#     # Créer des copies modifiables des quantités pour le processus d'allocation
#     current_quantite_demande = quantite_demande[:]
#     current_quantite_stocke = quantite_stocke[:]

#     # Boucle principale de la méthode du coût minimum
#     while sum(current_quantite_stocke) > 0 and sum(current_quantite_demande) > 0:
#         min_val = float('inf')
#         min_coords = []

#         # Trouver le coût minimal actuel (non-zéro) parmi les cellules disponibles
#         for i in range(len(current_couts)):
#             for j in range(len(current_couts[i])):
#                 # S'assure que la cellule est disponible (coût > 0) et qu'il reste
#                 # de l'offre et de la demande pour cette ligne/colonne.
#                 if current_couts[i][j] > 0 and current_quantite_stocke[i] > 0 and current_quantite_demande[j] > 0:
#                     if current_couts[i][j] < min_val:
#                         min_val = current_couts[i][j]
#                         min_coords = [[i, j]]
#                     elif current_couts[i][j] == min_val:
#                         min_coords.append([i, j])
        
#         if not min_coords: # Si aucune cellule avec coût positif n'est trouvée (cas rare, fin de l'allocation)
#             break

#         # Choisir la première cellule avec le coût minimum pour l'allocation
#         i, j = min_coords[0]

#         # Allouer le minimum entre l'offre restante de l'entrepôt et la demande restante du client
#         transfer_amount = min(current_quantite_stocke[i], current_quantite_demande[j])
        
#         tab[i][j] = transfer_amount
#         current_quantite_stocke[i] -= transfer_amount
#         current_quantite_demande[j] -= transfer_amount

#         # Mettre à zéro (ou marquer comme non disponible) les lignes ou colonnes entièrement satisfaites
#         if current_quantite_stocke[i] == 0:
#             for col in range(len(current_couts[i])):
#                 current_couts[i][col] = 0 # Marque la ligne comme non disponible pour de futures allocations
        
#         if current_quantite_demande[j] == 0:
#             for row in range(len(current_couts)):
#                 current_couts[row][j] = 0 # Marque la colonne comme non disponible pour de futures allocations

#     solution_base_cost = 0
#     for i in range(len(initial_couts)):
#         for j in range(len(initial_couts[i])):
#             solution_base_cost += initial_couts[i][j] * tab[i][j]
    
#     # Préparer la liste des affectations initiales pour le retour de la fonction
#     initial_assignments = []
#     for r_idx, row in enumerate(tab):
#         for c_idx, val in enumerate(row):
#             if val > 0:
#                 initial_assignments.append({'source': entrepots[r_idx], 'destination': clients[c_idx], 'amount': val})

#     values = {
#         'solution_base_cost': solution_base_cost,
#         'solution_table': tab,
#         'initial_assignments': initial_assignments
#     }
#     return values

# # Fonctions auxiliaires pour Stepping Stone (recherche de chemin fermé)

# # La fonction find_path était une tentative, mais find_closed_loop est plus complète pour BFS.
# # Je la commente car elle n'est pas utilisée directement dans la version finale pour Stepping Stone.
# # def find_path(start_row, start_col, basic_cells, visited, path):
# #     # ... (code précédent de find_path) ...
# #     return None

# # La fonction get_cycle était une autre tentative de recherche de cycle,
# # mais find_closed_loop est celle qui sera utilisée pour l'implémentation finale.
# # def get_cycle(start_row, start_col, basic_cells, num_rows, num_cols):
# #     # ... (code précédent de get_cycle) ...
# #     return None

# # find_closed_path_dfs était une tentative DFS, mais BFS (find_closed_loop) est préférée ici.
# # def find_closed_path_dfs(r_start, c_start, current_path, visited, basic_cells, num_rows, num_cols):
# #     # ... (code précédent de find_closed_path_dfs) ...
# #     return None


# def find_closed_loop(start_row, start_col, basic_cells, num_rows, num_cols):
#     """
#     Trouve un cycle fermé unique pour une cellule non basique en utilisant une approche BFS.
#     Ce cycle est utilisé dans l'algorithme de Stepping Stone pour l'ajustement des allocations.
#     """
#     # Inclure la cellule de départ dans l'ensemble des "cellules potentielles" pour le chemin
#     # car elle est le point d'entrée du cycle.
#     temp_basic_cells = set(basic_cells) # Copie des cellules basiques
    
#     # File pour le parcours BFS: (ligne, colonne, chemin_actuel)
#     queue = [(start_row, start_col, [(start_row, start_col)])]
    
#     # Ensemble pour garder une trace des états visités afin d'éviter les boucles infinies et les chemins redondants.
#     # Un état est (ligne, colonne, tuple_du_chemin_actuel)
#     visited_states = set() 
    
#     while queue:
#         r, c, path = queue.pop(0)

#         # Si l'état actuel (cellule et chemin) a déjà été visité, on l'ignore.
#         path_tuple = tuple(path)
#         if (r, c, path_tuple) in visited_states:
#             continue
#         visited_states.add((r, c, path_tuple))

#         # Vérifier les mouvements horizontaux (dans la même ligne, différentes colonnes)
#         for next_c in range(num_cols):
#             if next_c == c: continue # Ne pas rester sur la même colonne
            
#             # Une cellule voisine est éligible si elle est une cellule basique OU si c'est la cellule de départ
#             if (r, next_c) in temp_basic_cells or (r, next_c) == (start_row, start_col):
#                 # Éviter de revenir immédiatement à la cellule précédente du chemin (zigzag)
#                 if len(path) >= 2 and path[-2] == (r, next_c): 
#                     continue

#                 new_path = path + [(r, next_c)]
                
#                 # Si le chemin est fermé (revient à la cellule de départ) et a une longueur suffisante (au moins 4 segments)
#                 if (r, next_c) == (start_row, start_col) and len(new_path) >= 5: # Au moins 4 cellules uniques dans le cycle (A-B-C-D-A)
#                     # Retourne le cycle sans la répétition du point de départ à la fin
#                     return new_path[:-1] 

#                 queue.append((r, next_c, new_path))
        
#         # Vérifier les mouvements verticaux (dans la même colonne, différentes lignes)
#         for next_r in range(num_rows):
#             if next_r == r: continue # Ne pas rester sur la même ligne
            
#             # Une cellule voisine est éligible si elle est une cellule basique OU si c'est la cellule de départ
#             if (next_r, c) in temp_basic_cells or (next_r, c) == (start_row, start_col):
#                 # Éviter de revenir immédiatement à la cellule précédente du chemin (zigzag)
#                 if len(path) >= 2 and path[-2] == (next_r, c): 
#                     continue

#                 new_path = path + [(next_r, c)]
                
#                 # Si le chemin est fermé et a une longueur suffisante
#                 if (next_r, c) == (start_row, start_col) and len(new_path) >= 5:
#                     return new_path[:-1]

#                 queue.append((next_r, c, new_path))
    
#     return None # Pas de cycle trouvé


# def Stepping_Stone(costs, solution_table, entrepots, clients):
#     """
#     Implémente l'algorithme de Stepping Stone pour trouver la solution optimale.
#     """
#     num_rows = len(costs)
#     num_cols = len(costs[0])

#     # S'assurer que les tables sont en entiers
#     solution_table = [[int(x) for x in row] for row in solution_table]
#     costs = [[int(x) for x in row] for row in costs]

#     while True:
#         # 1. Identifier les cellules basiques (affectées)
#         basic_cells = set()
#         for r in range(num_rows):
#             for c in range(num_cols):
#                 if solution_table[r][c] > 0:
#                     basic_cells.add((r, c))

#         # 2. Identifier les cellules non basiques
#         non_basic_cells = []
#         for r in range(num_rows):
#             for c in range(num_cols):
#                 if (r, c) not in basic_cells:
#                     non_basic_cells.append((r, c))

#         # Calculer les pénalités (indices d'amélioration) pour les cellules non basiques
#         penalties = {}
#         most_negative_penalty = 0 # Commence à 0, cherche des valeurs < 0
#         most_negative_cell = None

#         for r_nb, c_nb in non_basic_cells:
#             # Trouver un chemin fermé pour chaque cellule non basique
#             path = find_closed_loop(r_nb, c_nb, basic_cells, num_rows, num_cols)
            
#             if path:
#                 # Calcul de la pénalité (delta)
#                 penalty = 0
#                 for i, (r_p, c_p) in enumerate(path):
#                     # Les signes alternent: + pour la cellule non basique, puis - , + , - ...
#                     sign = 1 if i % 2 == 0 else -1 
#                     penalty += sign * costs[r_p][c_p]
                
#                 penalties[(r_nb, c_nb)] = penalty
#                 # Chercher la pénalité la plus négative
#                 if penalty < most_negative_penalty:
#                     most_negative_penalty = penalty
#                     most_negative_cell = (r_nb, c_nb)
        
#         # 3. Vérifier l'optimalité
#         if most_negative_penalty >= 0:
#             break # La solution est optimale, car aucune pénalité négative n'a été trouvée.

#         # 4. Améliorer la solution si une pénalité négative a été trouvée
#         pivot_r, pivot_c = most_negative_cell
#         path_to_adjust = find_closed_loop(pivot_r, pivot_c, basic_cells, num_rows, num_cols)

#         if not path_to_adjust:
#             print(f"Attention: Aucun chemin fermé trouvé pour la cellule pivot {pivot_cell}. "
#                   "L'optimisation pourrait être incomplète ou nécessiter une recherche de chemin plus complexe. "
#                   "Sortie de la boucle d'optimisation.")
#             break

#         # Déterminer la plus petite quantité à soustraire (valeur theta)
#         # C'est la plus petite allocation dans les cellules du chemin qui ont un signe négatif.
#         min_transfer_amount = float('inf')
#         for i, (r_p, c_p) in enumerate(path_to_adjust):
#             if i % 2 != 0: # Cellules avec un signe négatif dans le cycle (indices impairs)
#                 min_transfer_amount = min(min_transfer_amount, solution_table[r_p][c_p])
        
#         # Ajuster les quantités dans le tableau de solution le long du chemin
#         for i, (r_p, c_p) in enumerate(path_to_adjust):
#             if i % 2 == 0: # Ajouter la quantité pour les cellules avec signe positif
#                 solution_table[r_p][c_p] += min_transfer_amount
#             else: # Soustraire la quantité pour les cellules avec signe négatif
#                 solution_table[r_p][c_p] -= min_transfer_amount
        
#         # Nettoyer les cellules dont l'allocation est devenue nulle (ou très proche de zéro)
#         for r in range(num_rows):
#             for c in range(num_cols):
#                 if solution_table[r][c] < 0.001: # Utiliser une petite tolérance pour gérer les flottants
#                     solution_table[r][c] = 0

#     # Calculer le coût total de la solution optimale finale
#     optimal_cost = 0
#     final_assignments = []
#     for r in range(num_rows):
#         for c in range(num_cols):
#             optimal_cost += costs[r][c] * solution_table[r][c]
#             if solution_table[r][c] > 0:
#                 final_assignments.append({'source': entrepots[r], 'destination': clients[c], 'amount': solution_table[r][c]})

#     return {
#         'optimal_cost': optimal_cost,
#         'optimal_solution_table': solution_table,
#         'final_assignments': final_assignments
#     }


# @app.route('/solve', methods=['POST'])
# def solve():
#     """
#     API endpoint to solve the transportation problem.
#     It uses the Minimum Cost Method for the initial basic feasible solution
#     and then the Stepping Stone algorithm for optimization.
#     Expects JSON input with 'tableEntrepots', 'tableClients', 'tableCouts',
#     'tableQuantiteDemande', and 'tableQuantiteStocke'.
#     Returns:
#         JSON: The initial and optimal solutions, or an error message.
#     """
#     try:
#         data = request.json
        
#         # Validation des données d'entrée
#         if not all(isinstance(x, str) and x.strip() for x in data['tableEntrepots']):
#             return jsonify({'error': 'Tous les entrepôts doivent être des chaînes non vides.'}), 400
#         if not all(isinstance(x, str) and x.strip() for x in data['tableClients']):
#             return jsonify({'error': 'Tous les clients doivent être des chaînes non vides.'}), 400
        
#         try:
#             costs_input = [[int(x) for x in row] for row in data['tableCouts']]
#             if any(x < 0 for row in costs_input for x in row):
#                 raise ValueError("Les coûts doivent être des nombres entiers positifs.")
#         except (ValueError, TypeError) as e:
#             return jsonify({'error': f'Tous les coûts doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
#         try:
#             demand_input = [int(x) for x in data['tableQuantiteDemande']]
#             if any(x <= 0 for x in demand_input):
#                 raise ValueError("Toutes les quantités demandées doivent être des nombres entiers positifs.")
#         except (ValueError, TypeError) as e:
#             return jsonify({'error': f'Toutes les quantités demandées doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
#         try:
#             supply_input = [int(x) for x in data['tableQuantiteStocke']]
#             if any(x <= 0 for x in supply_input):
#                 raise ValueError("Toutes les quantités stockées doivent être des nombres entiers positifs.")
#         except (ValueError, TypeError) as e:
#             return jsonify({'error': f'Toutes les quantités stockées doivent être des nombres entiers positifs. Détails: {e}'}), 400
        
#         # Vérification si le problème de transport est équilibré
#         if sum(supply_input) != sum(demand_input):
#             return jsonify({'error': 'La somme des quantités stockées doit être égale à la somme des quantités demandées.'}), 400
        
#         entrepots = data['tableEntrepots']
#         clients = data['tableClients']
        
#         # Calcul de la solution de base en utilisant la méthode du coût minimal
#         minitab_result = Mini_tab(costs_input, demand_input, supply_input, entrepots, clients)

#         if isinstance(minitab_result, str): # Gérer les messages d'erreur retournés par Mini_tab
#             return jsonify({'error': minitab_result}), 400

#         initial_solution_table = [row[:] for row in minitab_result['solution_table']] # Copie pour Stepping_Stone
#         initial_solution_result = {
#             'initial_assignments' : minitab_result["initial_assignments"],
#             'solution_base_cost' : minitab_result["solution_base_cost"],
#             'solution_table' : minitab_result["solution_table"],
#         }

#         # Application de l'algorithme de Stepping Stone pour l'optimisation
#         stepping_stone_result = Stepping_Stone(costs_input, initial_solution_table, entrepots, clients)
        
#         # Retourner les résultats des deux étapes
#         return jsonify(initial_solution_result, stepping_stone_result)
    
#     except Exception as e:
#         # Gestion générique des erreurs serveur
#         print(f"Erreur serveur: {str(e)}")
#         return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500
    

# if __name__ == '__main__':
    
#     # Esorina fotsiny ny commentaire raha raha te hi teste ilay application

#     #****************************************************************************************************************
#     #
#     # example_couts = [
#     #     [9, 12, 9, 6, 9, 10],  
#     #     [7, 3, 7, 7, 5, 5],  
#     #     [6, 5, 9, 11, 3, 11],  
#     #     [6, 8, 11, 2, 2, 10]
#     # ]
#     # example_entrepots = ['A', 'B', 'C', 'D']
#     # example_clients = ['1', '2', '3', '4', '5', '6']
#     # example_quantite_stocke = [50, 60, 20, 90] 
#     # example_quantite_demande = [40, 30, 70, 20, 40, 20] 

#     # print("--- Calcul de la solution initiale (Méthode du Coût Minimum) ---")
#     # initial_sol = Mini_tab(
#     #     copy.deepcopy(example_couts), # Utilise une copie pour ne pas modifier les coûts originaux
#     #     example_quantite_demande, 
#     #     example_quantite_stocke, 
#     #     example_entrepots, 
#     #     example_clients
#     # )
#     # if isinstance(initial_sol, str):
#     #     print(f"Erreur lors du calcul de la solution initiale: {initial_sol}")
#     # else:
#     #     print(f"Coût de la solution initiale: {initial_sol['solution_base_cost']}")
#     #     print("Tableau d'allocation initial:")
#     #     for row in initial_sol['solution_table']:
#     #         print(row)
#     #     print("\n--- Application de l'algorithme Stepping Stone ---")
#     #     # Passe une copie de la solution initiale pour que Stepping_Stone puisse la modifier
#     #     optimal_sol = Stepping_Stone(
#     #         example_couts, # Coûts originaux nécessaires pour le calcul des pénalités
#     #         copy.deepcopy(initial_sol['solution_table']), 
#     #         example_entrepots, 
#     #         example_clients
#     #     )
#     #     print(f"Coût de la solution optimale: {optimal_sol['optimal_cost']}")
#     #     print("Tableau d'allocation optimal:")
#     #     for row in optimal_sol['optimal_solution_table']:
#     #         print(row)
#     #     print("\n--- Fin de l'exemple ---")
#     #
#     # *********************************************************************************************************
#     app.run(debug=True)


