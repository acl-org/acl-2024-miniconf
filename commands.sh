brew install pipx

python3.10 -m venv env
source env/bin/activate

pip install poetry
pip install flask==2.3.1
pip install hydra-core --upgrade
pip Frozen-Flask Flask-Ext Flask-Markdown pytz pydantic markdown-to-json

poetry install

make run


# times zones for configs/site.yaml are available here: https://gist.github.com/Skipants/788819