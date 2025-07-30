import os
import py_compile

def find_py_files(package_name, dirpath_list, black_list):
    py_files = []
    for dirpath, _, filenames in os.walk(package_name):
        if dirpath in dirpath_list:  
            continue  

        for file in filenames:
            if file.endswith(".py") and file not in black_list: 
                full_path = os.path.join(dirpath, file)
                py_files.append(full_path)
    return py_files

def list_all_subfolders(root_folder):
    subfolders = []
    for dirpath, dirnames, _ in os.walk(root_folder):
        for dirname in dirnames:
            subfolders.append(os.path.join(dirpath, dirname))
    return subfolders

def build_dirpath_list(package_name):
    dirpath_list = []
    dirpath_list.append(package_name)
    dirpath_list.append(package_name + "/Models")
    dirpath_list.append(package_name + "/Tests")
    return dirpath_list

# Adjust the blacklist as needed
black_list = ["__init__.py"]
package_name = "bpusdk"
dirpath_list = build_dirpath_list(package_name)
py_files = find_py_files(package_name, dirpath_list, black_list)

# Compile each .py to .pyc
for py_file in py_files:
    try:
        py_compile.compile(py_file, cfile=py_file + 'c', doraise=True)
        os.remove(py_file)  # Optional: Remove the source .py
    except py_compile.PyCompileError as e:
        print(f"Failed to compile {py_file}: {e}")
print(f"END")