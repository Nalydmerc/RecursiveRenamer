# Directory-Recursive Copy/Rename

This program iterates through a directory and all of its subdirectories using os.walk, renaming every file contianed
in the directory based on input specified by the user. All renaming rules are saved in a dictionary, and stored in a
pickle file for future renaming runs so that bulk renaming can be done very easily and quickly.

# HOW TO USE:
    When first run, the program begins with a fresh dictionary. For every new filename encountered the user is prompted
    for the new rule to use to rename that file, which is will then save for every file of that name encountered.
    All rules take into account capitalization. If the file is encountered again with a different capitalization, it is
    renamed to match the rule.
    
    Multiple copies can also be made from one file. When the user is prompted for a new rule, any copies will be
    separated by commas. For example, given filename 'Asdf' and the rule input 'Asdf,herp,dErp' the file would have
    copies made named 'herp' and 'dErp' as well as preserving the original file. Leaving the original name out of
    the rule input would result in the file being deleted after the copies are made.
