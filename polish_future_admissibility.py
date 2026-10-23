#!/usr/bin/env python3
"""Conservative, exact-match polishing for The Cost of Future Admissibility.
Preview by default; --apply writes a timestamped backup and edits the .tex file.
"""
import argparse
from pathlib import Path
from datetime import datetime
import difflib

p = argparse.ArgumentParser()
p.add_argument('--file', default='cost_of_future_admissibility.tex')
p.add_argument('--apply', action='store_true')
a = p.parse_args()
path = Path(a.file)
original = path.read_text(encoding='utf-8')
edits = [
('abstract: qualify scope', 'the coarsest sufficient compression is a quotient whose size in bits is monotone and subadditive in the family;', 'the coarsest sufficient compression is a quotient whose logarithmic cardinality, when finite, is monotone and subadditive in the family;'),
('introduction: qualify state-count claim', 'the number of states can grow from the maximum to the product of the individual state counts', 'the number of states lies between the maximum and the product of the individual state counts, with both bounds attainable'),
('family: rank is not literal storage cost', 'a compression tuned to the present retains $\\rank(\\Now)$ bits and one prepared for the future retains $\\rank(\\Fut)$ bits.', 'the minimal present-answer quotients have logarithmic cardinalities $\\rank(\\Now)$ and $\\rank(\\Fut)$, respectively. These are information-capacity lower bounds, not measured storage costs for a particular implementation.'),
('language: avoid finite-state assumption', 'A language whose rules read only bounded windows and typed fields has a small quotient; a language whose rules may quote traces has none.', 'A language whose rules read only uniformly bounded windows over finite event alphabets can have a finite quotient, although its size need not be small; a language whose rules can distinguish arbitrary complete traces forces injectivity on those traces.'),
('revision horizon: qualify promise', 'A promise to enforce a revised constraint is credible exactly when the revision lies in the horizon of the state the system holds when the promise is made.', 'Membership in the revision horizon is an informational precondition for a promise to enforce a revised constraint from the retained state; credibility also requires a correct evaluator, authorization, and the operational ability to act.'),
('sufficiency gate: distinguish syntactic cost from proof', 'The gate costs little when the policy language declares its support, and it converts a silent failure', 'A support-based screening check can be inexpensive when the policy language declares its support, although proving derivability and continuation sufficiency may be costly; such a check can convert a silent failure'),
('privacy: qualify quantified tradeoff', 'The trade-off between privacy-driven erasure and future-policy sufficiency is thus a real one, and Theorem~\\ref{thm:inject} quantifies the cost of leaning to either side.', 'The trade-off between privacy-driven erasure and future-policy sufficiency is thus a real one. Theorem~\\ref{thm:inject} gives an informational lower bound for unrestricted revision, not a monetary or privacy cost for either choice.'),
('conclusion: informational rather than operational adoption', 'the set of revisions that can still be adopted is a Boolean-closed horizon determined by the state\'s partition', 'the set of revisions whose answers remain recoverable from the retained state and subsequent events is a Boolean-closed horizon determined by the state\'s partition'),
]
updated = original
for label, old, new in edits:
    count = updated.count(old)
    if count != 1:
        raise SystemExit(f'STOP: {label}: expected one exact match, found {count}. No changes written.')
    updated = updated.replace(old, new, 1)
    print('OK:', label)
print(''.join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile=str(path), tofile=str(path)+' (proposed)')))
if a.apply:
    backup = path.with_name(path.name + '.' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.bak')
    backup.write_text(original, encoding='utf-8')
    path.write_text(updated, encoding='utf-8')
    print('Applied. Backup:', backup)
else:
    print('Preview only. Run with --apply to write.')

