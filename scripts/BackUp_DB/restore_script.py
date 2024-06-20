import os
import shutil
import stat

def on_rm_error(func, path, exc_info):
    # Modifikuoja failo teises, kad būtų galima ištrinti
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Nustatykite projekto katalogą ir atsarginės kopijos katalogą
project_dir = os.path.abspath('/Users/Projects/YourProject')
backup_dir = os.path.abspath('/Users/Projects/YourProject/scripts/backup_directory')

print(f"Projekto katalogas: {project_dir}")
print(f"Atsarginės kopijos katalogas: {backup_dir}")

# Gaukite visus atsarginių kopijų aplankus
backup_subdirs = [d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
backup_subdirs.sort(reverse=True)  # Rūšiuokite pagal laiką, kad naujausi atsirastų pirmieji

if not backup_subdirs:
    raise Exception(f"Nerasta jokių atsarginių kopijų {backup_dir}")

# Pasirinkite naujausią atsarginę kopiją
latest_backup = backup_subdirs[0]
latest_backup_dir = os.path.join(backup_dir, latest_backup)
print(f"Atstatoma iš atsarginės kopijos: {latest_backup_dir}")

# Kopijuokite failus iš atsarginės kopijos į projekto katalogą
for item in os.listdir(latest_backup_dir):
    source = os.path.join(latest_backup_dir, item)
    destination = os.path.join(project_dir, item)
    if os.path.isdir(source):
        # Jei tikslinis katalogas jau egzistuoja, ištrinkite jį prieš kopijuodami
        if os.path.exists(destination):
            shutil.rmtree(destination, onerror=on_rm_error)
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)

# Atkurkite duomenų bazės failą
db_file = os.path.join(latest_backup_dir, 'db.sqlite3')  # Pakeiskite šį kelią į savo duomenų bazės failo kelią
if os.path.exists(db_file):
    try:
        shutil.copy2(db_file, project_dir)
    except Exception as e:
        print(f"Error restoring database file {db_file} to {project_dir}: {e}")
else:
    print(f"Database file does not exist in backup: {db_file}")

print(f'Projektas atkurtas iš atsarginės kopijos: {latest_backup_dir}')
