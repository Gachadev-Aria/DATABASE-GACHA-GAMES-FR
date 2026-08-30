# Importations externes
import tkinter as tk
from tkinter import ttk, font
import json, os

# Importation interne
from app.config import dest_para_json_path

class FontChooserDialog:
    """
    Classe secondaire pour choisir la police 
    et la taille de police pour la DATABASE.
    """
    def __init__(self, parent: tk.Frame):
        """Fonction d'initialisation de la classe pour créer 
        la page tk.TopLevel et récupérer les polices disponibles 
        et les données enregistrées dans parametres.json"""
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Personnaliser la police")
        self.top.geometry("400x350")
        self.top.transient(parent)
        self.top.grab_set()

        self.parametres_path = dest_para_json_path
        
        with open(self.parametres_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.police = self.data.get('police et taille')

        # Variables pour stocker les choix de l'utilisateur
        self.font_family = tk.StringVar(value=self.police[0])
        self.font_size = tk.IntVar(value=self.police[1])

        # Liste des polices disponibles
        self.font_families = sorted(font.families())
        self.create_widgets()

    def create_widgets(self):
        """Fonction qui créer les widgets pour choisir la police."""
        # Frame pour la famille de police
        family_frame = tk.LabelFrame(self.top, text="Famille de police")
        family_frame.pack(fill="x", padx=10, pady=5)

        self.family_combobox = ttk.Combobox(family_frame, textvariable=self.font_family,
            values=self.font_families, state="readonly")
        self.family_combobox.pack(fill="x", padx=5, pady=5)

        # Frame pour la taille de police
        size_frame = tk.LabelFrame(self.top, text="Taille")
        size_frame.pack(fill="x", padx=10, pady=5)

        self.size_spinbox = ttk.Spinbox(size_frame, from_=8, to=72, textvariable=self.font_size)
        self.size_spinbox.pack(fill="x", padx=5, pady=5)

        # Aperçu de la police
        preview_frame = tk.LabelFrame(self.top, text="Aperçu")
        preview_frame.pack(fill="x", padx=10, pady=5)

        self.preview_label = tk.Label(
            preview_frame, 
            text="Ai-je versé cinq yoghourts aux\n kiwis sur de la pizza flambée ? \n - ×",
            font=self.police)
        self.preview_label.pack(pady=10)

        # Boutons de validation
        button_frame = tk.Frame(self.top)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.on_cancel).pack(side="right", padx=5)

        # Mise à jour de l'aperçu
        self.font_family.trace_add("write", self.update_preview)
        self.font_size.trace_add("write", self.update_preview)

    def update_preview(self, *args):
        """Fonction qui met à jour l'aperçu de la police."""
        font_config = (self.font_family.get(), self.font_size.get())
        self.preview_label.config(font=font_config)

    def on_ok(self):
        """Fonction qui valide le choix de la police."""
        self.result = [self.font_family.get(), self.font_size.get()]
        fichier_config = dest_para_json_path
        try:
            with open(fichier_config, "w", encoding="utf-8") as f:
                json.dump({"police et taille": self.result}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de la police: {e}")
        self.top.destroy()

    def on_cancel(self):
        """Fonction qui annule le choix de la police."""
        self.result = None
        self.top.destroy()

    def show(self):
        """Fonction qui affiche la boîte de dialogue et retourne le résultat."""
        self.parent.wait_window(self.top)
        return self.result
    
