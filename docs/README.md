# Documentation

## Overview of the system

This system consists of multiple components:
* **frontend** - web page where users can browse and buy books
* **orchestrator** - service that handles connections between frontend and other specific backend services
* **fraud detection service** - service that checks if placed order is fraudulent or not
* **transaction verification service** - service that verifies if placed order is valid
* **suggestions service** - service that provides suggestions for other products to the user, based on bought items

The frontend communicates with the orchestrator via REST API requests and the orchestrator communicates with the other backend services via gRPC requests.

## Diagrams

The communication between components is shown on the [architecture diagram](architecture.png). The general flow of actions, starting from the user clicking "Submit" on the frontend web page and ending with the web page displaying the status of the user's order ("approved" or "rejected"), can be seen on the [system diagram](system.png).
