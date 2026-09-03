# Imports de modules externes
import tkinter as tk
from tkinter import messagebox, ttk
import json, pyperclip, os

# Imports de modules internes
from app.static.Listes import colonnes_GG, colonnes_G, colonnes_sqlG, colonnes_sqlGG, liste_all, games
from app.Fonctions import  build_OC, modifier_élément_ligne_OC, convertir, on_double_clic_secondaire
from app.Fonctions import trier_colonne, extraire_texte_depuis_json, new_scrollbar
from app.Fonctions import new_tableau, new_Notebook, remplir_tableau, choisir_couleur
from app.Fonctions import on_double_clic_principal, definir_police_color
from app.FontChooserDialog import FontChooserDialog
from app.GestionDB import DB
from app.config import dest_para_json_path, dest_json_path

class API():
    """Classe principale du logciel: l'interface."""
    def __init__(self, root):
        """
        Fonction d'initialisation de la classe pour créer l'interface, 
        récupérer les classes secondaires et les données de parametres.json.
        """
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.title("DATABASE GACHA GAMES")
        self.DataBase = DB()
        self.cursor = "star"
        self.FontChooserDialog = FontChooserDialog
        self.path1 = dest_para_json_path
        self.path2 = dest_json_path
        self.bg_color = extraire_texte_depuis_json(self.path1, "bg_color")
        self.btn_color = extraire_texte_depuis_json(self.path1, "btn_color")
        self.police = extraire_texte_depuis_json(self.path1, "police et taille")

        self.creer_API()
        self.load()

    def add(self):
        """
        Fonction conteneur permettant de mettre à jour 
        la SQL Database.
        """
        self.DataBase.add_db(self.tableauGG, self.tableauGC, self.tableauGN16, self.tableauGL2, self.tableauGL, self.tableauMM)
        
    def load(self):
        """
        Fonction conteneur pour charger les données 
        depuis la SQL Database dans les tk.Treeview.
        """
        self.DataBase.load_data(self.tableauGG, "GachaGames")
        self.DataBase.load_data(self.tableauGC, "GachaClub")
        self.DataBase.load_data(self.tableauGL2, "GachaLife2")
        self.DataBase.load_data(self.tableauGN16, "GachaNebula16")
        self.DataBase.load_data(self.tableauGL, "GachaLife")
        self.DataBase.load_data(self.tableauMM, "Minimuse")

    def remplir_tableaux(self):
        """
        Fonction conteneur pour remplir les tk.Treeview 
        après avoir ajouté, modifier ou supprimé un OC.
        """
        remplir_tableau(self.tableauGG, self.tableauGC, ["Gacha Plus", "Gacha Club", "Gacha Ultra", "Gacha Luminal", "Gacha Want", "Gacha Nox"])
        remplir_tableau(self.tableauGG, self.tableauGL2, ["Gacha Life 2", "Gacha Realms"])
        remplir_tableau(self.tableauGG, self.tableauGN16, "Gacha Nebula v1.6")
        remplir_tableau(self.tableauGG, self.tableauGL, ["Gacha Life", "Gachaverse"])
        remplir_tableau(self.tableauGG, self.tableauMM, "Minimuse")

    def creer_triof(self, page: tk.Frame):
        """
        Fonction permettant de créer un tk.Frame avec 3 tk.Button:
        -un pour fermer la page
        -un pour réduire la page
        -un pour ouvrir un site web.
        """
        self.triof = tk.Frame(page, bg=self.bg_color)
        self.triof.pack(side="right", anchor="nw", pady=2, padx=2)
        tk.Button(
            self.triof, text="  ×  ", background="#FF0000", foreground="#000000", 
            command=self.quit, relief="groove", font=self.police, cursor=self.cursor
            ).pack(side="right")
        tk.Button(
            self.triof, text="  -  ", background="#FFFFFF", foreground="#000000", 
            command=lambda: self.reduce(), relief="groove", font=self.police, cursor=self.cursor
            ).pack(side="right")
        tk.Button(
            self.triof, text="Besoin de convertir ?", bg='#FFFFFF', fg='black', font=self.police, 
            relief="groove", command=lambda: convertir(), cursor=self.cursor
            ).pack(side="right", pady=3, anchor='n')
        
    def reinitialiser(self):
        """
        Fonction permettant de réinitialiser l'interface 
        après la personnalisation de la DATABASE.
        """
        self.bg_color = extraire_texte_depuis_json(self.path1, "bg_color")
        self.police = extraire_texte_depuis_json(self.path1, "police et taille")
        self.btn_color = extraire_texte_depuis_json(self.path1, "btn_color")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.creer_API()
        self.load()

    def quit(self):
        """
        Fonction conteneur permettant de quitter la DATABASE 
        et de fermer la connection à la SQL Database.
        """
        self.DataBase.conn.close()
        self.root.destroy()

    def reduce(self):
        """Fonction conteneur permettant de réduire la page."""
        self.root.iconify()

    def choisir_police(self, parent: tk.Frame):
        """Fonction conteneur qui ouvre une boîte de 
        dialogue pour choisir une police.
        """
        dialog = self.FontChooserDialog(parent)
        return dialog.show()

    def personnaliser(self, parent: tk.Frame):
        """Fonction conteneur pour personnaliser la DATABASE et ensuite réinitialiser"""
        self.choisir_police(parent)
        choisir_couleur("bg")
        choisir_couleur("btn")
        self.reinitialiser()
    
    def creer_API(self):
        """Fonction principale de la classe API pour créer l'interface"""
        used_ids = set()

        def ajouter_oc():
            """
            Fonction conteneur permettant d'ajouter une ligne (un OC) 
            dans le tk.Treeview tableau_GG, le tableau principal.
            """
            next_id = 1
            while next_id in used_ids:
                next_id += 1
            build_OC(self.pageGG, self.tableauGG, self.bg_color, self.btn_color, self.police, next_id)
            used_ids.add(next_id)
            self.remplir_tableaux()
            self.add()

        def supprimer_OC(tableauGG: ttk.Treeview, tableauGC: ttk.Treeview, 
                         tableauGN16: ttk.Treeview, tableauGL2: ttk.Treeview, 
                         tableauGL: ttk.Treeview) -> int:
            """
            Fonction permettant de supprimer une ligne (un OC) dans le 
            tk.Treeview tableauGG, le tableau principal et dans 
            les tk.Treeview tableauGC, tableauGN16, tableauGL2, tableauGL
            selon la ligne supprimée dans le tk.Treeview tableauGG.
            Args:
                tableauGG: tableau principal Gacha Games.
                tableauGL: tableau principal Gacha Life.
                tableauGC: tableau secondaire Gacha Club et ses mod.
                tableauGN16: tableau secondaire Gacha Nebula v1.6.
                tableauGL2: tableau secondaire Gacha Life 2 et ses mod.
                tableauMM: tableau secondaire Minimuse.
            Returns:
                a: l'Id de l'OC supprimé.
            """
            ligne_select1 = tableauGG.selection()
            if not ligne_select1:
                messagebox.showerror("Réessaye", "Sélectionne un OC à supprimer.", icon='error')
                return
            a = tableauGG.item(ligne_select1, "values")[0]
            
            response = messagebox.askyesno("Mais ?...", "Veux-tu vraiment supprimer cet OC ?", icon="question")

            if response == True:
                tableauGG.delete(ligne_select1)
                tableaux= [tableauGC, tableauGN16, tableauGL2, tableauGL]
                for tableau in tableaux:
                    for item in tableau.get_children():
                        values = tableau.item(item, "values")
                        if values[0] == int(a) or values[0] == str(a):
                            tableau.delete(item)
            
                with open(self.path2, "r", encoding="utf-8") as f:
                    codes = json.load(f)
                del codes[values[0]]
                with open(self.path2, "w", encoding="utf-8") as f:
                    json.dump(codes, f, ensure_ascii=False, indent=4)
                used_ids.discard(int(a))
            return a

        def supprimer_oc():
            """
            Fonction conteneur permettant de:
            -supprimer une ligne (un OC) dans le tk.Treeview tableauGG, 
            le tableau principal et dans les tk.Treeview tableauGC, 
            tableauGN16, tableauGL2, tableauGL selon la ligne supprimée 
            dans le tk.Treeview tableauGG
            -(re)remplir les tk.Treeview tableauGC, tableauGN16, tableauGL2, tableauGL
            -mettre à jour la SQL Database.
            """
            id = supprimer_OC(self.tableauGG, self.tableauGC, self.tableauGN16, self.tableauGL2, self.tableauGL, self.tableauMM)
            self.DataBase.delete_db(id)

        def modifier_élément_oc():
            """
            Fonction conteneur permettant de:
            -modifier une ligne (un OC) dans le tk.Treeview tableauGG, 
            le tableau principal et dans les tk.Treeview tableauGC, 
            tableauGN16, tableauGL2, tableauGL selon la ligne supprimée 
            dans le tk.Treeview tableauGG.
            -(re)remplir les tk.Treeview tableauGC, tableauGN16, tableauGL2, tableauGL
            -mettre à jour la SQL Database.
            """
            modifier_élément_ligne_OC(self.tableauGG, self.Notebook, self.bg_color, self.btn_color, self.police)
            self.remplir_tableaux()
            self.add()

        def copier_code(tableau: ttk.Treeview):
            """
            Fonction permettant de copier le code de l'OC (la ligne) sélectionné.
            Args:
                tableau: tableau depuis lequel l'OC (la ligne) a été sélectionné.
            """
            ligne_select = tableau.selection()
            if len(tableau.item(ligne_select, "values")) == 4:
                a, _, _, _ = tableau.item(ligne_select, "values")
            elif len(tableau.item(ligne_select, "values")) == 5:
                a, _, _, _, _ = tableau.item(ligne_select, "values")
            if not ligne_select:
                messagebox.showerror("Réessaye", "Sélectionne un OC dont il faut copier le code.", icon='error')
                return   
            path = os.path.join(os.path.dirname(__file__), "fichier_code", "codes.json")  
            with open(path, "r", encoding="utf-8") as f:
                codes = json.load(f)
            code = codes.get(a)
            if code:
                pyperclip.copy(code)
                messagebox.showinfo("Yeah !", "Code offline de l'OC copié !", icon='info')

        self.pageBG = tk.Canvas(self.root, background=self.bg_color)
        self.pageBG.pack(fill='both', expand=True)

        self.creer_triof(self.pageBG)

        tk.Label(self.pageBG, text="DATABASE GACHA GAMES", bg=self.bg_color, font=self.police).pack(side=tk.TOP, pady=5)

        self.page_conteneur = tk.Frame(self.pageBG, bg=self.bg_color)
        self.page_conteneur.pack(fill='y', expand=True, anchor='w', side='left')
        
        self.Notebook, self.pages = new_Notebook(self.page_conteneur, liste_all, self.bg_color, self.btn_color, self.police)

        self.pageGG = self.pages["Gacha Games"]
         self.pageGL = self.pages["GL"]
        self.pageGC = self.pages["GC"]
        self.pageGL2 = self.pages["GL2"]
        self.pageGN16 = self.pages["GN"]
        self.pageMM = self.pages["MM"]

        self.tableauGG = new_tableau(self.pageGG, self.police, self.bg_color, colonnes_GG, colonnes_sqlGG, 200, trier_colonne)
        self.tableauGG.bind("<Double-1>", lambda event: on_double_clic_principal(self.tableauGG, self.ImageOC))
        self.tableauGL = new_tableau(self.pageGL, self.police, self.bg_color, colonnes_G, colonnes_sqlG, 230, trier_colonne)
        self.tableauGL.bind("<Double-1>", lambda event: on_double_clic_secondaire(self.tableauGL,self.ImageOC))
        self.tableauGC = new_tableau(self.pageGC, self.police, self.bg_color, colonnes_G, colonnes_sqlG, 230, trier_colonne)
        self.tableauGC.bind("<Double-1>", lambda event: on_double_clic_secondaire(self.tableauGC,self.ImageOC))
        self.tableauGL2 = new_tableau(self.pageGL2, self.police, self.bg_color, colonnes_G, colonnes_sqlG, 230, trier_colonne)
        self.tableauGL2.bind("<Double-1>", lambda event: on_double_clic_secondaire(self.tableauGL2, self.ImageOC))
        self.tableauGN16 = new_tableau(self.pageGN16, self.police, self.bg_color, colonnes_G, colonnes_sqlG, 230, trier_colonne)
        self.tableauGN16.bind("<Double-1>", lambda event: on_double_clic_secondaire(self.tableauGN16, self.ImageOC))
        self.tableauMM = new_tableau(self.pageMM, self.police, self.bg_color, colonnes_G, colonnes_sqlG, 230, trier_colonne)
        self.tableauMM.bind("<Double-1>", lambda event: on_double_clic_secondaire(self.tableauMM, self.ImageOC))
        
        new_scrollbar(self.tableauGG)
        new_scrollbar(self.tableauGL)
        new_scrollbar(self.tableauGC)
        new_scrollbar(self.tableauGL2)
        new_scrollbar(self.tableauGN16)
        new_scrollbar(self.tableauMM)

        self.FrameBtn = tk.Frame(self.pageGG, bg=self.bg_color)
        self.FrameBtn.pack(side="top")

        self.btn_add = tk.Button(
            self.FrameBtn, text="Ajouter un OC", bg=self.btn_color, fg=definir_police_color(self.btn_color), 
            font=self.police, command=ajouter_oc, cursor=self.cursor)
        self.btn_add.pack(side="left", padx=3, pady=3, anchor='n')
        self.btn_delete = tk.Button(
            self.FrameBtn, text="Supprimer un OC", bg=self.btn_color, fg=definir_police_color(self.btn_color), 
            font=self.police, command=supprimer_oc, cursor=self.cursor)
        self.btn_delete.pack(side="left", padx=3, pady=3, anchor='n')
        self.btn_modify = tk.Button(
            self.FrameBtn, text="Changer un OC", bg=self.btn_color, fg=definir_police_color(self.btn_color), 
            font=self.police, command=modifier_élément_oc, cursor=self.cursor)
        self.btn_modify.pack(side="left", padx=3, pady=3, anchor='n')
        self.btn_customize = tk.Button(
            self.FrameBtn, text="Personnaliser DATABASE", bg=self.btn_color, fg=definir_police_color(self.btn_color), 
            font=self.police, command=lambda: self.personnaliser(self.pageGG), cursor=self.cursor
            )
        self.btn_customize.pack(side="left", padx=3, pady=3, anchor='n')

        self.listgames = tk.LabelFrame(
            self.page_conteneur, text="Liste des Jeux Gacha", font=self.police, height=200, width=300, bg=self.bg_color,
            borderwidth=3, border=3, fg=definir_police_color(self.bg_color))
        self.listgames.pack()

        text_games = "   ".join(games[0:4]) + "\n\n" + "   ".join(games[4:8]) + "\n\n" + "    ".join(games[8:12])

        tk.Label(self.listgames, text=text_games, font=self.police, bg=self.bg_color, fg=definir_police_color(self.bg_color)).pack(padx=5, pady=5)

        self.page_conteneur2 = tk.Frame(self.pageBG, bg=self.bg_color)
        self.page_conteneur2.place(x=1510, y=65, anchor='ne')  
        self.ImageOC = tk.LabelFrame(
            self.page_conteneur2, text="Image de l'OC sélectionné", font=self.police, height=687, width=620, bg=self.bg_color,
            borderwidth=3, border=3, fg=definir_police_color(self.bg_color))
        self.ImageOC.pack(side='top')
        tk.Button(
            self.page_conteneur2, text="Copier le code", bg=self.btn_color, fg=definir_police_color(self.btn_color), 
            font=self.police, command=lambda: copier_code(self.tableauGG)
            ).pack(side="bottom", padx=3, pady=3, anchor='center')
