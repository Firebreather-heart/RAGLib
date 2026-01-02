import os
import sys
import time

from chunker import chunk_generator
from .state_manager import StateManager

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def read_dir(path:str):
    file_list = [f for f  in os.scandir(path) if f.is_file()]
    return file_list 

def process_file(filepath:str, sm:StateManager)->bool:
    """Only pass reasonable file sizes to this"""
    filehash = sm.get_file_hash(filepath)
    file_state = sm.get_file_state(filepath)
    if not file_state:
        sm.insert_file(filepath, filehash)
        file_state = sm.get_file_state(filepath)
    
    if not file_state:
        raise ValueError('could not fetch file state from db')
    
    if file_state['file_hash'] != filehash:
        sm.insert_file(filepath, filehash)
        file_state = sm.get_file_state(filepath)

    if not file_state:
        raise ValueError('could not fetch file state from db')

    if file_state["status"] == 'COMPLETED':
        print(f'skipping file {filepath}')
        return True
    
    start_idx = file_state['last_chunk_index']
    try:
        with open(filepath, 'r') as f:
            txt = f.read()
    except UnicodeDecodeError:
            print(f'Skipping non-utf8 file: {filepath}')
            return False
    
    for real_idx, (chunk, _) in enumerate(chunk_generator(
        txt, 500, 50
    )):
        if real_idx <= start_idx:
            continue
        
        print(f"****************\n{real_idx} -> chunking {filepath}\n{chunk}\n\n\n")
        sm.set_file_progress(filepath, real_idx)
        time.sleep(0.1)
    sm.mark_completed(filepath)
    return True
            

if __name__ == '__main__':
    sm = StateManager()
    data_path = os.path.join(parent_dir, 'test_data')
    
    if os.path.exists(data_path):
        files = read_dir(data_path)
        for file_path in files:
            process_file(file_path.path, sm)
    else:
        print(f"Directory not found: {data_path}")