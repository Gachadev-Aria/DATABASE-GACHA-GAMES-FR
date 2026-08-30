# Imporataions externes
import sqlite3, os
from tkinter import ttk

# Importation interne
from app.config import dest_db_path

class DB():
    """Classe secondaire pour gérer la SQL Database."""
    def __init__(self):
        """Fonction d'initialisation de la classe pour créer la SQL Database"""
        db_path = os.path.join(os.path.dirname(__file__), "database", "gacha_games.db")
        self.conn = sqlite3.connect(dest_db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS GachaGames (
            CharacterId INTEGER PRIMARY KEY,
            CharacterName TEXT,
            Game TEXT,
            CharacterImage TEXT,
            DATE TEXT DEFAULT CURRENT_DATE
        );""")

        self.tables = ["GachaClub", "GachaLife2", "GachaNebula16", "GachaLife"]
        
        for table in self.tables:
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                CharacterId INTEGER PRIMARY KEY,
                CharacterName TEXT,
                CharacterImage TEXT,
                DATE TEXT DEFAULT CURRENT_DATE
            );""")

        self.conn.commit()
    
    def load_data(self, tree: ttk.Treeview, table: str):
        """
        Fonction permettant de remplir le tableau 
        avec les données de la table SQL.
        Args:
            tree: tableau à remplir.
            table: nom de la table SQL.
        """
        for item in tree.get_children():
            tree.delete(item)
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

    def update_db1(self, tableauGG: ttk.Treeview):
        """
        Fonction permettant de mettre à jour la table 
        SQL GachaGames de la SQL Database avec les lignes 
        du ttk.Treview tableauGG.
        Args:
            tableauGG:
        """
        self.cursor.execute("DELETE FROM GachaGames")
        for item in tableauGG.get_children():
            values = tableauGG.item(item, "values")
            if len(values) == 5:
                self.cursor.execute("""
                INSERT OR REPLACE INTO GachaGames (CharacterId, CharacterName, Game, CharacterImage, DATE)
                VALUES (?, ?, ?, ?, ?)
                """, values)
            elif len(values) == 4:
                self.cursor.execute("""
                INSERT OR REPLACE INTO GachaGames (CharacterId, CharacterName, Game, CharacterImage)
                VALUES (?, ?, ?, ?)
                """, values)
        self.conn.commit()

    def update_db2(self, tableauG_: ttk.Treeview, name_table: str):
        """
        Fonction permettant de mettre à jour la table 
        SQL Gacha____ de la SQL Database avec les lignes 
        du ttk.Treview tableauG_.
        Args:
            tableauG_:
        """
        self.cursor.execute(f"DELETE FROM {name_table}")
        for item in tableauG_.get_children():
            values = tableauG_.item(item, "values")
            if len(values) == 4:
                self.cursor.execute(f"""
                INSERT OR REPLACE INTO {name_table} (CharacterId, CharacterName, CharacterImage, DATE)
                VALUES (?, ?, ?, ?)
                """, values)
            elif len(values) == 3:
                self.cursor.execute(f"""
                INSERT OR REPLACE INTO {name_table} (CharacterId, CharacterName, CharacterImage)
                VALUES (?, ?, ?)
                """, values)
            self.conn.commit()

    def update_db(
            self, tableauGG: ttk.Treeview, tableauGC: ttk.Treeview, 
            tableauGN16: ttk.Treeview, tableauGL2: ttk.Treeview, 
            tableauGL: ttk.Treeview):
        """
        Fonction conteneur permettant de mettre à jour les tables 
        SQL GachaGames, GachaClub, GachaLife2, GachaNebula16,
        Gacha Life, de la SQL Database avec les ttk.Treview 
        tableauGG, tableauGC, tableauGL2, tableauGN16, tableauGL.
        Args:
            tableauGG: 
            tableauGC: 
            tableauGL: 
            tableauGL2: 
            tableauGN16:
        """
        self.update_db1(tableauGG)
        self.update_db2(tableauGC, "GachaClub")
        self.update_db2(tableauGL2, "GachaLife2")
        self.update_db2(tableauGN16, "GachaNebula16")
        self.update_db2(tableauGL, "GachaLife")

