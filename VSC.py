import os 
import hashlib
import sys
import time

def init_repo():
    if os.path.exists('.Byte'):
        print('Repository already exists')
        return
    
    os.makedirs('.Byte/objects', exist_ok=True)
    os.makedirs('.Byte/refs/heads', exist_ok=True)
    with open('.Byte/HEAD', 'w') as f:
        f.write('refs: refs/heads/master')
    print('Initialized repository')

def hash_obj(data):
    sha = hashlib.sha1()
    sha.update(data)
    return sha.hexdigest()

def store_obj(data):
    obj_id = hash_obj(data)
    with open(f'.Byte/objects/{obj_id}', 'wb') as f:
        f.write(data)
    return obj_id

def add_file(filename):
    if not os.path.exists(filename):
        print('File not found')
        return  
    
    with open(filename, 'rb') as f:
        data = f.read()

    obj_id = store_obj(data)
    
    with open('.Byte/index', 'a') as f:
        f.write(f'{obj_id} {filename}\n')   

    print(f"Added {filename}")

def commit(message):
    email = input('Enter your email: ')
    if not os.path.exists('.Byte/index'):
        print('No changes to commit')
        return
    
    with open('.Byte/HEAD') as f:
        files = f.read().strip()

    head = open(".Byte/HEAD").read().strip().split(': ')[1]
    parent = open(f".Byte/{head}").read().strip() if os.path.exists(f".Byte/{head}") else None

    commit_data = f'tree {hash_obj(files.encode())}\n'
    if parent:
        commit_data += f'parent {parent}\n' 
    commit_data += f'\n{message}\n'
    commit_data += f'author: {email}\n'
    commit_data += f'\n{time.time()}'

    commit_id = store_obj(commit_data.encode())

    with open(f'.Byte/{head}', 'w') as f:
        f.write(commit_id)

    print(f'Committed to {commit_id}')

def create_branch(branch_name):
    head = open(".Byte/HEAD").read().strip().split(': ')[1]
    commit_id = open(f".Byte/{head}").read().strip()

    with open(f'.Byte/refs/heads/{branch_name}', 'w') as f:
        f.write(commit_id)

    print(f'Created branch {branch_name} craeted at {commit_id}')

def switch_branch(branch_name):
    branch_path = f'.Byte/refs/heads/{branch_name}'
    if not os.path.exists(branch_path):
        print('Branch does not exist')
        return
    
    with open('.Byte/HEAD', 'w') as f:
        f.write(f'refs: {branch_path}')
    
    print(f'Switched to branch {branch_name}')

def show_log():
    with open(".Byte/HEAD") as f:
        ref_line = f.read().strip()

    if ref_line.startswith("refs: "):
        ref_path = ref_line.split("refs: ")[1]
    else:
        print("HEAD file is corrupted")
        return
    
    branch_path = f".Byte/{ref_path}"
    
    if not os.path.exists(branch_path):
        print("No commits found")
        return

    with open(branch_path) as f:
        commit_id = f.read().strip()
    
    while commit_id:
        commit_file = f".Byte/objects/{commit_id}"
        
        if not os.path.exists(commit_file):
            print(f"Commit object {commit_id} is missing")
            return
        
        with open(commit_file) as f:
            commit_data = f.read()
        
        print(f"\nCommit: {commit_id}\n")
        print(commit_data)

        parent_line = [line for line in commit_data.split('\n') if line.startswith('parent')]
        commit_id = parent_line[0].split(' ')[1] if parent_line else None


if len(sys.argv) < 2:
    print('Usage: python VSC.py <command>')
    sys.exit(1)

command = sys.argv[1]

if command == 'init':
    init_repo()
elif command == 'add':
    add_file(sys.argv[2])
elif command == 'commit':
     commit(sys.argv[sys.argv.index("-m") + 1])
elif command == "branch" and len(sys.argv) > 2:
    create_branch(sys.argv[2])
elif command == "switch" and len(sys.argv) > 2:
    switch_branch(sys.argv[2])
elif command == 'log':
    show_log()
else:
    print(f'Unknown command {command}')
    sys.exit(1)