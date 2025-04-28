##################################################################
# Helper functions by Dr. Fabio Papacchini

import numpy as np
import heapq as hq
# facts is a dictionary where keys are atoms names and values are set of tuples representing their instances
# e.g., {"Lecturer" : {("fabio",),("marco",)}} represents Lecturer(fabio) and Lecturer(marco)
facts = {}

# list of rules
# each rule is a tuple (body, head)
# body is a list of atoms (i.e., tuples with atom name as first element)
# head is a single tuple where the first element is the name of the atom, and the other elements are its arguments
# e.g., ([("Lecturer", "X")("Teaches", "X", "Y")], ("Module", "Y"))
# represents the rule Lecturer(x) & Teaches(x,y) -> Module(y)
rules = []


# simple function for adding facts
# the input is the name of the atom followed by its arguments
# e.g., ("Lecturer", "fabio") represents the atom Lecturer(fabio), ("Likes", "fabio", "chocolate") represents Likes(fabio,chocolate)
def add_fact(name, *args):
    global facts
    current_set = set()
    if name in facts.keys():
        current_set = facts[name]
    current_set.add(tuple(args))
    facts[name] = current_set

# simple function to add a rule
# see description above for the format of body and head
def add_rule(body, head):
    global rules
    rules += [(body, head)]


# recursive function to find all ways to instantiate a rule body based on currently known facts
# input:
#  - body of a rule (i.e., a list of atoms with variables)
#  - substitution we are currently trying to build (i.e., a dictionary where keys are variables and values represent what the variables are replaced with)
#  - all found substitutions (i.e., a list of complete substitutions)
def find_substitutions(body_to_check, current_sub, subs):
    global facts

    # base case 1
    # all atoms in the body have been successfully matched by the current substitution
    # add the substitution to the overall list of substitutions and return the list
    if body_to_check == []:
        subs += [current_sub]
        return subs

    # split the body into the atom to check and the rest, we will recurse on the rest to reach the base case 1
    atom, *rest = body_to_check
    # take the atom name and its arguments
    name, *args = atom

    # base case 2
    # if there is no instance for the atom, the substution fails
    # otherwise, collect all possible instances of the atom
    if name in facts.keys():
        matches = facts[name]
    else:
        return subs

    # loop to filter atom instances based on the current values assigned to variables
    for i in range(len(args)):
        var = args[i]
    
        if var in current_sub.keys():
            matches = set(filter(lambda x : True if x[i] == current_sub[var] else False, matches))

    # base case 3
    # if an atom has no instances left, then the current substituion fails
    if matches == []:
        return subs

    # loop over valid atom instances
    for match in matches:
        new_sub = current_sub.copy()

        for i in range(len(args)):
            var = args[i]
            # extend the current substitution with new varible bindings based on the atom instance
            if not (var in new_sub.keys()):
                new_sub[var] = match[i]

        # recursive call -- note that the call is within a for loop, which results in a backtracking approach
        subs = find_substitutions(rest, new_sub, subs)
        
    # return found substitutions
    return subs



# function that apply all found substitutions to the head of the rule to derive new facts
# input: a list of substitutions (each substitution is a dictionary) and the head of a rule
# output: true if a new fact was derived, false otherwise
def derive(substitutions, head):
    global facts

    # unapcking the head to get the atom name and its arguments
    name, *args = head

    result = set()

    # loop to create atom instances based on the different substitutions
    for sub in substitutions:
        # initialisation of an instance as an empty tuple
        instance = ()
        for i in args:
            # updating the instance with actual values based on the substitution under consideration
            instance += (sub[i],)
        result.add(instance)

    # check which instances are actually new
    if name in facts.keys():
         new_facts = result.difference(facts[name])
    else:
        facts[name] = result
        new_facts = result

    # return false if all facts are already known
    if new_facts == set():
        return False


    # update facts with new derived instances and return true
    facts[name] = facts[name].union(new_facts)
    return True

##################################################################
# My code starts here


