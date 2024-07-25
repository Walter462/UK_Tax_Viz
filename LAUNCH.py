#import viz_engine_app
from viz_engine_app import app
if __name__ == '__main__':
    app.run_server(debug=True)

import subprocess
    
# Use pip freeze to get the list of installed packages
requirements = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

# Write the output to a requirements.txt file
with open('requirements.txt', 'w') as f:
    f.write(requirements.stdout)