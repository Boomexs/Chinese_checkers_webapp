import sqlite3
import json

class movedb_proxy:
    def __init__(self):
        self.connection = sqlite3.connect('../database/game_history.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                record TEXT NOT NULL
            )
        ''')
        self.connection.commit()
        return
    
    def __del__(self):
        self.connection.close()

    def get_id_list(self):
        self.cursor.execute('''
            SELECT game_id FROM games
        ''')
        ids = self.cursor.fetchall()
        id_list = [row[0] for row in ids]
        return id_list

    def add_game_record(self, start_board: list, moves: list):
        record = {
            'start_board': start_board,
            'moves': moves
        }
        record_as_text = json.dumps(record)
        self.cursor.execute('''
            INSERT INTO games (record)
                VALUES (?)
        ''',(record_as_text,))
        self.connection.commit()

    def get_game_record_by_id(self, id: int):
        self.cursor.execute('''
            SELECT record FROM games WHERE game_id = ?
        ''', (id,))
        record_as_db_entry = self.cursor.fetchall()
        record_as_text = [row[0] for row in record_as_db_entry]
        print(record_as_text[0])
        record = json.loads(record_as_text[0])
        return record
        
if __name__=="__main__":
    proxy = movedb_proxy()
    print('id list:',proxy.get_id_list())
    proxy.add_game_record([1,2,3,4,5,6,7,8,9],[[1,2],[3,4]])
    print('id list:',proxy.get_id_list())
    print('game moves:',proxy.get_game_record_by_id(1)['moves'])