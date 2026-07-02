
"""
Constraint Negotiation Research Prototype

This is intentionally NOT a graphics program.
It is a laboratory that evolves rewrite operators and records
their ancestry and statistics.

Run:
    python ontology_lab.py
"""

import random
import math
from collections import Counter

OPS = ["A","B","C","D"]

class Rule:
    newid = 0
    def __init__(self, lhs=None, rhs=None, parents=()):
        self.id = Rule.newid
        Rule.newid += 1
        self.lhs = lhs or random.choice(OPS)
        self.rhs = rhs or "".join(random.choice(OPS) for _ in range(random.randint(1,3)))
        self.parents = parents
        self.age = 0
        self.success = 0
        self.fail = 0

    def apply(self,s):
        return s.replace(self.lhs,self.rhs,1)

    @property
    def fitness(self):
        return self.success/(1+self.fail)

rules=[Rule() for _ in range(24)]
population=["".join(random.choice(OPS) for _ in range(8)) for _ in range(200)]

for generation in range(2000):

    newpop=[]

    for state in population:
        r=random.choice(rules)
        new=r.apply(state)

        # reward compression with retained diversity
        before=len(set(state))
        after=len(set(new))
        score=(len(state)-len(new))*0.2+(before-after)*0.4

        if score>=0:
            r.success+=1
        else:
            r.fail+=1

        newpop.append(new)

    population=newpop

    # mutate rules
    if generation%10==0:
        parent=random.choice(rules)
        child=Rule(parent.lhs,parent.rhs,(parent.id,))
        if random.random()<0.5:
            child.lhs=random.choice(OPS)
        else:
            child.rhs="".join(random.choice(OPS) for _ in range(random.randint(1,4)))
        rules.append(child)

    # extinction
    rules=[r for r in rules if r.fitness>0.05 or r.age<50]

    for r in rules:
        r.age+=1

print("=== EVOLVED RULES ===")
for r in sorted(rules,key=lambda x:x.fitness,reverse=True)[:20]:
    print(f"{r.id:3d}: {r.lhs}->{r.rhs:4s} fit={r.fitness:.2f} parents={r.parents}")

print("\nPopulation diversity:")
print(Counter(population).most_common(10))
