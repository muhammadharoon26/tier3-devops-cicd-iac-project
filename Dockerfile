FROM python:3.9-slim

# Working directory && Install the requirements
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
COPY . .
EXPOSE 5000

# Run the flask app
CMD [ "python", "-m", "app.main" ]