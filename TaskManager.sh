db=./app_data.db
settings=./settings.json
if !( test -f "$db" ) || !( test -f "$settings" ); then
	pip install -r requirements.txt
	python3 install.py
fi
python3 start.py
