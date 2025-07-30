# ClassifyAPI 🚀

![Project Status](https://img.shields.io/badge/status-pre--alpha-orange)
![Language](https://img.shields.io/badge/python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/framework-Flask%2FFastAPI-lightgrey)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> A lightweight, cloud-deployed web API for serving machine learning classification models.

## The Mission

This project serves as the practical application for the "Cloud Computing for Data Science" diploma curriculum. Its goal is to take a trained machine learning model and make it accessible to the world through a simple, robust API.

This project picks up where the [`AutoCleanSE`](https://github.com/chishxd/autocleanse) project leaves off. We will use the clean data produced by `AutoCleanSE` to train a model, and then we will build the infrastructure to deploy and serve that model in the cloud.

## Core Features (The Roadmap)

-   [ ] **API Framework:** A simple web server using Flask or FastAPI to define prediction endpoints.
-   [x] **Cloud Storage Integration:** Ability to connect to S3-compatible object storage (like MinIO or AWS S3) to retrieve assets.
-   [ ] **Model Serving:** Load a serialized ML model (e.g., a `.pkl` file) and use it to make live predictions.
-   [ ] **Cloud Deployment:** The entire application will be packaged and deployed to a cloud provider (e.g., as an AWS Lambda function).
-   [ ] **Containerization:** The application will be containerized using Docker/Podman for portability.

## Current Status

We have successfully established programmatic access to a local, S3-compatible MinIO server using `boto3`. This proves our ability to interact with cloud storage, which is the foundational first step.

### Local Setup for Cloud Simulation

This project uses **MinIO** to simulate AWS S3 locally. This allows for rapid, offline development.

<details>
<summary><b>Running the Local MinIO Server</b></summary>

```bash
# First, ensure the MinIO container exists. If not, create it.
# This command runs the server in the background.
podman run -d -p 9000:9000 -p 9001:9001 --name minio-server -v ~/minio-data:/data -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=password" minio/minio server /data --console-address ":9001"

# To start the server for a new work session:
podman start minio-server

# To stop the server:
podman stop minio-server
```
</details>

## Usage

The current test script demonstrates how to connect to the MinIO server.

```python
# cloud_test.py
import boto3

# --- Configuration ---
access_key = "admin"
secret_key = "password"
endpoint_url = "http://127.0.0.1:9000"
# ---

s3_client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

response = s3_client.list_buckets()
print("Successfully connected. Found buckets:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")
```

## License

Distributed under the MIT License.