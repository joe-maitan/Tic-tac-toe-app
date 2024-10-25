# Tic-tac-toe-app
CS457 Term Project

# Module load
Because this is being developed on the CS machines from CSU we have a module load command to load python 3.9
```
module load python/bundle-3.10
```

But if you have a version of python downloaded that is greater than python 3.6, do not worry about using specifically 3.9.

To create a virtual environment (venv) in Python 3 on Linux, you can use the following command:
```
python3 -m venv venv
```

After creating the virtual enviornment active it using:
```
source venv/bin/activate
```

To install the necessary libraries from requirements.txt run:
```
pip3 install -r requirements.txt
```

Windows
```
python3 -m pip  install -r requirements.txt
```


# How to run the program
## The backend
The program has two pieces of right now, the backend and the frontend.

To run the backend you must be in the backend directory (/Tic-tac-toe-app/backend), from there type:
```
python3 server.py
```

This will initiate the backend server.

## The frontend
To run the frontend you need to be in the frontend directory (/Tic-tac-toe-app/frontend), from there type:
```
npm run dev
```

or

```
npm start
```

