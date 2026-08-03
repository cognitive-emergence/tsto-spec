# TSTO/00 Publication Checklist

## Completed in this release

- [x] Version and release date are consistent across normative texts, translations, PDFs, and metadata.
- [x] CC BY 4.0 is declared consistently.
- [x] TSTO and JEP-TSTO Schemas parse as JSON Schema Draft 2020-12.
- [x] The valid TSTO example passes structural validation.
- [x] The invalid TSTO example fails because Baseline evidence is missing.
- [x] All four JEP Binding examples pass the supplementary structural Schema.
- [x] The valid TSTO integrity digest was recomputed with RFC 8785 canonicalization; external resource digests and unsigned signatures are clearly identified as illustrative.
- [x] PDFs were rendered and visually reviewed.
- [x] SHA-256 checksums are included.

## GitHub publication

1. Create a public repository and copy the contents of this directory to its root.
2. Review the repository name and visibility.
3. Commit the release and create tag `tsto-00`.
4. Create a GitHub Release from the tag and attach the four PDFs or the complete ZIP.
5. Enable Issues and private security advisories if feedback will be accepted.

## Zenodo archival

1. Connect the repository to Zenodo before creating the GitHub Release if automatic archival is desired, or upload the Zenodo deposit ZIP manually.
2. Confirm the imported metadata and CC BY 4.0 license.
3. Reserve or mint the DOI and publish the record.
4. Add the assigned DOI to the repository description and a later metadata-only `CITATION.cff` update; do not rewrite the archived release.
