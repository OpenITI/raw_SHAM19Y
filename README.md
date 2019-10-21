# raw_SHAM19Y

Shamela texts, scraped in October 2019; converted into mARkdown attempting to map TOC tables onto the text.

This is a test repository:

1. Run `_05_to_OpenITI_mARkdown.py`
2. All files from `3_json` should be converted to OpenITI mARkdown
3. Converted files will be saved to `4_openITI_mARkdown`
4. Those that cannot be converted will be moved to `5_failed_conversion`
5. Those that were successfully converted will be moved to `5_successful_conversion`
6. **NB:** The script breaks on unsuccessful conversion (there seem to be too ,many different issues with the JSON files exported from Shamela BOK files); a workaround: the name of a currently processing file is saved into `latest_file.txt`; if the script fails, the next run of the script moves this file to `5_failed_conversion`.