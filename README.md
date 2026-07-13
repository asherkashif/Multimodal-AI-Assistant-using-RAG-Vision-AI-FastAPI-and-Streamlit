# Multimodal AI Assistant

A simple multimodal AI assistant project built with FastAPI and Streamlit. The application provides a basic web interface for uploading files such as PDFs and images, sending them to a backend API, and storing them locally for further processing.

## Overview

This project combines:
- a FastAPI backend for file handling and health checks
- a Streamlit frontend for a simple user interface
- local file storage in the uploads folder

## Features

- Upload PDF, JPG, JPEG, and PNG files from the web interface
- Receive upload success feedback from the backend
- Basic API endpoints for health monitoring and file upload
- Simple navigation UI built with Streamlit

## Project Structure

- app/main.py - FastAPI application entry point
- app/api/upload.py - Upload endpoint and file-saving logic
- frontend/app.py - Streamlit frontend interface
- uploads/ - Directory where uploaded files are stored
- requirements.txt - Python dependencies

## Tech Stack

- Python
- FastAPI
- Streamlit
- Requests
- python-multipart

## Installation

1. Clone the repository
2. Create and activate a virtual environment (optional but recommended)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the backend

```bash
uvicorn app.main:app --reload
```

The backend will be available at:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health

### Start the frontend

```bash
streamlit run frontend/app.py
```

The Streamlit app will open in your browser at:
- http://localhost:8501

## Usage

1. Open the Streamlit app in your browser
2. Upload a supported file
3. Click the upload button
4. The file will be sent to the FastAPI backend and saved in the uploads folder

## Notes

This project currently focuses on file upload and basic interface flow. It can be extended later with AI-based document analysis, image understanding, report generation, and chat-style interactions.
