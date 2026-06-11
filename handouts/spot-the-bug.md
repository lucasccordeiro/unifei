# Exercise 1 — Spot the Bug (Session 1, 15 min, pairs)

Below is a fragment of C. In pairs, **7 minutes**: find as many defects as
you can. For each one, write down *what* is wrong and *what could happen at
runtime* (crash? silent corruption? attacker opportunity?).

```c
int *zPtr;
int *aPtr = NULL;
void *sPtr = NULL;
int number, i;
int z[5] = {1, 2, 3, 4, 5};

sPtr = z;
++zPtr;
number = zPtr;
number = *zPtr[2];
number = *sPtr;
++z;
```

There are **at least six** distinct problems.

We debrief together: one bug per pair until the board is full.

*(Based on COMP63342 Coursework 01, Q1.)*
