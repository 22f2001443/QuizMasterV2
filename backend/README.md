# It's all about the 'backend'

## How to run backend

1. Create `.env` file using `.env.example`
2. Activate virtual environment
3. Install dependencies: `pip install -r req.txt`
4. Run server: `python app.py` or `flask run --host=0.0.0.0 --port=8000`

## File Structure:

### Root
| File/Folder Name    | Type                   | Purpose |
|:--------------------|:---------------------- |:----------|
| venv                |  Virtual Enviourment   |Install all dependecies without conflicting with other py packages installed already   |
|app.py               |  Python File           |Main py file where the Flask app in initialized | 
|req.txt              |  Txt File              |File containing all the pachkages' name required for the project |
|config.py            |  Python File           |Defining configuration requied|
|data                 |  Folder                |Stores DB files, JSON, etc|
|controller           |  Folder                |Containes all py files handling backend
|.env                 |  Enviourmental Storage |Stores Environment-specific config

### /data
| File/Folder Name    | Type                   | Purpose              |
|:--------------------|:---------------------- |:---------------------|
| quiz_db_v2.sqlite   |  DB File               |SQLite Database file  |

### /controller
| File/Folder Name    | Type                   | Purpose               |
|:--------------------|:---------------------- |:----------------------|
| db.py               |  Python File           |Initializing SQLAlchamy|
|model.py             |  Python File           |Defining the DB Structure|
|routes               |  Folder                |Containg files that handel endpoints| 

### .\/controller/routes
| File/Folder Name    | Type                   | Purpose               |
|:--------------------|:---------------------- |:----------------------|
|routesRegister.py    |  Python File           |Handels the endpoints by calling reqired api(s) |


Will update it later.
# okay
240125
240516