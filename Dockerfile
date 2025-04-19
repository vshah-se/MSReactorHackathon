# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirement.txt .

# Install any needed packages specified in requirement.txt
# Using --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code into the container at /app
# Copy app.py and rag.py (if it's used by the app)
COPY app.py .
COPY rag.py .
# If the PDFs are needed by the application at build time, copy them too
# COPY RCW_59.18.pdf .
# COPY rental_agreement.pdf .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables if needed
# ENV NAME World

# Run app.py when the container launches
# For production, use a WSGI server like Gunicorn:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
# CMD ["python", "app.py"]
