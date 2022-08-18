# ahpn_copy_new_scans

Creates a list of files to be copied and written to tape from new AHPN submission

## USE
To run this script:

`python ahpn_find_new_files.py`

## ABOUT
This script identifies AHPN materials that have not already been written to tape from previous material submissions. It calculates sha-256 hash values for all newly submitted materials and creates a manifest: **ahpn_new_manifest_list-<timestamp>.csv**

The script compares the materials in the new manifest (by both hash value and file path) to those in the existing manifest of AHPN materials already written to tape. It returns a "copy list" of the materials not already written to tape: **ahpn_copy_list-<timestamp>.csv**

For each item, the copy list contains: 
- sha-256 hash value
- drive file path
- full file path (from the location the script was run)
- file name
- file size (bytes)

The script also creates a CSV of the matches found between the existing manifest and the new: **ahpn_match_list-<timestamp>.csv**