FROM python:3.9  # Adjust version if needed

WORKDIR /app

# Install Google API Client and any other dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt 

# Copy your Python Script and credentials
COPY backup_script.py ./
COPY credentials.json ./ 
COPY token.json ./  # Copy token.json if it exists 

# Mount the 'backupfiles' directory
VOLUME /app/backupfiles  

# Set the default command to run your script
CMD ["python", "backup_script.py"] 
