"""
to complete the application, you need to have a python script at the top-level that defines the Flask application instance. 
Let's call the script <i> microblog.py </i>, and define it as a single line that imports the application instance
"""

from app import app

# Remember the two app entities? Here you can see both together in the same sentence. The Flask application instanc eis called app and is a member of the app package. the "from app import app" statement
# imports the app variable that is a member of the "app" package. If you find this confusing, you can rename either the package or the variable to something else.
# Before you run this, set FLASK_APP=microblog.py in win console to set the enviromental variable