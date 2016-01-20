"""
Directory-Recursive Copy/Rename

This script iterates through a directory and all of its subdirectories recursively, renaming files
and copying files with new names as specified by the user. We needed this at three birds with
a large directory relating to assessments, where a couple thousand screenshots needed
to be renamed to a very specific name standard.

"""
import os
import pickle
from shutil import copyfile

dicname = 'name_dictionary'
pickle_directory = 'C:\\Users\\intern\\Desktop\\'
working_directory = 'C:\\Users\\intern\\Desktop\\December 2015'


def save_obj(obj, name):
    with open(pickle_directory + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(pickle_directory + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def run_through_dir(directory):
    for root, dirs, files in os.walk(directory):
        print(root)
        for child_dir in dirs:
            run_through_dir(root + '\\' + child_dir)
        for file in files:
            file_directory = root
            name = os.path.basename(file).lower()
            extension = os.path.splitext(name)[1]

            if name not in rename_dict:
                print('Unknown name found: ' + name)
                new_names = input('Enter new name(s), no extension, split by commas:').lower()
                new_names = new_names.split(',')
                new_names = [n.strip() for n in new_names]
                rename_dict[name] = new_names
                save_obj(rename_dict, dicname)

            if len(rename_dict[name]) > 1:
                old_path = root + '\\' + name
                for new_name in rename_dict[name]:
                    new_path = os.path.join(file_directory + '\\' + new_name + extension)
                    print(new_path)
                    copyfile(old_path, new_path)
                os.remove(old_path)
            else:
                new_name = rename_dict[name][0]
                new_path = os.path.join(file_directory + '\\' + new_name + extension)
                old_path = root + '\\' + name
                os.rename(old_path, new_path)

if os.path.isfile(pickle_directory + dicname + '.pkl'):
    rename_dict = load_obj(dicname)
else:
    rename_dict = {}

run_through_dir(working_directory)
