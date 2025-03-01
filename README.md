# Vinicunca_AI_Project1
RAG and GEN AI Haircare Project

## Install NextJS
https://nextjs.org/docs/app/getting-started/installation
Packages are ready just type:

npm install 

## Starting NextJS - FRONTEND
Please read the documentation here:
Tutorial: https://www.youtube.com/watch?v=_EgI9WH8q1A&t=11s

```
npm run dev
```
* Automatically installs necessary dependencies
* Runs the dev environment and automatically reloads whenever changes are made

## Starting FastAPI - BACKEND
Please read the fastapi documentation here: https://fastapi.tiangolo.com/#create-it

### Step 1
Install dependencies from the requirements file
```
python -m pip install -r requirements.txt
```

#### FOR MAC
``` 
python3 -m pip install -r requirements.txt
```

### Step 2
Setup you Gemini Key and the .env in backend folder
* Create .env file in backend
* Paste Gemini Key
* Make sure the variable is declared as: GEMINI_API_KEY

### Step 3 
```
python -m uvicorn main:app --reload
```
#### FOR MAC
``` 
python3 -m uvicorn main:app --reload
```
uvicorn will call the app and reload it automatically whenever we make changes. 
main:app = filename:appname
--reload positional argument

