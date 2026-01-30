# Webhook Receiver Repo

A Flask application that receives GitHub webhooks, stores them in MongoDB, and displays them in a real-time UI.

## Prerequisites

- Python 3.8+
- MongoDB (MongoDB Atlas account recommended)

## Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/GovindHede/webhook-repo.git
    cd webhook-repo
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Open `.env` and fill in your **MONGO_URI**. 
      - Example Atlas URI: `mongodb+srv://user:password@cluster.mongodb.net/myDatabase?retryWrites=true&w=majority`
      - Ensure you whitelist your IP in MongoDB Atlas Network Access.

5.  **Run the Application**
    ```bash
    python run.py
    ```
    The app will start at `http://localhost:5000`.

## Webhook Configuration

To receive webhooks from GitHub on your local machine, you need to expose your localhost to the internet.

1.  **Using ngrok**
    - Install `ngrok`.
    - Run: `ngrok http 5000`
    - Copy the HTTPS URL (e.g., `https://1234.ngrok.io`).

2.  **GitHub Setup**
    - Go to your trigger repository settings (e.g., `action-repo`).
    - Add a Webhook:
      - **Payload URL**: `https://<your-ngrok-url>/webhook`
      - **Content Type**: `application/json`
      - **Events**: Push and Pull Requests.

## Features

- Handles **PUSH**, **PULL_REQUEST**, and **MERGE** events.
- Stores events in MongoDB to persist data.
- UI polls every 15 seconds to show new events.
- Prevents duplicates using GitHub Delivery ID.