# function to apply a rule
# call the provided functions 
def apply_rule(rule):
    global facts
    body, head = rule # call the provided functions 
    substitutions = find_substitutions(body, {}, [])
    derive(substitutions, head)


# function to saturate the knowledge base
# it tries to apply rules until no new facts are added to kb
def saturateKB():
    global facts
    global rules
    added_fact = True # flag to track if new facts are added

    while added_fact: # loop until no more facts are added
        added_fact = False
        size_before = sum(len(f) for f in facts.values()) # number of facts before applying rules

        for rule in rules:
            apply_rule(rule) # apply every rule 

        size_after = sum(len(f) for f in facts.values()) # number of facts after applying rules

        if size_after > size_before: # set flag accordingly
            added_fact = True

R_multipliers = {
    "R1": 1.0,
    "R2": 1.2,
    "R3": 1.4,
    "R4": 1.6,
    "R5": 1.8}

# calculate euclidean distance between two points
def distance(start, end):
    return np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)


def construct_graph(allowed_relations):
    """
    constructs a graph from facts in the format:
    {
        point_coordinate: [(neighbor_coordinate, relation_name, cost), (....)],
        point_coordinate: [....],
    }
    only builds edges for allowed relations
    """
    global facts
    graph = {}

    # set up nodes for points
    for points in facts.values():
        # check if fact is a point by checking if all instances have arity 1
        if points and all(len(point) == 1 for point in points): 
            for point in points:
                point = format_coord(point) # remove tuple nesting
                graph[point] = [] # create adjacency list for each point

     # set up missing nodes from relations
    for relation in allowed_relations: 
        if relation in facts and relation in R_multipliers:# check if relation is valid
            for (start, end) in facts[relation]:
                start = format_coord(start)
                end = format_coord(end)
                # create adjacency list for each point
                if start not in graph:
                    graph[start] = [] 
                if end not in graph:
                    graph[end] = [] 

    # add edges for allowed relations
    for relation in allowed_relations:  
        if relation in facts and relation in R_multipliers:  # check if relation is valid
            for (start, end) in facts[relation]:
                start = format_coord(start)
                end = format_coord(end)
                # calculate cost and append
                cost = distance(start, end) * R_multipliers[relation]
                graph[start].append((end, relation, cost))

    return graph


# helper fucntion to format nested coordinate tuples like ((x,y),) to (x,y)
def format_coord(coord):
    # while a coord is a size 1 tuple containing another tuple,
    while isinstance(coord, tuple) and isinstance(coord[0], tuple) and len(coord) == 1:
        coord = coord[0] # unwrap it by setting coord to its only element
    return coord


goals = set() # global goals set
goal_predicates = set() # global aux set to update goals after saturating the KB

# function to update the goals based on the given predicates
# finds the intersection of all sets of points for each predicate
def update_goals(predicates):
    global facts
    global goals, goal_predicates
    
    if not predicates and not goal_predicates:
        goals = set()
        return # exit early and 'return' empty set if nothing was passed in the initial call
    elif predicates: 
        goal_predicates = predicates # save predicates for second call
    else:
        predicates = goal_predicates # restore saved predicates when calling function after saturating the KB
        

    # start with the first goal predicate
    first = predicates[0]
    if first not in facts: # no goals for this predicate if no facts available
        goals = set()
        return        
    possible_goals = set(format_coord(point) for point in facts[first]) # remove tuple nesting before adding to set

    # find intersection with the other goal predicates
    for predicate in predicates[1:]:
        if predicate not in facts:
            goals = set()
            return
        pred_points = set(format_coord(point) for point in facts[predicate]) # remove tuple nesting before adding to set
        possible_goals = possible_goals.intersection(pred_points) # find intersection

    goals = possible_goals


