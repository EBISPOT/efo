#!/usr/bin/env python3
"""Compare the named class hierarchies of two reasoned EFO releases.

Usage: reasoner_hierarchy_diff.py A.owl B.owl [--out-dir DIR]

Each input is a reasoned release (RDF/XML or functional syntax; RDF/XML is
converted with `om convert`).  The script extracts every named `SubClassOf`
axiom, then reports the edges present in only one file after discounting edges
that are merely re-routed, i.e. still reachable through the other file's named
hierarchy.  What remains are genuine differences in what the two reasoners
entailed.  Written for the scheduled HermiT QC workflow (HermiT build vs the ELK
release) and usable by hand for any two builds.  Always exits 0; the caller
decides what counts as a failure.
"""
import argparse, collections, os, re, subprocess, sys, tempfile

NAME = r'(<[^>]+>|[A-Za-z][\w.-]*:[\w.-]+)'
SUB = re.compile(r'^SubClassOf\((?:Annotation\([^)]*\) )*' + NAME + ' ' + NAME + r'\)$')
LABEL = re.compile(r'^AnnotationAssertion\((?:Annotation\([^)]*\) )*rdfs:label ' + NAME + r' "((?:[^"\\]|\\.)*)"')


def to_ofn(path):
    if path.endswith('.ofn'):
        return path
    out = os.path.join(tempfile.mkdtemp(), os.path.basename(path) + '.ofn')
    subprocess.run([os.environ.get('OM', 'om'), 'convert', '-i', path, '-o', out], check=True)
    return out


def load(path):
    edges, labels = set(), {}
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            m = SUB.match(line)
            if m:
                edges.add((m.group(1), m.group(2)))
                continue
            m = LABEL.match(line)
            if m:
                labels.setdefault(m.group(1), m.group(2))
    return edges, labels


def reachable(edges):
    g = collections.defaultdict(set)
    for a, b in edges:
        g[a].add(b)

    def reach(a, b):
        seen, stack = {a}, [a]
        while stack:
            x = stack.pop()
            for y in g.get(x, ()):
                if y == b:
                    return True
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return False
    return reach


def short(iri):
    iri = iri.strip('<>')
    return re.sub(r'^.*/(?:obo/|efo/|ORDO/)?', '', iri) if iri.startswith('http') else iri.split(':', 1)[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('a'); ap.add_argument('b')
    ap.add_argument('--out-dir', default='.')
    args = ap.parse_args()
    ea, la = load(to_ofn(args.a)); eb, lb = load(to_ofn(args.b))
    labels = {**lb, **la}
    ra, rb = reachable(ea), reachable(eb)
    only_a = sorted((x, y) for x, y in ea - eb if not rb(x, y))
    only_b = sorted((x, y) for x, y in eb - ea if not ra(x, y))
    na, nb = os.path.basename(args.a).split('.')[0], os.path.basename(args.b).split('.')[0]
    print(f'{na}: {len(ea):,} named SubClassOf axioms; {nb}: {len(eb):,}; shared {len(ea & eb):,}')
    print(f'entailed only by {na}: {len(only_a)}   entailed only by {nb}: {len(only_b)}   (re-routed edges discounted)')
    os.makedirs(args.out_dir, exist_ok=True)
    for name, rows in ((f'only_in_{na}.tsv', only_a), (f'only_in_{nb}.tsv', only_b)):
        with open(os.path.join(args.out_dir, name), 'w', encoding='utf-8') as f:
            f.write('subclass\tsubclass label\tsuperclass\tsuperclass label\n')
            for x, y in rows:
                f.write(f'{short(x)}\t{labels.get(x, "")}\t{short(y)}\t{labels.get(y, "")}\n')
    for title, rows in ((f'only {na}', only_a), (f'only {nb}', only_b)):
        for x, y in rows[:60]:
            print(f'  [{title}] {short(x)} ({labels.get(x, "")}) SubClassOf {short(y)} ({labels.get(y, "")})')
        if len(rows) > 60:
            print(f'  [{title}] … {len(rows) - 60} more in {args.out_dir}')


if __name__ == '__main__':
    main()
