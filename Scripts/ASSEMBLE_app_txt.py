import os

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of files to merge
file_names = ['IMPORT.py',
              'constants.py', 
              'calculations.py', 
              'viz_engine_app.py',
              'LAUNCH.py']

# Construct absolute file paths
file_paths = [os.path.join(script_dir, file_name) for file_name in file_names]

# Destination file (merged output)
output_file = 'merged_app.py'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    for file_path in file_paths:
        with open(file_path, 'r') as infile:
            # Write a comment indicating the start of a new file's content
            outfile.write(f"# Start of {file_path}\n")
            # Read the content of each file and write it to the output file
            outfile.write(infile.read())
            # Add a newline character to separate the content of each file
            outfile.write('\n')
            # Write a comment indicating the end of a file's content
            outfile.write(f"# End of {file_path}\n\n")

