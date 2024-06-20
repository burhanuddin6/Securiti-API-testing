### Please create a virtual environment and install dependencies:
```
python3 -m venv env # create a folder named env
```
```
source env/bin/activate # this activates virtual environment
```
Install dependencies after activating virtual environment
```
python3 -m pip install -r requirements.txt
```
For deactivating virtual environment:
```
deactivate
```
Make sure to run all the files in this repo with virtual environemnt activated. After installing any external library, make sure to add it in requirements.txt:
```
python -m pip freeze > requirements.txt
```
### Please create data.json file before running sraper.py:
```
{
    "email": "your email",
    "password": "your password"
}
```
