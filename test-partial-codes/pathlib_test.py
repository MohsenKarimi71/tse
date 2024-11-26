from pathlib import Path


# iterating over all files and directories in current directory and gathering directories
p = Path(".")
dirs = [x for x in p.iterdir() if x.is_dir()]
print(dirs)


# iterating over all files and directories in parent directory and gathering files
p = Path("..")
dirs = [x for x in p.iterdir() if x.is_dir()]
print(dirs)


# listing all python source files in current directory
p = Path('.')
py_files = list(p.glob("**/*.py"))
print(py_files)
py_files = list(p.glob("*.py"))
print(py_files)
py_files = list(p.glob("../**/*1.xlsx"))
print(py_files)


# listing all file and directory in 'related' directory in parent directory
p = Path('../related')
contents = [x for x in p.iterdir()]

for content in contents:
    print("directory: " + str(content) if content.is_dir() else "file: " + str(content))