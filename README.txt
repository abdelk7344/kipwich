FLASK Protocol: 

STARTING:
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
flask run

FINISHING: 
pip freeze > requirements.txt

GITHUB Protocol: 

INTIALIZING GITHUB:
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/abdelk7344/kipwich.git
git push -u origin main


MAKING CHANGES TO REPO: 
git pull
git add .
git commit -m "commit name"
git push
