# Interview task

### Steps to launch app in local environment.
1. Create virtual environment using python3.12 (v3.12.4 was used for development).
```
python3.12 -m venv venv
```
3. Activate environment:
```
source venv/bin/activate
```
3. Install dependencies from file:
```
pip install -r requirements.txt
```
4. Create file with configuration settings using .env-template file.
5. Launch app (port - 8000):
```
fastapi dev app/main.py
```
