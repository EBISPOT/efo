import argparse
import pandas as pd
import re

def mark_efo_as_obsolete_in_text(xml_content, efo_id, oba_id, version, reason):
    efo_pattern = re.compile(r'(<!-- http://www.ebi.ac.uk/efo/EFO_{}.*?</owl:Class>)'.format(re.escape(efo_id)), re.DOTALL)
    match = efo_pattern.search(xml_content)
    oba_pattern = re.compile(f'http://www.ebi.ac.uk/efo/EFO_{efo_id}')
    if match:
        efo_term = match.group(1)
        obsoleted_version_tag = f'    <efo:obsoleted_in_version>{version}</efo:obsoleted_in_version>\n'
        reason_tag = f'    <efo:reason_for_obsolescence>{reason}</efo:reason_for_obsolescence>\n'
        deprecated_tag = '    <owl:deprecated rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</owl:deprecated>\n'
        replacement_tag = '    <obo:IAO_0100001>http://purl.obolibrary.org/obo/OBA_' + oba_id + '</obo:IAO_0100001>\n'

        label_pattern = re.compile(r'(<rdfs:label>)(.*?)(</rdfs:label>)')
        efo_term = label_pattern.sub(r'\1obsolete_\2\3', efo_term)
        updated_efo_term = re.sub(r'(</owl:Class>)', obsoleted_version_tag + reason_tag + deprecated_tag + replacement_tag + r'\1', efo_term)

        before_updated_section = xml_content[:match.start()]
        before_updated_section = oba_pattern.sub(f'http://purl.obolibrary.org/obo/OBA_{oba_id}', before_updated_section)
        after_updated_section = xml_content[match.end():]
        after_updated_section = oba_pattern.sub(f'http://purl.obolibrary.org/obo/OBA_{oba_id}', after_updated_section)
        xml_content = before_updated_section + updated_efo_term + after_updated_section
    else:
        print(f"Error: EFO term {efo_id} not found in the XML content.")
        sys.exit(1)

    return xml_content

def process_csv_and_update_ontology(csv_file, ontology_xml_file, version, output_file):
    df = pd.read_csv(csv_file)
    with open(ontology_xml_file, "r") as f:
        xml_content = f.read()

    for _, row in df.iterrows():
        print(f"Replacing EFO term {row['efo_id']} with OBA term {row['oba_id']}")
        efo_id = row['efo_id'].split(':')[1]
        oba_id = row['oba_id'].split(':')[1]
        reason = f"Project to replace EFO measurement branch with enriched OBA branch. Please use: OBA:{oba_id}"
        xml_content = mark_efo_as_obsolete_in_text(xml_content, efo_id, oba_id, version, reason)

    with open(output_file, "w") as f:
        f.write(xml_content)
    print(f"Ontology XML has been updated and saved as '{output_file}'.")

def main():
    parser = argparse.ArgumentParser(description="Update an ontology XML file by marking EFO terms as obsolete and replacing references with OBA terms.")
    
    parser.add_argument("csv_file", help="Path to the CSV file containing EFO and OBA term mappings")
    parser.add_argument("ontology_xml_file", help="Path to the ontology XML file to be updated")
    parser.add_argument("version", help="Version of the update (e.g., 3.74.0)")
    parser.add_argument("output_file", help="Path to save the updated ontology XML file")

    args = parser.parse_args()

    process_csv_and_update_ontology(args.csv_file, args.ontology_xml_file, args.version, args.output_file)

if __name__ == "__main__":
    main()

