import os
import backend
from backend import delete_filled_dir

workdirectory = os.getcwd()
print(workdirectory)
print(os.walk(workdirectory))
backend.prepare_env()
os.chdir(workdirectory + r'\test')
backend.copy_file_in_workdir()