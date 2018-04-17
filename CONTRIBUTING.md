## Before you write a new request, please consider the following:

- **Does the term already exist?** Before submitting suggestions for new ontology terms, check whether the term exist, either as a primary term or a synonym term. You can search using [OLS](http://www.ebi.ac.uk/ols/ontologies/efo). 

## Guidelines for creating GitHub tickets with contributions to EFO:
### General Guidelines:

1. **Write a detailed request:** Please be specific and include as many details as necessary, providing background information, and if possible, suggesting a solution. The editors will be better equipped to address your suggestions if you offer details regarding 'what is wrong', 'why', and 'how to fix it'.

2. **Provide examples and references if necessary:** For example, including PMIDs for new term requests that are harder to define, and including also screenshots, or URLs illustrating the current ontology structure for other types of requests.

3. **For new term request:** Please follow the outlined procedures below for [single term requests](#single-term-request-guidelines) and [multiple term requests](#multiple-term-request-guidelines).

4. **For updates to relationships:** Provide details of the current axioms, why you think they are wrong or not sufficient, and what exactly should be added or removed. These should also be addressed following the single term request or multiple term request methodology.

On behalf of the EFO team, thank you! If you have any questions or are unsure about the contributing process, you can contact us at [efo-users@ebi.ac.uk](mailto:efo-users@ebi.ac.uk).

### Single Term Request Guidelines:

**Note:** A single term request refers to a term request that can be considered a “one off”, i.e. no other term request is expected in the near future. If you have multiple one term requests spanning over time between releases, please collect them in a Google Sheet under a Webulous template as outlined in Multiple Term Requests and follow the Multiple Term Requests contribution outlines.

- Please write a detailed request, following the outline provided automatically when opening a [new ticket](https://github.com/EBISPOT/efo/issues/new). At minimum, a term requires a preferred term label, textual definition and a suggested parent class to be included in EFO. However, the more details supplied for the individual term, the better equipped editors will be to quickly add the term to EFO.
- For updates to existing terms, please ensure you are specific in referencing the exact term e.g. Term label (EFO:000000). 
- When requesting changes to current information, please be as descriptive as possible. For example, when requesting changes to axioms, include current axioms and why you believe they are not currently sufficient, including any references to support the proposed changes, what should be added and what should be removed.
- When requesting the removal of a term, please provide the reason you believe the term should be removed as well as any link to a replacement term currently available in EFO.

### Multiple Term Request Guidelines:

When requesting multiple terms between releases, whether they are connected or are individual, please use Webulous. More information regarding Webulous can be found [here](https://www.ebi.ac.uk/efo/webulous/).

**Installing Webulous**

- Navigate to the ‘Add-ons’ tab of a new Google Sheet.
- Select ‘Get add-ons…” and search for Webulous. 
- Once installed, select Webulous from the ‘Add-ons’ (‘Add-ons’ ⇾ ‘Webulous’) tab and then ‘Webulous template’. 
- Add a new server (https://ebi.ac.uk/efo/webulous **NOT** the supplied http://ebi.ac.uk/efo/webulous server!).

**Using the templates**

- After Webulous is set-up, select the template type (‘Add-ons’ ⇾ ‘Webulous’ ⇾ ‘Webulous template’) you are wishing to use whether your request is for new terms or additional information for existing terms, such as synonyms.
- Fill in the template according to the term(s)/annotations needed.
- For new terms, at minimum, please provide preferred term label, textual definition and a suggested parent class. If possible please also provide X-refs (definition citations). The full list of ontologies and external resources currently imported or mapped into EFO can be found in the [EFO release notes](https://github.com/EBISPOT/efo/blob/master/ExFactor%20Ontology%20release%20notes.txt).


**After completing the template**

- Once completed, please [create a new ticket](https://github.com/EBISPOT/efo/issues/new) with a link to the Google Sheet, ensuring it is accessible for editing by anyone at the EBI. This allows the editors to validate your submission and ensure any errors are caught prior to being merged with EFO.


