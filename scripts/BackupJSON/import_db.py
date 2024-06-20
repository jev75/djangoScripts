import os
import sys
import django
from django.core import serializers
from django.db import transaction
from django.apps import apps

def import_app_data_from_json(app_label, file_path):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Pakeiskite į savo projekto nustatymų failą

    django.setup()

    try:
        app_config = apps.get_app_config(app_label)
    except LookupError:
        print(f'App label "{app_label}" does not exist.')
        return

    # Perskaityti JSON failą ir deserializuoti duomenis
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        objects = serializers.deserialize('json', data)
        with transaction.atomic():
            for obj in objects:
                if obj.object.__class__ in app_config.get_models():
                    obj.save()

if __name__ == "__main__":
    app_labels = ['YourApp1', 'YourApp2']  # Pakeiskite į tikrus jūsų aplikacijų pavadinimus
    file_path = f'{app_label}_data.json'
    import_app_data_from_json(app_label, file_path)

# Paleidimas iš terminalo
# python scripts/import_db.py
