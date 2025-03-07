# Real-time Clickstream Analytics and User Behavior Prediction Pipeline for E-commerce

## Overview
A real-time analytics platform that processes and analyzes user clickstream data from e-commerce platforms to generate personalized product recommendations. The system uses a modern data engineering stack with streaming capabilities, machine learning, and containerized deployment options.

This project implements a real-time Clickstream Analytics and User Behavior Prediction pipeline for e-commerce using Kafka, Spark, and Elasticsearch and deployed using Docker and Kubernetes. The project is deployed using docker-compose and kubernetes deployment files. Here in this project we have used flask api to get the user input and to predict the user behavior and return the recommendation to the user. The input data here for this project is simulated using python scripts and stored in kafka topic , this data is processed using spark streaming and stored in elasticsearch. The recommendation is stored in postgresql database. The dashboard is created using Tableau but since the data is simulated so the recommendation is not accurate and so the tableau dashboard is not created. it is just for the demonstration of the project to showcase my expertise in the field of data engineering and data science . 

This same project file can be used as a pipeline in the real world ecomerce data to predict the user behavior and return the recommendation to the user with the help of the real data from the enterprise.

## Motivation & Objective
E-commerce businesses deal with vast amounts of user interaction data. Understanding customer behavior in real time can enhance user experience, improve product recommendations, and optimize sales. 

### This project aims to:
- Capture real-time user activity through event streaming.
- Process and store clickstream data for analytical insights.
- Develop machine learning models to predict user behavior and preferences.
- Deliver personalized product recommendations through a REST API.
- Visualize insights using Tableau dashboards.

## Architecture
![Alt Text](https://github.com/Albinmanuvel/Clickstream-Analytics-for-E-Commerce/blob/main/images/Architecture.png?raw=true)



### Key Components
- **Data Ingestion**: Kafka-based streaming pipeline for real-time clickstream data
- **Processing**: Apache Spark for stream processing and real-time analytics
- **Storage**: 
  - PostgreSQL for structured data and recommendations
  - Elasticsearch for real-time analytics and search
- **API Layer**: Flask-based REST API for serving recommendations
- **Deployment**: Docker and Kubernetes support for scalable deployment

## Features
- Real-time clickstream data processing
- Session-based user analytics
- Product recommendations using collaborative filtering
- RESTful API for accessing analytics and recommendations
- Scalable architecture using containers
- Support for both Docker Compose and Kubernetes deployment

## Tech Stack
- **Apache Kafka**: Stream processing platform
- **Apache Spark**: Distributed computing and ML
- **PostgreSQL**: Relational database
- **Elasticsearch**: Real-time search and analytics
- **Flask**: Web API framework
- **Docker & Kubernetes**: Containerization and orchestration

## Folder Structure for Clickstream Analytics Project

```bash

Clickstream-Analytics-for-E-Commerce/
│── scripts/                    # Contains Python scripts for producer, consumer, recommendation
│   ├── kafka_producer.py        # Kafka producer script (simulated clickstream data)
│   ├── spark_consumer.py        # Spark Streaming consumer to process clickstream data
│   ├── real_time_recommendation.py  # Real-time recommendation engine
│── data/                        # Folder for storing any sample datasets (optional)
│   ├── sample_data.json
│── notebooks/                   # Jupyter notebooks for data analysis & visualization
│   ├── exploratory_analysis.ipynb
│── sql/                         # SQL scripts for database setup & queries
│   ├── create_database.sql       # SQL script to create clickstream_db
│   ├── insert_sample_data.sql    # Sample data insertion script
│── docker/                       # Docker-related files for containerization
│   ├── Dockerfile                # Docker instructions for setting up the project
│   ├── docker-compose.yml        # Docker Compose file for managing multi-container setup
│── kubernetes/                   # Kubernetes manifests for orchestration
│   ├── kafka-deployment.yaml     # Kubernetes config for Kafka
│   ├── spark-deployment.yaml     # Kubernetes config for Spark
│   ├── postgres-deployment.yaml  # Kubernetes config for PostgreSQL
│── requirements.txt              # List of Python dependencies
│── README.md                     # Project documentation
│── .gitignore                     # Files to ignore in GitHub
│── LICENSE                        # License file for open-source usage

```





## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Kubernetes cluster (optional)
- Java 8+ (for Apache Spark)

### Local Development Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/clickstream-analytics.git
cd clickstream-analytics
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export POSTGRES_USER=your_username
export POSTGRES_PASSWORD=your_password
export POSTGRES_DB=clickstream_db
```

### Docker Deployment

1. Build and run using Docker Compose:
```bash
cd docker
docker-compose up --build
```

### Kubernetes Deployment

1. Apply Kubernetes configurations:
```bash
kubectl apply -f kubernetes/
```

## Usage

### Starting the Services

1. Start the Kafka producer:
```bash
python scripts/kafka_producer.py
```

2. Launch the Spark consumer:
```bash
python scripts/spark_consumer.py
```

3. Start the Flask API:
```bash
python scripts/app.py
```

### API Endpoints

- `GET /sessions`: Retrieve session-based analytics
- `GET /real-time-events`: Get real-time clickstream events
- *(Add other API endpoints)*

## Data Flow

1. Clickstream events are generated/simulated using `simulate_clickstream.py`
2. Events are published to Kafka topics
3. Spark Streaming processes the events in real-time
4. Processed data is stored in PostgreSQL and Elasticsearch
5. Real-time recommendations are generated using collaborative filtering
6. Results are accessible via Flask API endpoints

## Monitoring and Maintenance

- Kafka topics can be monitored using Kafka Manager
- Elasticsearch indices can be monitored via Kibana
- PostgreSQL database can be accessed using standard SQL tools

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Apache Spark and Kafka communities
- Contributors and maintainers of all used libraries

## Contact
[albinmanuvel31@gmail.com]

Linkedin - [www.linkedin.com/in/albin-manuvel-6607a9221]

Project Link: [https://github.com/Albinmanuvel/Clickstream-Analytics-for-E-Commerce]
