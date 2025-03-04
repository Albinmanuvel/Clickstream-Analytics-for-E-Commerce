# Use official Python image as the base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables (modify as needed)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the necessary ports
EXPOSE 5000  
# Flask API
EXPOSE 9092  
# Kafka
EXPOSE 5432  
# PostgreSQL
EXPOSE 9200  
# Elasticsearch

# Default command (modify based on your main service)
CMD ["python", "scripts/spark_consumer.py"]
