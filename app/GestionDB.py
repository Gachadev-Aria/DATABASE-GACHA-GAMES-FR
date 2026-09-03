# Imporataions externes
import sqlite3
from tkinter import ttk

# Importation interne
from app.config import dest_db_path

class DB():
    """Classe secondaire pour gérer la SQL Database."""
    def __init__(self):
        """Fonction d'initialisation de la classe pour créer la SQL Database"""
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

        self.tables = ["GachaClub", "GachaLife2", "GachaNebula16", "GachaLife", "Minimuse"]
        
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

    def add_db1(self, tableauGG: ttk.Treeview):
        """
        Fonction permettant d'ajouter des données dans la table 
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

    def add_db2(self, tableauG: ttk.Treeview, name_table: str):
        """
        Fonction permettant d'ajouter des données dans la table 
        SQL Gacha____ de la SQL Database avec les lignes 
        du ttk.Treview tableauG.
        Args:
            tableauG:
        """
        self.cursor.execute(f"DELETE FROM {name_table}")
        for item in tableauG.get_children():
            values = tableauG.item(item, "values")
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

    def add_db(
            self, tableauGG: ttk.Treeview, tableauGC: ttk.Treeview, 
            tableauGN16: ttk.Treeview, tableauGL2: ttk.Treeview, 
            tableauGL: ttk.Treeview, tableauMM: ttk.Treeview):
        """
        Fonction conteneur permettant d'ajouter des données dans les tables 
        SQL GachaGames, GachaClub, GachaLife2, GachaNebula16,
        Gacha Life, Minimuse, de la SQL Database avec les ttk.Treview 
        tableauGG, tableauGC, tableauGL2, tableauGN16, tableauGL, tableauMM.
        Args:
            tableauGG: 
            tableauGC: 
            tableauGL: 
            tableauGL2: 
            tableauGN16:
            tableauMM:
        """
        self.add_db1(tableauGG)
        self.add_db2(tableauGC, "GachaClub")
        self.add_db2(tableauGL2, "GachaLife2")
        self.add_db2(tableauGN16, "GachaNebula16")
        self.add_db2(tableauGL, "GachaLife")
        self.add_db2(tableauMM, "Minimuse")

    def delete_db(self, id: int):
        """
        Fonction permettant de supprimer un élément de la SQL Database.
        Args:
            id: l'Id de l'OC à supprimer.
        """
        self.cursor.execute("DELETE FROM GachaGames WHERE CharacterId = ?", (id,))
        self.cursor.execute("DELETE FROM GachaClub WHERE CharacterId = ?", (id,))
        self.cursor.execute("DELETE FROM GachaLife2 WHERE CharacterId = ?", (id,))
        self.cursor.execute("DELETE FROM GachaNebula16 WHERE CharacterId = ?", (id,))
        self.cursor.execute("DELETE FROM GachaLife WHERE CharacterId = ?", (id,))
        self.cursor.execute("DELETE FROM Minimuse WHERE CharacterId = ?", (id,))
        self.conn.commit()
