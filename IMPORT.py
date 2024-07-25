# sys and subprocess to install libraries
import subprocess
import sys
# Function to check if a library is installed and install it if not
def install(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# Libraries list to check and install if necessary
libraries = ['pandas', 
             'numpy', 
             'openpyxl', 
             'dash', 
             'plotly']
for lib in libraries:
    install(lib)

#data
import gunicorn as gunicorn
import pandas as pd
import numpy as np
from json import dumps
import openpyxl as openpyxl
#visuals
import dash as dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

