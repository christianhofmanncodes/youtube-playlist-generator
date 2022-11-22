sed -i 's/==/>=/g' requirements/base.txt
pip3 install -r requirements/base.txt --upgrade
pip3 freeze > requirements/base.txt
