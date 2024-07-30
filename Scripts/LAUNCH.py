#import viz_engine_app
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)

from IMPORT import dash
from viz_engine_app import app

if __name__ == '__main__':
    app.run_server(debug=True)
