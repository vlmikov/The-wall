## The Wall

The Wall program is created 

1. ["GET","POST"] /create_wall_configuration/

    GET  => Return all valid configurations

    POST => Validate and save configurations

2. ["GET", "PUT", "DELETE"] /create_wall_configuration/

    GET     => accepts pk, query db and return the record 

3. ["GET"] /profiles/<int:profile>/days/<int:day>/ 

     Endpoint that accepts profile number and day and returns
    day, ice_amount for the input profile till the provided day.

4. ["GET"] /profiles/<int:profile>/overview/<int:day>/

     Endpoint that accepts profile number and day and returns
    day, cost for the input profile till the provided day.

5. ["GET"] /profiles/overview/<int:day>/

    Endpoint that accepts day and return overview of the wall
    till the input day.

6. ["GET"] /profiles/overview/

    Endpoint that return wall overview.
    cost needed to complete all sections.


### Installation
To use this Python script, you must first clone or download the repository and install the required dependencies,
which can be found in the requirements.txt file. You can install them using pip:

1. Create script directory
```
mkdir the_wall
cd the_wall
```
2. Create virtual environment and activate it

```
python3 -m venv env
# For macOS
source env/bin/activate
# For Windows
.\env\Scripts\activate

```
3. Clone or download the repository

```
git clone https://github.com/vlmikov/The-wall
```
4. Install requirenments.txt
```
pip3 install -r requirements.txt
```
5. Set your credentials for postgress in settings.py

5. Run test
```
python manage.py test
```
6. Run the server
```
python manage.py runserver
```




