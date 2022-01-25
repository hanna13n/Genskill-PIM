# Genskill-PIM  

Genskill Project - Personal Info Manager  
A web app with React frontend and Flask backend
https://eazynote.herokuapp.com/
  
## Instructions
1. Clone this repo. 
2. Create a python virtual env and activate it  
``` 
python3 -m venv newenv   
. /path-to-newenv/bin/activate
```  
3. Install dependencies
```
pip install -r requirements.txt
npm install
```
4. Create a postgres database and set up the environment variable
```
export DATABASE_URL=databaseURL
```
6. Initialise database  
```
export FLASK_APP=notes
flask initdb
```
7. Run the application
```
flask run
npm start
```
