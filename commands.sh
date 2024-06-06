brew install pipx

python3.10 -m venv env
source env/bin/activate

pip install poetry
pip install flask==2.3.1
pip install hydra-core --upgrade
pip install Frozen-Flask
pip install Flask-Ext
pip install Flask-Markdown pytz pydantic

poetry install

make run


# times zones for configs/site.yaml are available here: https://gist.github.com/Skipants/788819