"""Independent correctness checks: every solution against a slow, obvious reference.

Used by ``python lessons/verify.py``.  One module per group of categories; each
check produces a random input together with the answer a brute-force reference
gives for it (or a judge, when several answers are acceptable).
"""
