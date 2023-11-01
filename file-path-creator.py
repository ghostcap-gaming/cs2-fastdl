import os

CONFIG_FILE = "config.txt"
DOWNLOADS_FILE = "downloads.txt"
DEFAULT_FOLDERS = ["testmaps", "testmodels"]

def list_files(startpath='.'):
    file_paths = []

    for root, dirs, files in os.walk(startpath):
        for file in files:
            if file == '.DS_Store':
                continue
            
            path = os.path.join(root, file)
            file_paths.append(path)

    if "assets.zip" not in file_paths and os.path.exists("assets.zip"):
        file_paths.append("assets.zip")

    return file_paths

def save_to_file(paths, filename=DOWNLOADS_FILE):
    with open(filename, 'w') as f:
        for path in paths:
            f.write(path + '\n')

def read_previous_downloads(filename=DOWNLOADS_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().splitlines()
    return []

def read_config_folders(filename=CONFIG_FILE):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            for folder in DEFAULT_FOLDERS:
                f.write(folder + '\n')
        return DEFAULT_FOLDERS
    
    with open(filename, 'r') as f:
        return f.read().splitlines()

if __name__ == "__main__":
    folders = read_config_folders()

    prev_downloads = set(read_previous_downloads())

    all_paths = []
    for folder in folders:
        all_paths.extend(list_files(folder))

    all_paths = set(all_paths)
    final_paths = all_paths.union(prev_downloads) - (prev_downloads - all_paths)

    save_to_file(sorted(list(final_paths)))
