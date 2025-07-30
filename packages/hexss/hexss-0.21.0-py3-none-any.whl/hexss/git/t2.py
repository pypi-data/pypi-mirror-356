import os
import subprocess
from git import Repo

GIT_URL = "https://github.com/hexs/Image-Dataset.git"
CLONE_DIR = "Image-Dataset"
SPARSE_PATH = "pet_photos/Dog"
BRANCH = "main"

# Clone with minimal history (no checkout, no blobs)
if not os.path.exists(CLONE_DIR):
    Repo.clone_from(
        GIT_URL, CLONE_DIR,
        no_checkout=True,
        multi_options=["--filter=blob:none"]
    )

os.chdir(CLONE_DIR)

# Initialize sparse-checkout (cone mode)
subprocess.run(["git", "sparse-checkout", "init", "--cone"], check=True)
subprocess.run(["git", "sparse-checkout", "set", SPARSE_PATH], check=True)
subprocess.run(["git", "checkout", BRANCH], check=True)

print(f"Done! Only {SPARSE_PATH} is checked out in {os.path.abspath('.')}")

'''
output is
Your branch is up to date with 'origin/main'.
Already on 'main'
Done! Only pet_photos/Cat is checked out in C:\PythonProjects\hexss\hexss\git\Image-Dataset

and if I want 'pet_photos/Dog'

'''

'''
git clone --filter=blob:none --no-checkout https://github.com/hexs/Image-Dataset.git
cd Image-Dataset
git sparse-checkout init --cone
git sparse-checkout set pet_photos/Cat
git checkout main
'''