def a_star(start, cost_limit):
    global goals
    frontier = [] # create the priority queue
    best_paths = [] # list to store best paths

    # push the first state on the queue
    hq.heappush(frontier, (heuristic(start), 0, start, [start]))
    
    while frontier:
        # get the most promising path from the queue
        overall, cost, current_state, path = hq.heappop(frontier)

        if cost > cost_limit:# if the cost exceeds the limit, skip
            continue

        # if goal state is reached, store the path with cost
        if current_state in goals:
            best_paths.append((round(cost, 2), path))
            continue 

        # get all possible successors to expand the current path
        successors = get_successors(current_state)

        # create all possible extensions of the current path and push them on the queue
        for (edge_cost, h_succ, neighbor, relation) in successors:
            new_cost = cost + edge_cost
            if new_cost > cost_limit: # if new cost exceeds the limit, skip
                continue
            # update cost and path
            overall_cost = new_cost + h_succ
            new_path = list(path) + [relation, neighbor]
            hq.heappush(frontier, (overall_cost, new_cost, neighbor, new_path))

    best_paths.sort(key=lambda x: x[0]) # sort paths by cost 
    return best_paths[:3] # return the best 3

# helper function to calculate the heuristic (euclidian distance to the closest goal)
def heuristic(state):
    if not goals:
        return 0
    return min(distance(state, goal) for goal in goals)

# helper function to get all successors of a state
def get_successors(state):
    successors = []
    if state not in graph:
        return []
    for (successor, relation, cost) in graph[state]:
        h = heuristic(successor)
        successors.append((cost, h, successor, relation)) # append tuple in the order used by A*
    return successors

# helper function to print A* output
# input format is (path_cost, [path])
def output(a_star_output):
    if not a_star_output[1]:
        return
    print(f'Path cost:  {a_star_output[0]}')
    path = a_star_output[1]
    print('Path:  ', end='')
    for item in path:
        print(item, ' ', end='')
    print()


# run A* to find the best 3 paths and print the output
# repeat before and after saturating the KB
def run(start_state, cost_limit, allowed_relations):
    global graph
    graph = construct_graph(allowed_relations)
    
    print('Before saturating the knowledge base')
    a_star_output = a_star(start_state, cost_limit) # run A*
    if not a_star_output:
        print('No path')
    else:
        for path in a_star_output:
           output(path)

    saturateKB()
    update_goals([])# update goals using predicates saved from first call

    # repeat the same process after saturating the KB
    graph = construct_graph(allowed_relations)
    print('After saturating the knowledge base')
    a_star_output = a_star(start_state, cost_limit)
    if not a_star_output:
        print('No path')
    else:
        for path in a_star_output:
            output(path)
    


# sample test test case 1:
add_fact("P1", (2, 0))
add_fact("P2", (2, 3))
add_fact("P2", (6, 0))
add_fact("P3", (6, 0))
add_fact("R1", (0, 0), (2, 0))
add_fact("R2", (2, 0), (2, 3))
add_fact("R3", (2, 0), (6, 0))

add_rule([("P2", "X")], ("P3", "X"))
add_rule([("R1", "X", "Y"), ("R3", "Y", "Z")], ("R5", "X", "Z"))
add_rule([("R2", "X", "Y"), ("P2", "Y"), ("R3", "X", "Z"), ("P3", "Z")], ("R4", "Y", "Z"))

update_goals(["P3"])
run((0,0), 11, ["R1","R2","R3","R4","R5"])


# sample test test case 2:
# add_fact("A", (0,0))    
# add_fact("A", (-2,2))
# add_fact("A", (2,-1))
# add_fact("B", (-4,0))
# add_fact("B", (2,2))
# add_fact("R1", (0,0), (-2,2))
# add_fact("R1", (0,0), (2,-1))
# add_fact("R1", (2,-1), (2,2))
# add_fact("R2", (-2,2), (-4,0))
# add_fact("R2", (2,-1), (2,2))
# add_fact("R2", (2,2), (4,1))

# add_rule([("A", "X"), ("R1", "X", "Y"), ("R2", "Y", "Z")], ("B", "Z"))
# add_rule([("A", "X"),("R1", "X", "Y"),("R2", "Y", "Z")], ("R3", "X", "Z"))

# update_goals(["B"])
# run((0,0), 6, ["R1","R2","R3","R4","R5"])
            
