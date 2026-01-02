import hashlib
import sqlite3
from typing import Optional

class StateManager:
    def __init__(self):
        """
        STATUS: NULL, PROCESSING, COMPLETED
        """
        self.cx = sqlite3.connect("pipeline.db")
        self.cx.row_factory = sqlite3.Row
        self.cu = self.cx.cursor()
        self.cu.execute("""
CREATE TABLE IF NOT EXISTS ingestion_state (
    file_path TEXT PRIMARY KEY,
    file_hash TEXT,
    last_chunk_index INTEGER DEFAULT -1,
    status TEXT
                        )
""")
        self.cx.commit()

    def get_file_hash(self, filepath:str):
        """Calculates the SHA256 hash of a file"""
        hasher = hashlib.sha256()
        BUFFER_SIZE = 65536
        with open(filepath, 'rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def get_file_status(self, filepath:str)->Optional[str]:
        current_file = self._get_file(filepath)
        if current_file:
            return current_file['status']
        return None
    
    def insert_file(self, filepath:str, filehash:str):
        query = '''INSERT INTO ingestion_state 
        (file_path, file_hash, last_chunk_index, status) 
        VALUES (?, ?, -1, 'PROCESSING') 
        ON CONFLICT (file_path) DO UPDATE SET
            last_chunk_index = CASE
                WHEN ingestion_state.file_hash != excluded.file_hash THEN -1
                ELSE ingestion_state.last_chunk_index
            END,
            status = CASE
                WHEN ingestion_state.file_hash != excluded.file_hash THEN 'PROCESSING'
                ELSE ingestion_state.status
            END,
            file_hash = excluded.file_hash
        '''
        self.cu.execute(query, (filepath, filehash,))
        self.cx.commit()
    
    def get_file_state(self, filepath:str)->Optional[dict]:
        file_obj = self._get_file(filepath)
        return file_obj
    
    def set_file_progress(self, filepath:str, chunk_index:int)->bool:
        query = "UPDATE ingestion_state SET status = 'PROCESSING', last_chunk_index = ? WHERE file_path = ? "
        self.cu.execute(query, (chunk_index, filepath,))
        self.cx.commit()
        return True
    
    def mark_completed(self, filepath:str)->bool:
        query = "UPDATE ingestion_state SET status = 'COMPLETED' WHERE file_path = ?"
        self.cu.execute(query, (filepath,))
        self.cx.commit()
        return True
        
    def _get_file(self, filepath:str)->Optional[dict]:
        query = "SELECT file_path, file_hash, last_chunk_index, status FROM ingestion_state WHERE file_path = ?"
        self.cu.execute(query, (filepath, ))
        return self.cu.fetchone()
