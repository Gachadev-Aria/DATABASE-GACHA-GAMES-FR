import os, sys, shutil


if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
    source_db_path = os.path.join(application_path, "app", "database", "gacha_games.db")
    source_json_path = os.path.join(application_path, "app", "fichier_code", "codes.json")
    source_para_json_path = os.path.join(application_path, "app", "parametres", "parametres.json")
    if os.name == 'nt':
        app_data_dir = os.path.join(os.environ['APPDATA'], "DATABSE")
    else:
        app_data_dir = os.path.join(os.path.expanduser("~"), ".config", "DATABASE")
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    source_db_path = os.path.join(application_path, "database", "gacha_games.db")
    source_json_path = os.path.join(application_path, "fichier_code", "codes.json")
    source_para_json_path = os.path.join(application_path, "parametres", "parametres.json")
    if os.name == 'nt':
        app_data_dir = os.path.join(os.environ['APPDATA'], "DATABASE")
    else:
        app_data_dir = os.path.join(os.path.expanduser("~"), ".config", "DATABASE")

dest_db_path = os.path.join(app_data_dir, "gacha_games.db")
dest_json_path = os.path.join(app_data_dir, "codes.json")
dest_para_json_path = os.path.join(app_data_dir, "parametres.json")

def init_files():
    os.makedirs(app_data_dir, exist_ok=True)
    if os.path.exists(dest_db_path) is False:
        if os.path.exists(source_db_path):
            shutil.copy2(source_db_path, dest_db_path)
        else:
            raise FileNotFoundError(f"Fichier source introuvable : {source_db_path}")

    if os.path.exists(dest_json_path) is False:
        if os.path.exists(source_json_path):
            shutil.copy2(source_json_path, dest_json_path)
        else:
            raise FileNotFoundError(f"Fichier source introuvable : {source_json_path}")
        
    if os.path.exists(dest_para_json_path) is False:
        if os.path.exists(source_para_json_path):
            shutil.copy2(source_para_json_path, dest_para_json_path)
        else:
            raise FileNotFoundError(f"Fichier source introuvable : {source_para_json_path}")
