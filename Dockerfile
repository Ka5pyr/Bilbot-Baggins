# Use a base image with Python 3.10-slim
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file first (leveraging Docker cache)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code
COPY . .

# Set the entry point to run the bot
CMD ["python3", "main.py", "--docker"]