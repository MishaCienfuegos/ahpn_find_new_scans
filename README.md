# ahpn_find_new_scans

Creates a list of files to be copied and written to tape from new AHPN submission

## USE
To run this script:

`python ahpn_find_new_files.py -old <path-to-existing-ahpn-manifest.csv> -new <path-to-directory-with-new-ahpn-scans>`

## ABOUT
This script identifies AHPN materials that have not already been written to tape from previous material submissions. It calculates sha-256 hash values for all newly submitted materials and creates a manifest: `ahpn_new_manifest_list-<timestamp>.csv`

The script compares the materials in the new manifest (by both hash value and file path) to those in the existing manifest of AHPN materials already written to tape. It returns a "copy list" of the materials not already written to tape: `ahpn_copy_list-<timestamp>.csv`

For each item, the copy list contains: 
- sha-256 hash value
- drive file path
- full file path (from the location the script was run)
- file name
- file size (bytes)

The script also creates a CSV of the matches found between the existing manifest and the new: `ahpn_match_list-<timestamp>.csv`. This list can be used to confirm these files have been written to tape.

NOTE: This script checks both the hash value and file path to determine if the item should be copied. A file is added to the copy list if a match for both is not found in the existing manifest. See code comments for the functions `find_matches` and `subtract_lists`.

This script is intended as Step 1 in a two-step process:
1. Create new manifest and identify items to copy
2. Copy

See this [Identifying & Copying New Scans](https://wikis.utexas.edu/pages/viewpage.action?pageId=205204519) wiki for the previous workflow using Open Refine, including steps for copying the new materials.

Note also that calculating the hashes to create a manifest for the new scans requires some computational power. A standard machine should be adequate for subfolders, but to create a manifest for the whole drive, consider using a more-powerful-than-average machine.

