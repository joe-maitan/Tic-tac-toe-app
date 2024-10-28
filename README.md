# Tic-tac-toe-app
CS457 Term Project

# Module load
Because this is being developed on the CS machines from CSU we have a module load command to load python 3.10 or greater
```
module load python/bundle-3.10
```

But if you have a version of python downloaded that is greater than python 3.6, do not worry about using specifically 3.9.

# How to run the app
1. Clone the repository
```
git clone https://github.com/joe-maitan/Tic-tac-toe-app.git
```

2. Navigate to the project directory
```
cd Tic-tac-toe-app
```

3. Navigate to the backend directory
```
cd backend
```

4. Create a virtual enviornment
* On MacOS and Linux
```
python3 -m venv venv
```

* On Windows
```
python -m venv venv
```

NOTE: The venv is already included in the project, just needs to be activated.

5. Activate the virtual enviornment:
* On MacOS and Linux:
```
source venv/bin/activate
```

* On Windows:
```
venv/Scripts/activate
```

6. Install dependencies:
* On MacOS and Linux:
```
pip3 install -r requirements.txt
```

* On Windows:
```
pip install -r requirements.txt
```

7. Navigate to the frontend directory:
```
cd ../frontend
```

8. Install the dependencies for the frontend:
NOTE: Must have Node.js and NVM installed on machine
```
npm install
```

9. Run the dev enviornments of each (until we figure out how to deploy)
* For the backend:
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\backend python3 server.py
```
* For the frontend:
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\frontend npm run dev
```


