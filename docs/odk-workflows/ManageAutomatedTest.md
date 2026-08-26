## Constraint violation checks

We can define custom checks using [SPARQL](https://www.w3.org/TR/rdf-sparql-query/). SPARQL queries define bad modelling patterns (missing labels, misspelt URIs, and many more) in the ontology. If these queries return any results, then the build will fail. Custom checks are designed to be run as part of GitHub Actions Continuous Integration testing, but they can also run locally.

### Steps to add a constraint violation check:

1. Add the SPARQL query in `src/sparql`. The name of the file should end with `-violation.sparql`. Please give a name that helps to understand which violation the query wants to check.
2. Add the query path to the `--queries` list in the `sparql_test` target in
   `owlmake.yaml`.
3. Run the QC target to confirm the new check is included.

```shell
om make qc
```
