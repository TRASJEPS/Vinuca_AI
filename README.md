# Vinicunca_AI_Project1
RAG and GEN AI Haircare Project

## Starting NextJS
Please read the documentation here:

Tutorial: https://www.youtube.com/watch?v=_EgI9WH8q1A&t=11s

```
npm run dev
```
* Automatically installs necessary dependencies
* Runs the dev environment and automatically reloads whenever changes are made

## Starting FastAPI
Please read the fastapi documentation here: https://fastapi.tiangolo.com/#create-it

### Step 1
Install dependencies from the requirements file
```
python -m pip install -r requirements.txt
```

### Step 2
```
python -m uvicorn main:app --reload
```
uvicorn will call the app and reload it automatically whenever we make changes. 
main:app = filename:appname
--reload positional argument