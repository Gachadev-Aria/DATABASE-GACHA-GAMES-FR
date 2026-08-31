# Importations externes
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, filedialog, messagebox, colorchooser
import json, os, webbrowser
from PIL import Image, ImageTk
from colour import Color
from color_contrast import AccessibilityLevel, check_contrast
from random import choice

# Importations internes
from app.static.Listes import list_games, colonnes_GG, colonnes_sqlGG
from app.config import dest_json_path, init_files, dest_para_json_path

init_files()

with open(dest_json_path, "r") as f:
    codes = json.load(f)

# Composants pour l'API

def new_scrollbar(tableau: ttk.Treeview):
    """
    Fonction containeur permettant de créer un ttk.Scrollbar 
    pour un ttk.Treeview.
    Args:
        tableau:
    """
    scrollbar = ttk.Scrollbar(tableau, orient=tk.VERTICAL, command=tableau.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tableau.configure(yscroll=scrollbar.set)
    return scrollbar

def new_tableau(page: tk.Frame, police: tuple[str, int], bg_color: str, colonnes: list[str], colonnesSQL: list[str], a: int, fct):
    """
    Fonction conteneur permettant de créer un ttk.Treview dans 
    le tk.Frame du tk.Notebook.
    Args:
        page: page dans lequel la tableau sera placé.
        police: famille et taille de police.
        bg_color: couleur de l'arrière-plan de l'interface.
        colonne: liste des noms des en-têtes pour le tableau.
        colonneSQL: liste des noms des colonnes des tables SQL secondaires.
        a: ipady du tableau.
        fct: fonction liée aux en-têtes du tableau.
    """
    tableau = ttk.Treeview(page, columns=colonnesSQL, show="headings")
    style = ttk.Style()
    style.configure(
        "Treeview.Heading",
        background="white",  
        foreground="black",   
        font=police,  
        rowheight=40, 
        borderwidth=1, relief="solid"        
        )
    
    style.map(
        "Treeview",
        background=[("selected", bg_color)],  # Couleur de fond des lignes sélectionnées
        foreground=[("selected", definir_police_color(bg_color))]    # Couleur du texte des lignes sélectionnées
    )
    
    for col1, col2 in zip(colonnes, colonnesSQL):
        tableau.heading(col2, text=col1, command= lambda: fct(tableau, True))
        tableau.column(col2, width=len(col1)*2, anchor=tk.CENTER)
    tableau.pack(fill='both', pady=10, ipady=a, side="top")
    return tableau

def new_Notebook(parent: tk.Frame, pages_names: list[str], bg_color: str, btn_color:str, police: tuple[str, int]):
    """
    Fonction conteneur permettant de créer le tk.Notebook.
    Args:
        parent: page dans lequel le tk.Notebook sera placé.
        pages_names: liste des noms des pages du tk.Notebook.
        bg_color: couleur de l'arrière-plan de l'interface.
        btn_color: couleur des boutons de l'interface.
        police: nom et taille de police.
    """
    Notebook = ttk.Notebook(parent)
    style = ttk.Style()
    style.theme_use("clam") 
    style.configure("TNotebook", background=bg_color, padding=[10, 5])
    
    style.configure(
        "TNotebook.Tab",
        background=btn_color,  
        foreground=definir_police_color(btn_color),   
        font=(police[0], police[1]-2),           
        padding=[10, 5],       
        borderwidth=2,         
        relief="solid",        
        lightcolor=bg_color,  
        darkcolor=btn_color,
    )

    style.map(
        "TNotebook.Tab",
        background=[("selected", bg_color)], 
        foreground=[("selected", definir_police_color(btn_color))],  
        relief=[("selected", "groove")]          
    )

    style.map(
        "TNotebook.Tab",
        background=[("active", btn_color)],
        relief=[("active", "raised")]         
        )
    
    style.configure("TFrame", background=bg_color)

    Notebook.pack(fill='both', pady=10, padx=10)

    pages = {}
    for name in pages_names:
        page = ttk.Frame(Notebook)
        Notebook.add(page, text=name)
        pages[name] = page

    return Notebook, pages

def Top_level_build_oc(page: tk.Frame, bg_color: str, btn_color: str, police: tuple[str, int]):
    """
    Fonction permettant de créer une page de formulaire 
    pour ajouter un OC (une ligne).
    Args:
        page: page depuis le tk.TopLevel va s'ouvrir.
        bg_color: couleur de l'arrière-plan de l'interface.
        bg_color: couleur des tk.Button de l'interface.
        police: nom et taille de police.
    """
    dialog = tk.Toplevel(page, relief='raised', bg=bg_color)
    dialog.title("Nouvel OC")
    dialog.grab_set()
    dialog.geometry("600x700")

    result = {}

    main_frame = tk.Frame(dialog, bg=bg_color)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    titre_nom_oc = tk.LabelFrame(main_frame, text="Nom de l'OC", font=police, bg=bg_color)
    titre_nom_oc.pack(fill="x", pady=5)

    nom_oc_var = tk.StringVar()
    nom_oc_entry = tk.Entry(titre_nom_oc, textvariable=nom_oc_var, width=30, font=police)
    nom_oc_entry.pack(padx=10, pady=5)

    titre_choix = tk.LabelFrame(main_frame, text="Jeux", font=police, bg=bg_color)
    titre_choix.pack(fill="x", pady=5)

    liste = tk.Listbox(titre_choix, height=4, selectmode=tk.SINGLE, font=police)
    for jeu in list_games:
        liste.insert(tk.END, jeu)
    liste.pack(fill="x", padx=10, pady=5)

    titre_champ_texte = tk.LabelFrame(main_frame, text="Code de l'OC", font=police, bg=bg_color)
    titre_champ_texte.pack(fill="both", expand=True, pady=5)

    champ_texte = tk.Text(
        titre_champ_texte, bd=4, width=70, height=15, font=police, background='white')
    champ_texte.pack(fill="both", expand=True, padx=10, pady=5)

    button_frame = tk.Frame(main_frame, bg=bg_color)
    button_frame.pack(fill="x", pady=10)

    def save_and_close():
        result["nom"] = nom_oc_var.get()
        result["code"] = champ_texte.get("1.0", tk.END).strip()
        result["jeu"] = liste.get(tk.ACTIVE) if liste.curselection() else ""
        dialog.destroy()

    ok_btn = tk.Button(
        button_frame, text="Valider", bg=btn_color, fg=definir_police_color(btn_color), 
        font=police, command=save_and_close)
    ok_btn.pack(side=tk.RIGHT, padx=5)

    cancel_btn = tk.Button(
        button_frame, text="Annuler", bg=btn_color, fg=definir_police_color(btn_color), 
        font=police, command=dialog.destroy)
    cancel_btn.pack(side=tk.RIGHT, padx=5)

    page.wait_window(dialog)

    if result == {}: 
        return None
    else:
        return result

def Top_level_modifier_oc(page: tk.Frame, bg_color: str, btn_color: str, police: tuple[str, int], choix: int, ID: int):
    """
    Fonction permettant de créer une page de formulaire 
    pour modifier un OC (une ligne) selon ce que l'on veut modifier.
    Args:
        page: page depuis le tk.TopLevel va s'ouvrir.
        bg_color: couleur de l'arrière-plan de l'interface.
        btn_color: couleur des tk.Button de l'interface.
        police: nom et taille de police.
        choix: ce qu'on veut modifier.
        ID: numéro de l'OC (la ligne) qu'on veut modifier.
    """
    result = {}

    if choix != 3:
        dialog = tk.Toplevel(page, relief='raised', bg=bg_color)
        dialog.grab_set()
        main_frame = tk.Frame(dialog, bg=bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if choix == 1:
            dialog.title("Modifier le nom de l'OC")
            dialog.geometry("600x150")
            titre_nom_oc = tk.LabelFrame(main_frame, text="Nom de l'OC", font=police, bg=bg_color)
            titre_nom_oc.pack(fill="x", pady=5)
        
            nom_oc_var = tk.StringVar()
            nom_oc_entry = tk.Entry(titre_nom_oc, textvariable=nom_oc_var, width=30, font=police)
            nom_oc_entry.pack(padx=10, pady=5)

            def save_and_close():
                result["new_info"] = nom_oc_var.get()
                dialog.destroy()

        elif choix == 2:
            dialog.title("Modifier l'origine de l'OC")
            dialog.geometry("600x400")
            titre_choix = tk.LabelFrame(main_frame, text="Jeux", font=police, bg=bg_color)
            titre_choix.pack(fill="x", pady=5)
            liste = tk.Listbox(titre_choix, height=4, selectmode=tk.SINGLE, font=police)
            for jeu in list_games:
                liste.insert(tk.END, jeu)
            liste.pack(fill="x", padx=10, pady=5)

            def save_and_close():
                result["new_info"] = liste.get(tk.ACTIVE) if liste.curselection() else ""
                dialog.destroy()

        elif choix == 4:
            dialog.title("Modifier le code de l'OC")
            dialog.geometry("600x600")
            titre_champ_texte = tk.LabelFrame(
                main_frame, text="Nouveau code de l'OC", font=police, bg=bg_color)
            titre_champ_texte.pack(fill="both", expand=True, pady=5)
            champ_texte = tk.Text(
                titre_champ_texte, bd=4, width=70, height=15, font=police, background='white')
            champ_texte.pack(fill="both", expand=True, padx=10, pady=5)
            
            def save_and_close():
                codes[str(ID)] = champ_texte.get("1.0", tk.END).strip()
                dialog.destroy()

        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill="x", pady=10)

        ok_btn = tk.Button(
            button_frame, text="Valider", bg=btn_color, fg=definir_police_color(btn_color), 
            font=police, command=save_and_close)
        ok_btn.pack(side=tk.RIGHT, padx=5)
    
        cancel_btn = tk.Button(
            button_frame, text="Annuler", bg=btn_color, fg=definir_police_color(btn_color), 
            font=police, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
        page.wait_window(dialog)

        if result == {}:
            return None
        else:
            return result["new_info"]
    
    else:
        result = filedialog.askopenfilename(title="Choisissez la nouvelle image")
        if result == {}:
            return None
        else: 
            return result


def creer_canvas(chemin: str, page_parent: tk.LabelFrame):
    """
    Fonction permettant de créer un canvas avec 
    l'image de l'OC choisi auparavant.
    Args:
        chemin: chemin de l'image.
        page_parent: tk.LabelFrame qui contiendra l'image.
    Returns:
        canvas ou non.
    """
    if chemin == 'i':
        return None
    else:
        canvas = tk.Canvas(page_parent, width=610, height=657, bg='white')
        canvas.pack(fill='both', expand=True)

        image = Image.open(chemin)
        if ImageTk.PhotoImage(image).width() == 1000 and ImageTk.PhotoImage(image).height() == 1000:
            image.thumbnail((600, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(310, 300, image=photo, anchor="center")
        elif ImageTk.PhotoImage(image).width() == 850 and ImageTk.PhotoImage(image).height() == 500:
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(310, 300, image=photo, anchor="center")
        elif ImageTk.PhotoImage(image).width() == 1920 and ImageTk.PhotoImage(image).height() == 1020:
            image.thumbnail((1920, 700), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(310, 300, image=photo, anchor="center")
        elif ImageTk.PhotoImage(image).width() == 1560 and ImageTk.PhotoImage(image).height() == 720:
            image.thumbnail((1920, 700), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(310, 300, image=photo, anchor="center")
        elif ImageTk.PhotoImage(image).width() == 720 and ImageTk.PhotoImage(image).height() == 1600:
            image.thumbnail((500, 1500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(310, 280, image=photo, anchor="center")
        canvas.image = photo

        return canvas


# Fonctions concernants les tableaux
def build_OC(page: tk.Frame, tableauGG: ttk.Treeview, bg_color: str, btn_color: str, police: tuple[str, int], ID: int):
    """
    Fonction permettant d'ajouter un OC (une ligne) dans le tk.Treview tableauGG.
    Args:
        page: page depuis le tk.TopLevel va s'ouvrir.
        tableauGG:
        bg_color: couleur de l'arrière-plan de l'interface.
        btn_color: couleur des tk.Button de l'interface.
        police: nom et taille de police.
        ID: nouveau numéro de l'OC (la ligne) à ajouter 
    """

    data = Top_level_build_oc(page, bg_color, btn_color, police)
    if data is None:
        return
    else:
        nom_oc = data.get('nom')
        code_oc = data.get('code')
        game_oc = data.get('jeu')
        
        if not nom_oc:
            messagebox.showerror("Alors...", "Renseigne au moins un nom.", icon='error')
            return None

        codes[str(ID)] = code_oc.strip()

        with open(dest_json_path, "w", encoding="utf-8") as f:
            json.dump(codes, f, ensure_ascii=False, indent=4)   

        chemin = filedialog.askopenfilename(title="Choisis l'image de l'OC")
        if chemin:  
            infos = {"Nom": nom_oc, "Game": game_oc, "Image": chemin}
        else:  
            infos = {"Nom": nom_oc, "Game": game_oc, "Image": "i"}

        tableauGG.insert("", tk.END, values=(ID, infos["Nom"], infos["Game"], infos["Image"]))

def modifier_élément_ligne_OC(tableauGG: ttk.Treeview, page: tk.Frame, bg_color: str, btn_color: str, police: tuple[str, int]):
    """
    Fonction permettant de modifier un OC (une ligne) dans le tk.Treeview tableauGG.
    Args:
        tableauGG:
        page: page depuis le tk.TopLevel va s'ouvrir.
        bg_color: couleur de l'arrière-plan de l'interface.
        btn_color: couleur des tk.Button de l'interface.
        police: nom et taille de police.
    """

    ligne_select = tableauGG.selection()
    if not ligne_select:
        messagebox.showerror("Bah ?", "Sélectionne un OC à modifier.", icon='error')
        return

    élément = ligne_select[0]
    éléments = tableauGG.item(élément, "values")
    id = éléments[0]

    choix = simpledialog.askinteger(
        "Modifier une information",
        "Quelle colonne voulez-vous modifier ?\n"
        "1. Nom\n"
        "2. Jeux\n"
        "3. Image\n"
        "4. Code\n\n"
        "(Entrez un nombre entre 1 et 4)",
        minvalue=1,
        maxvalue=4
    )

    if not choix:
        return

    new_info = None
    new_info = Top_level_modifier_oc(page, bg_color, btn_color, police, choix, id)

    if new_info is not None and choix:
        info_new = list(éléments)
        info_new[choix] = new_info
        tableauGG.item(élément, values=tuple(info_new))

def trier_colonne(tableau, inverse: bool):
    """
    Fonction permettant de trier le tableau par ordre alphabétique 
    selon la colonne sélectionnée.
    Args:
        tableau: 
        inverse: "True"
    """
    enfants = tableau.get_children("")
    data = []
    for enfant in enfants:
        valeurs = tableau.item(enfant, "values")
        data.append((valeurs, enfant))

    # Trie les données selon les valeurs des colonnes
    def cle_tri(item):
        return tuple(
            int(val) if val.isdigit() else val.lower()
            for val in item[0]
        )

    data.sort(reverse=inverse, key=cle_tri)

    # Réorganise les lignes dans le tableau
    for index, (valeurs, enfant) in enumerate(data):
        tableau.move(enfant, "", index)

    # Met à jour l'en-tête pour le prochain tri
    for col1, col2 in zip(colonnes_GG, colonnes_sqlGG):
        tableau.heading(col2, text=col1, command=lambda: trier_colonne(tableau, not inverse))

def remplir_tableau(tableauGG: ttk.Treeview, tableauG_: ttk.Treeview, jeu: str):
    """
    Fonction permettant de remplir le tk.Treview tableauG_ 
    à partir des lignes du tk.Treview tableauGG.
    Args:
        tableauGG:
        tableauG:
        jeu: nom du jeu.
    """
    for item in tableauG_.get_children():
        tableauG_.delete(item)
    for item in tableauGG.get_children():
        if len(tableauGG.item(item, "values")) == 4:
            a, b, c, d  = tableauGG.item(item, "values")
            new_tuple = a, b, d
        elif len(tableauGG.item(item, "values")) == 5:
            a, b, c, d, e  = tableauGG.item(item, "values")
            new_tuple = a, b, d, e
        if jeu == c or c in jeu:
            tableauG_.insert("", "end", values=new_tuple)


def on_double_clic_principal(tableauGG, ImageOC: tk.LabelFrame):
    """
    Fonction permettant de supprimer ce qui existe dans le 
    tk.LabelFrame ImageOC et d'afficher ou non l'image de l'OC.
    Args:
        tableauGG:
        master: page qui va acceuillir l'image de l'OC.
    """
    for widget in ImageOC.winfo_children():
        widget.destroy()
    ligne_select = tableauGG.selection()
    if len(tableauGG.item(ligne_select, "values")) == 5:
        _, _, _, chemin, _ = tableauGG.item(ligne_select, "values")
    elif len(tableauGG.item(ligne_select, "values")) == 4:
        _, _, _, chemin = tableauGG.item(ligne_select, "values")
    creer_canvas(chemin, ImageOC)

def on_double_clic_secondaire(tableauG_: ttk.Treeview, ImageOC: tk.LabelFrame):
    """
    Fonction permettant de supprimer ce qui existe dans le 
    tk.LabelFrame ImageOC et d'afficher ou non l'image de l'OC.
    Args:
        tableauGG:
        master: page qui va acceuillir l'image de l'OC.
    """    
    for widget in ImageOC.winfo_children():
        widget.destroy()
    
    ligne_select = tableauG_.selection()
    if len(tableauG_.item(ligne_select, "values")) == 4:
        _, _, chemin, _ = tableauG_.item(ligne_select, "values")
    elif len(tableauG_.item(ligne_select, "values")) == 3:
        _, _, chemin = tableauG_.item(ligne_select, "values")
    creer_canvas(chemin, ImageOC)


# Autres fonctions
def choisir_couleur(type: str):
    """
    Fonction permettant d'ouvrir une fenêtre pour 
    sélectionner une couleur soit pour l'arrière-plan
    soit pour les boutons et de l'enregister dans parametres.json.
    Args:
        type: 'bg' pour la couleur de l'arrière-pla, 'btn' pour la couleur des boutons.
    """
    if type == 'bg':
        couleur = colorchooser.askcolor(title="Choisir la couleur de l'arrière-plan")
    elif type == 'btn':
        couleur = colorchooser.askcolor(title="Choisir la couleur des boutons")
    if couleur[1]:
        try:
            with open(dest_para_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if type == 'bg':
                data["bg_color"] = couleur[1]
            elif type == 'btn':
                data["btn_color"] = couleur[1]
            with open(dest_para_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de la couleur: {e}")

def extraire_texte_depuis_json(chemin, name):
    """Fonction permettant d'extraire le texte d'un fichier JSON."""
    try:
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                config = json.load(f)
                t = config.get(name, "")
        return t
    except FileNotFoundError:
        print(f"Erreur : Le fichier {chemin} est introuvable.")
        return []
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {chemin} n'est pas un JSON valide.")
        return []
    except KeyError:
        print("Erreur : Le champ '{chemin}' ou '{name}' est manquant dans le fichier JSON.")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []

def convertir():
    """Fonction permettant d'accéder au site web de conversion."""
    webbrowser.open("https://convertisseur-codes-gacha.onrender.com/")

def definir_police_color(bg: str) -> str:
    """
    Fonction permettant de choisir entre le noir et 
    le blanc pour la couleur de la police d'écriture
    selon le contraste avec la couleur de l'arrière-plan ou des tk.Button.
    Args:
        bg: couleur de l'arrière-plan ou des tk.Button
    Returns:
        couleur: couleur du texte.
    """
    new_bg = Color(bg)
    noir = check_contrast('#000000', new_bg, level=AccessibilityLevel.AA18)
    blanc = check_contrast("#FFFFFF", new_bg, level=AccessibilityLevel.AA18)
    if noir is True:
        return '#000000'
    elif blanc is True:
        return '#FFFFFF'
    elif noir is True and blanc is True or noir is False and blanc is False:
        return choice([blanc, noir])
