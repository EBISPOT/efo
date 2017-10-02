#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import re
import yaml
import json
import uuid
import csv
import itertools
import sys
import warnings
from collections import Counter

gcif = None
synmap = {}
titlemode = False

def main():

    parser = argparse.ArgumentParser(description='DOSDB'
                                                 'fooo',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-t', '--to', type=str, required=False,
                        help='Renderer')
    parser.add_argument('-n', '--name', type=str, required=False, default='auto',
                        help='Ontology name')
    parser.add_argument('-b', '--base', type=str, required=False, default='http://purl.obolibrary.org/obo/',
                        help='URI base prefix')
    parser.add_argument('-p', '--pattern', type=str, required=False,
                        help='YAML Pattern file')
    parser.add_argument('-P', '--prefixes', type=str, required=False,
                        help='Prefix map file')
    parser.add_argument('-i', '--input', type=str, required=False,
                        help='Input file for values to be filled in template')
    parser.add_argument('-x', '--xpfiles', nargs='+', required=False,
                        help='Input file for values to be filled in template')
    parser.add_argument('-a', '--annotate', type=bool, required=False,
                        help='Annotate each generated class with template values')
    parser.add_argument('-U', '--titlemode', type=bool, required=False,
                        help='Auto-uppercasify (e.g. HPO)')
    parser.add_argument('-G', '--gci', type=str, required=False,
                        help='Output file for GCI axioms not expressable in OMN')
    parser.add_argument('-s', '--suppress', nargs='+', required=False, default=[],
                        help='Suppress annotations')
    parser.add_argument('-S', '--synonym', type=str, required=False, default=[],
                        help='json synonym files')
    args = parser.parse_args()

    global titlemode
    titlemode = args.titlemode

    global synmap
    if args.synonym:
        f = open(args.synonym, 'r')
        synmap = json.load(f)
        f.close()
    
    prefixmap = {}
    if args.prefixes:
        f = open(args.prefixes, 'r')
        prefixmap = yaml.load(f)
        f.close()

    pattern_name = args.pattern
    f = open(args.pattern, 'r') 
    tobj = yaml.load(f)
    if 'pattern_name' not in tobj:
        tobj['pattern_name'] = pattern_name

    ontology_iri = args.base + args.name

    # REPAIR
    # See https://github.com/dosumis/dead_simple_owl_design_patterns/issues/26
    # historically we have used 'property', but the schema now defined as 'annotationProperty'
    if 'annotations' in tobj:
        for aobj in tobj['annotations']:
            if 'property' in aobj:
                warnings.warn("Updating deprecated key: property -> annotationProperty")
                aobj['annotationProperty'] = aobj['property']

    
    global gcif
    if args.gci:
        gcif = open(args.gci, 'w')
        gcif.write('Prefix(:=<%s>)\n' % args.base)
        for (k,v) in prefixmap.items():
            gcif.write('Prefix(%s:=<%s>)\n' % (k,v)) 
        gcif.write('Ontology(<%s-gci>\n' % ontology_iri)
        
    bindings_list = []
    if args.input:
        bindings_list = parse_bindings_list(args.input)
    if args.xpfiles:
        bindings_list = parse_xp_files(args.xpfiles)
    print('Prefix: : <%s>' % args.base)
    print('Prefix: IAO: <http://purl.obolibrary.org/obo/IAO_>')
    print('Prefix: DOSDP: <http://geneontology.org/foo/>')
    print('Prefix: oio: <http://www.geneontology.org/formats/oboInOwl#>')
    for (pfx,uri) in prefixmap.items():
            print('Prefix: %s: <%s>' % (pfx,uri))
    
    print()
    print(" ## Auto-generated")
    print()
    print('Ontology: <%s>' % ontology_iri)
    if 'imports' in tobj:
        for uri in tobj['imports']:
            print('  Import: <%s>' % uri)
    print('AnnotationProperty: IAO:0000115')
    for v in tobj['vars']:
        print('AnnotationProperty: %s' % make_internal_annotation_property(tobj, v))
    print('AnnotationProperty: %s' % get_applies_pattern_property())
    print('AnnotationProperty: oio:hasRelatedSynonym')

        
    if 'annotations' in tobj:
        for aobj in tobj['annotations']:
            print('AnnotationProperty: %s' % aobj['annotationProperty'])

        

    ##print('AnnotationProperty: %s' % make_internal_annotation_property(tobj['pattern_name']))

    p = tobj
    # build map of quoted entity replacements
    qm = {}
    for k in p['classes']:
        iri = p['classes'][k]
        qm[k] = iri
        print('Class: %s ## %s' % (iri,k))
    for k in p['relations']:
        iri = p['relations'][k]
        qm[k] = iri
        print('ObjectProperty: %s ## %s' % (iri,k))

    print('## Auto-generated classes')
    for bindings in bindings_list:
        cls_iri = uuid_iri()
        if 'class_iri' in tobj:
            cls_iri = apply_template(tobj['class_iri'], bindings)
        if 'iri' in bindings:
            cls_iri = bindings['iri']
        apply_pattern(tobj, qm, bindings, cls_iri, args)

    if gcif:
        gcif.write(')')
        gcif.close
        
def uuid_iri():
    return format('urn:uuid:%s' % str(uuid.uuid4()))

def render_iri(iri):
    if iri.startswith("urn:") or iri.startswith("http"):
        return "<"+iri+">"
    return iri

def parse_bindings_list(fn):
    delimiter='\t'
    if fn.endswith("csv"):
        delimiter=','
    input_file = csv.DictReader(open(fn), delimiter=delimiter)
    bindings_list = [row for row in input_file]
    return bindings_list

