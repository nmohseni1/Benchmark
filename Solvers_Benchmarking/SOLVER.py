import utils
import copy



def solve(num_agents, edges, timeout):
    coalitions = [list(range(num_agents))]
    for _ in range(num_agents):
        new_coalitions = copy.deepcopy(coalitions)
        for c in coalitions:
            if len(c) > 1:
                c1, c2 = split(c, edges, timeout)
                if utils.value(c1, edges) + utils.value(c2, edges) > utils.value(c, edges):
                    new_coalitions.remove(c)
                    new_coalitions.append(c1)
                    new_coalitions.append(c2)
        if len(coalitions) == len(new_coalitions):
            break
        coalitions = new_coalitions
    return coalitions



def split(c, edges, timeout, solver='QBSOLVE'):
    Q = {}
    for i in range(len(c)):
        for j in range(len(c)):
            if i < j:
                utils.add(Q, i, i, edges[(c[i],c[j])])
                utils.add(Q, j, j, edges[(c[i],c[j])])
                utils.add(Q, i, j, -2*edges[(c[i],c[j])])
    if solver == 'QBSOLVE':
        solution = utils.solve_with_qbsolv(Q, len(c), timeout)
    elif solver == 'SA':
        solution = utils.solve_with_SA(Q, len(c), timeout)
    elif solver == 'Tabu':
        solution = utils.solve_with_Tabu(Q, len(c), timeout)
    else:
        raise ValueError(f"Unknown solver: {solver}")

    c1 = [c[k] for k in range(len(c)) if solution[k] == 1]
    c2 = [c[k] for k in range(len(c)) if solution[k] == 0]
    return c1, c2


