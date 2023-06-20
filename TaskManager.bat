@echo off

set db_path="%cd%\app_data.db"
set settings_path="%cd%\settings.json"

if exist %db_path% (
    if exist %settings_path% (
    python start.py
    )
) else (
    pip install -r requirements.txt
    python install.py
    python start.py
)



