# Development stage
FROM python:alpine AS development

WORKDIR /python-docker

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run tests (assuming your tests are still Python scripts)
# CMD ["python3", "test_app.py", "-v"]

# Production stage
FROM python:alpine AS production

WORKDIR /python-docker

# Copy only the necessary files for production
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Create a new user with UID 10016
RUN addgroup -g 10016 choreo && \
    adduser --disabled-password --no-create-home --uid 10016 --ingroup choreo choreouser

# Switch to the new user
USER 10016

# Expose the application port
EXPOSE 8000

# Start the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
