# Failure Cases

TODO[PERSON-1]: After running `python eval/evaluate.py`, document misses and false positives here.

Initial categories to watch:

- Arabic number words not covered by the deterministic rules.
- Salary clauses with written-out amounts instead of digits.
- Non-compete clauses that are narrow and should not be flagged by the MVP.
- Deductions that are standard payroll deductions and should not be treated as potential risk.
