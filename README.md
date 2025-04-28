# Forward Chaining and A* Pathfinding

This project implements a classical AI system in Python combining forward chaining with A* heuristic pathfinding.  
It builds a knowledge base using predicate logic facts and rules, derives new information through inference, and finds optimal paths before and after knowledge saturation.

## Features

- Representation of predicate facts and binary relations as graph nodes and edges.
- Forward chaining algorithm to derive additional facts and relationships.
- A* search algorithm with support for:
  - Customizable allowed relations (e.g., R1, R2, etc.).
  - User-defined maximum path cost.
  - Finding and returning up to three optimal paths.
  - Dynamic goal state identification based on predicates.
- Pure Python implementation using only `numpy` and `heapq`.

## How to Clone

```bash
git clone https://github.com/Atukas77/Forward-Chaining-and-A_star-Pathfinding
```

## How to Run

The project can be run by appending calls to `add_fact`, `add_rule`, `update_goals`, and `run` at the bottom of the Python file and then executing it. Alternatively, you can import the file or paste the code into an interactive Python 3 session.

### Option 1: Direct Execution

1. Open the Python file.
2. At the bottom, add the setup and execution code. Example:

```python
add_fact("A", (0,0))    
add_fact("A", (-2,2))
add_fact("A", (2,-1))
add_fact("B", (-4,0))
add_fact("B", (2,2))
add_fact("R1", (0,0), (-2,2))
add_fact("R1", (0,0), (2,-1))
add_fact("R1", (2,-1), (2,2))
add_fact("R2", (-2,2), (-4,0))
add_fact("R2", (2,-1), (2,2))
add_fact("R2", (2,2), (4,1))

add_rule([("A", "X"), ("R1", "X", "Y"), ("R2", "Y", "Z")], ("B", "Z"))
add_rule([("A", "X"),("R1", "X", "Y"),("R2", "Y", "Z")], ("R3", "X", "Z"))

update_goals(["B"])
run((0,0), 6, ["R1","R2","R3","R4","R5"])
```

3. Save and run the file:

```bash
python3 forwardchaining_astar.py
```

### Option 2: Interactive Python 3 Session

1. Open a terminal.
2. Launch Python:

```bash
python3
```

3. Paste the code or import the file, and manually add the setup and execution code. Example:

```python
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
```

### Output Interpretation

- Before saturation, the system runs A* on the initial graph.
- After saturation (forward chaining infers new facts), A* is rerun on the expanded graph.
- Paths are printed with their cost and relation sequences.

Example output:

```
Before saturating the knowledge base
Path cost:  7.6
Path:  (0, 0)  R1  (2, 0)  R3  (6, 0)  
After saturating the knowledge base
Path cost:  5.6
Path:  (0, 0)  R1  (2, 0)  R2  (2, 3)  
Path cost:  7.6
Path:  (0, 0)  R1  (2, 0)  R3  (6, 0)  
Path cost:  10.8
Path:  (0, 0)  R5  (6, 0)  
```

### Important Notes

- Use the provided `add_fact` and `add_rule` functions to build or modify the knowledge base.
- Costs are calculated based on Euclidean distance multiplied by relation-specific factors (to ensure heuristics are always optimistic).
- No external modules, file IO, or user prompts are used—the system is manually operated.
