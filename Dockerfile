# Use an official Python runtime as the base image
FROM python

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set the environment variables (if any)
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=hossein
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=hossein

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Command to run the Python script
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