## reeads tabular files and applies cross-product
def parse_xp_files(fns):
    lists = []
    for fn in fns:
        delimiter='\t'
        if fn.endswith("csv"):
            delimiter=','
        input_file = csv.DictReader(open(fn), delimiter=delimiter)
        lists.append( [row for row in input_file] )
    bindings_list = []
    # assume pairwise: TODO: recurse for len>2
    for i in lists[0]:
        for j in lists[1]:
            m = i.copy()
            m.update(j)
            bindings_list.append(m)
    return bindings_list

## Returns an array of length N,
## where N is the same length as the number of vars in the template object
## [ [v1syn1, v1syn2, ...], ..., [vNsyn1, vNsyn2, ...]
def get_synonym_combos(tobj, bindings, synmap, label):
    lvars = tobj['vars']
    vals = []
    for v in lvars:
        syns = []
        id = bindings[v]
        lk = v+" label"
        if lk in bindings:
            syns.append(bindings[lk])
        if id in synmap:
            for s in synmap[id]:
                syns.append(s['synonym'])
        vals.append(syns)
    combos = list(itertools.product(*vals))
    textt = tobj['text']
    texts = []
    for combo in combos:
        text = format(textt % combo)
        if text != label:
            texts.append( ('oio:hasRelatedSynonym', text) )
    return texts


def get_values(tobj, bindings, isLabel=False):
    lvars = tobj['vars']
    vals = []
    for v in lvars:
        varval = ""
        if isLabel:
            k = v+" label"
            varval = bindings[k] if k in bindings else bindings[v]
            if varval == None:
                varval = bindings[v]
        else:
            varval = render_iri(bindings[v])
        vals.append(varval)
    return vals

def apply_template(tobj, bindings, isLabel=False):
    textt = tobj['text']
    vals = get_values(tobj, bindings, isLabel)
    text = format(textt % tuple(vals))
    return text

def apply_pattern(p, qm, bindings, cls_iri, args):
    print("")
    var_bindings = {}
    for v in p['vars']:
        if v not in bindings:
            sys.stderr.write("variable "+v+" is specified in vars: but is not in bindings:\n")
        iri = bindings[v]
        var_bindings[v] = iri
        vl = v + " label"
        lbl = bindings[vl] if vl in bindings else ''
        if not lbl:
            lbl = iri
        print('Class: %s ## %s' % (iri,lbl))

    print("## "+str(json.dumps(var_bindings)))
    
    print('Class: %s' % render_iri(cls_iri))
    label = ""
    if 'name' in p:
        tobj = p['name']
        text = apply_template(tobj, bindings, True)
        if 'label' not in args.suppress:
            ##TODO
            if 'iri label' in bindings and bindings['iri label']:
                label = bindings['iri label']
            else:
                label = text
            write_annotation('rdfs:label', label, bindings)
    if 'def' in p:
        tobj = p['def']
        text = apply_template(tobj, bindings, True)
        # todo: protect against special characters
        write_annotation('IAO:0000115', text, bindings)
    if 'annotations' in p:
        tanns = p['annotations']
        for tobj in tanns:
            ap = tobj['annotationProperty']
            text = apply_template(tobj, bindings, True)
            # todo: protect against special characters
            write_annotation(ap, text, bindings)
    if 'equivalentTo' in p:
        tobj = p['equivalentTo']
        expr_text = apply_template(tobj, bindings)
        expr_cmt = apply_template(tobj, bindings,True).replace("\n", "")
        expr_text = replace_quoted_entities(qm, expr_text)
        print(' EquivalentTo: %s ## %s' % (expr_text,expr_cmt))
    if 'subClassOf' in p:
        tobj = p['subClassOf']
        expr_text = apply_template(tobj, bindings)
        expr_cmt = apply_template(tobj, bindings,True).replace("\n", "")
        expr_text = replace_quoted_entities(qm, expr_text)
        print(' SubClassOf: %s ## %s' % (expr_text,expr_cmt))
    if 'axioms' in p:
        for tobj in p['axioms']:
            expr_text = apply_template(tobj, bindings)
            expr_cmt = apply_template(tobj, bindings,True).replace("\n", "")
            expr_text = replace_quoted_entities(qm, expr_text)
            gcif.write(' %s ## %s\n' % (expr_text,expr_cmt))
    if len(synmap.keys()) > 0:
        if 'name' in p:
            tobj = p['name']
            texts = get_synonym_combos(tobj, bindings, synmap, label)
            if len(texts) > 0:
                print("  ## Auto-syns\n")
                for (prop,text) in texts:
                    write_annotation(prop, text, bindings)
        
    if args.annotate:
        pn = p['pattern_name']
    
        print('  Annotations: %s "%s"' % (get_applies_pattern_property(), pn))
        for (k,v) in var_bindings.items():
            print('  Annotations: %s %s' % (make_internal_annotation_property(p, k), v))

def get_applies_pattern_property():
    return 'DOSDP:applies-pattern'
    
def make_internal_annotation_property(p, s):
    return p['pattern_name'] + "/"+s

def write_annotation(ap, text, bindings={}):
    if titlemode:
        toks = text.split(" ")
        toks[0] = toks[0].title()
        text = " ".join(toks)
    if ap in bindings:
        # override
        if bindings[ap] != '':
            text = bindings[ap]

    # todo: allow non-literal annotations
    print(' Annotations: %s %s' % (ap,safe_quote(text)))

def safe_quote(text):
    text = text.replace("\n"," ").replace('"','\\"')
    return format('"%s"' % text)

# Stolen from DOS' code
def replace_quoted_entities(qm, text):
    for k in qm:
        v = qm[k]
        text = re.sub("\'"+k+"\'", v, text)  # Suspect this not Pythonic. Could probably be done with a fancy map lambda combo.  
    return text



if __name__ == "__main__":
    main()
