from flask import Blueprint

admin = Blueprint('admin', __name__)

# import views here
from . import views
