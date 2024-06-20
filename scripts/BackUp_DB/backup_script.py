import os
import shutil
import datetime

# Nustatykite projekto katalogą ir atsarginės kopijos katalogą
project_dir = os.path.abspath('/Users/Projects/YourProject')
backup_dir = os.path.abspath('/Users/Projects/YourProject/scripts/backup_directory')

print(f"Projekto katalogas: {project_dir}")
print(f"Atsarginės kopijos katalogas: {backup_dir}")

# Patikrinkite, ar projektas egzistuoja
if not os.path.exists(project_dir):
    raise Exception(f"Projekto katalogas neegzistuoja: {project_dir}")

# Sukurkite atsarginės kopijos katalogą, jei jo nėra
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Sukurkite laiko žymę
timestamp = datetime.datetime.now().strftime('%m%d_%H-%M')

# Sukurkite atsarginės kopijos aplanką su laiko žyma
backup_subdir = os.path.join(backup_dir, f'backup_{timestamp}')
os.makedirs(backup_subdir)

# Kopijuokite projekto failus (išskyrus virtualią aplinką ir atsarginės kopijos aplanką)
excluded_dirs = ['.venv', 'backup_directory', 'scripts']
for item in os.listdir(project_dir):
    source = os.path.join(project_dir, item)
    destination = os.path.join(backup_subdir, item)
    if item not in excluded_dirs:  # Nurodykite katalogus, kurių nenorite kopijuoti
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")

# Eksportuokite duomenų bazę (pvz., SQLite)
db_file = os.path.join(project_dir, 'db.sqlite3')  # Pakeiskite šį kelią į savo duomenų bazės failo kelią
if os.path.exists(db_file):
    try:
        shutil.copy2(db_file, backup_subdir)
    except Exception as e:
        print(f"Error copying database file {db_file} to {backup_subdir}: {e}")
else:
    print(f"Database file does not exist: {db_file}")

print(f'Atsarginė kopija sukurta: {backup_subdir}')
