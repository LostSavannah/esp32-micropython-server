import sqlite3
import time
import os
import hashlib

def get_checksum(data:bytes) -> str:
    return hashlib.md5(data).hexdigest()

class VersionManager:
    def __init__(self, root:str, database:str) -> None:
        self.root = root
        self.database = database

    def get_version(self, epoch:float = None) -> dict[str, str]:
        epoch = epoch or time.time()
        result = dict()
        query = """
        select v.* 
        from versions as v 
            join (
                select max(version_epoch) as epoch, 
                version_logic_path as logic_path 
                from 
                    versions 
                where 
                    version_epoch < ? 
                group by 
                    version_logic_path) as m 
                on 
                    m.epoch = v.version_epoch and 
                    m.logic_path = v.version_logic_path;"""
        with sqlite3.Connection(self.database) as connection:
            c = connection.execute(query, (epoch,))
            for r in c:
                result[r[2]] = r[0]
                print(r)
        return result

    def set_file(self, path:str, data:bytes) -> str:
        checksum = get_checksum(data)
        file_path = os.sep.join([self.root, checksum])
        moment = time.time()
        with open(file_path, 'wb') as fo:
            fo.write(data)
        query = "insert into versions VALUES (?, ?, ?);"
        with sqlite3.Connection(self.database) as connection:
            connection.execute(query, (checksum, moment, path))
        return checksum

    def get_file(self, path:str, epoch:float = None) -> bytes|None:
        versions = self.get_version(epoch)
        if path in versions:
            return self.get_by_hash(versions[path])
            
    def get_by_hash(self, hash:str) -> bytes|None:
        with open(os.sep.join([self.root, hash]), 'rb') as fi:
            return fi.read()