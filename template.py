import os
dirs = [
    os.path.join("data","external"),
    os.path.join("data","interim"),
    os.path.join("data","processed"),
    os.path.join("data", "raw"), 
    "docs",
    "models",
    "references",
    os.path.join("reports", "figures"),    
    "notebooks",
    "saved_models",
    "src"
]
for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass
files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
]
for file_ in files:
    with open(file_, "w") as f:
        pass