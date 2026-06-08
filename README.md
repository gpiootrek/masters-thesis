# Master's thesis: Using large language models in information classification systems

> Author: Piotr Gołąb

## Overview
This repository contains the source code and documentation for a master's thesis project focused on mitigating the filter bubble effect in modern media consumption. The system is a web-based news aggregator that utilizes Large Language Models (LLMs) to classify news articles by political bias and sentiment. By providing transparent categorization and algorithmic recommendations, the application aims to expose users to diverse perspectives and broaden their informational horizons.

## Scientific Scope
While the project features a fully functional web application, its primary focus is on the scientific evaluation of applied AI. Key research areas include:
* Evaluating the accuracy and reliability of various Language Models in detecting subtle political bias.
* Analyzing sentiment distribution across different news sources.
* Designing recommendation algorithms optimized for diversity rather than engagement, effectively combating algorithmic echo chambers.

## System Architecture
The project is structured as a decoupled web application, designed with scalability and modern software engineering practices in mind.

### Frontend
* **Framework:** Angular
* **Role:** Provides a responsive user interface for reading news, viewing sentiment/bias metrics, and interacting with the recommendation feed.

### Backend & AI/ML
* **Framework:** Python, FastAPI
* **Role:** Manages RESTful API endpoints, handles data scraping and aggregation, and serves as the bridge to the machine learning components.
* **AI Integration:** Implements custom NLP pipelines and integrates with external LLM APIs for real-time text classification and recommendation logic.

### Infrastructure & DevOps
* **Deployment:** Containerized using Docker to ensure consistency across environments.
* **Continuous Integration:** Automated testing and build processes pipeline to validate backend logic and frontend stability.
* **Architecture:** Designed for cloud deployment, ensuring separation of concerns between the API layer, database, and ML inference services.

## License
All rights reserved. Developed as part of a Master's Thesis program.