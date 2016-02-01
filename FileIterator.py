"""
Directory-Recursive Copy/Rename

This program iterates through a directory and all of its subdirectories using os.walk, renaming every file contianed
in the directory based on input specified by the user. All renaming rules are saved in a dictionary, and stored in a
pickle file for future renaming runs so that bulk renaming can be done very easily and quickly.

HOW TO USE:
    When first run, the program begins with a fresh dictionary. For every new filename encountered the user is prompted
    for the new rule to use to rename that file, which is will then save for every file of that name encountered.
    All rules take into account capitalization. If the file is encountered again with a different capitalization, it is
    renamed to match the rule.

    Multiple copies can also be made from one file. When the user is prompted for a new rule, any copies will be
    separated by commas. For example, given filename 'Asdf' and the rule input 'Asdf,herp,dErp' the file would have
    copies made named 'herp' and 'dErp' as well as preserving the original file. Leaving the original name out of
    the rule input would result in the file being deleted after the copies are made.

"""
import os
import pickle
from shutil import copyfile
__author__ = "Dylan Smith"
__email__ = "Nalydmerc@gmail.com"

# Change this to False to prompt user for pickle path
useInternalPaths = False

# dicname is the name of the dictionary file without the extension.
dicname = 'name_dictionary'
# pickle_directory is the folder that the pickle file is in, WITH SLASH.
pickle_directory = 'C:\\Users\\intern\\Desktop\\'
# working_directory is the folder that you'll be going through, WITHOUT SLASH.
working_directory = "C:\\Users\\intern\\Desktop\\Test"


# Saves renaming rules to file
def save_obj(obj, name):
    with open(pickle_directory + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# Loads renaming rules from file
def load_obj(name):
    with open(pickle_directory + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def run_through_dir(directory):
    # For every directory
    for root, dirs, files in os.walk(directory):
        print(root)
        for file in files:
            file_directory = root
            # Note the fact that the name is lowercase
            name = os.path.splitext(os.path.basename(file))[0].lower()
            proper_name = os.path.splitext(os.path.basename(file))[0]
            extension = os.path.splitext(os.path.basename(file))[1]
            skip = False

            # Learn new renaming rule if it's unknown, or skin if it requires manual inspection
            if name not in rename_dict:
                print('Unknown name found: ' + proper_name)
                new_names = input('Enter new name(s), no extension, split by commas. Leave empty to accept' +
                                  ' the current filename, or type "skip" to skip:')
                if new_names == '':
                    rename_dict[name] = [proper_name]
                    save_obj(rename_dict, dicname)
                elif new_names != 'skip':
                    new_names = new_names.split(',')
                    new_names = [n.strip() for n in new_names]
                    rename_dict[name] = new_names
                    save_obj(rename_dict, dicname)
                else:
                    skip = True

            if not skip:
                # Check the number of items we're renaming the file to. We could be making copies of the screenshot
                # with different names.
                if len(rename_dict[name]) > 1:
                    old_path = root + '\\' + name + extension
                    # Iterate through the List of filename Strings, making a new copy for every string.
                    for new_name in rename_dict[name]:
                        new_path = file_directory + '\\' + new_name + extension
                        if new_name.lower() != name:
                            # We don't know if the new file we're copying this file to already exists, so we'll check
                            # and add a number to append to the filename until we find one that doesn't exist already.
                            if not os.path.exists(new_path):
                                copyfile(old_path, new_path)
                            else:
                                i = 1
                                new_path = file_directory + '\\' + new_name + '(' + str(i) + ')' + extension
                                while os.path.exists(new_path):
                                    i += 1
                                    new_path = file_directory + '\\' + new_name + '(' + str(i) + ')' + extension
                                    copyfile(old_path, new_path)
                        # Rename the file to the proper capitalization.
                        elif new_name != proper_name:
                            os.rename(old_path, new_path)
                    lowercase_new_names = [n.lower() for n in rename_dict[name]]
                    if name not in lowercase_new_names:
                        os.remove(old_path)
                else:
                    new_name = rename_dict[name][0]
                    if new_name != 'thumbs' and new_name != 'thumbs(2)' and proper_name != new_name:
                        new_path = file_directory + '\\' + new_name + extension
                        old_path = root + '\\' + name + extension
                        # If this is true then we're just working with capitalization changes.
                        if old_path.lower() == new_path.lower():
                            os.rename(old_path, new_path)
                        else:
                            # We don't know if the new file we're moving this file to already exists, so we'll check and
                            # add a number to append to the filename until we find one that doesn't exist already.
                            if not os.path.exists(new_path):
                                os.rename(old_path, new_path)
                            else:
                                i = 1
                                new_path = file_directory + '\\' + new_name + '(' + str(i) + ')' + extension
                                while os.path.exists(new_path):
                                    i += 1
                                    new_path = file_directory + '\\' + new_name + '(' + str(i) + ')' + extension
                                os.rename(old_path, new_path)

if not useInternalPaths:
    pickle_path = input("Input pickle file path: ")
    if pickle_path[0] == '"':
        pickle_path = pickle_path[1:-1]
    # These variables follow the same rules as above
    pickle_directory = pickle_path[0:pickle_path.rfind('\\')+1]
    dicname = pickle_path[pickle_path.rfind('\\')+1:pickle_path.rfind('.')]

# Import Pickle Rules
if os.path.isfile(pickle_directory + dicname + '.pkl'):
    rename_dict = load_obj(dicname)
else:
    print("Pickle file not found. Creating new dictionary.")
    rename_dict = {}

for thing in working_directory.split():
    run_through_dir(thing)
