# Event Management System

## Overview
The Event Management System is a RESTful service that manages and queries event data based on a user's geographical location and a specified date. This service allows users to add events into the system and retrieve events occurring within the next 14 days from a specified date.

## Tech Stack
- **Python**: Used for backend development.
- **Flask**: Chosen as the web framework for its simplicity and flexibility in building RESTful APIs.
- **MongoDB**: Selected as the database for its scalability and flexibility in handling unstructured data.
- **pymongo**: Python driver for MongoDB, used for interacting with the MongoDB database.
- **aiohttp**: Asynchronous HTTP client/server framework for making parallel calls to external APIs.

## Database
MongoDB was chosen as the database due to its flexibility in handling unstructured data, which is common in event management systems. Additionally, MongoDB's scalability makes it suitable for handling large volumes of event data.

## Design Decisions
- **Flask**: Chosen for its lightweight nature and simplicity in building RESTful APIs.
- **Asynchronous Calls**: Utilized aiohttp for making parallel calls to external APIs to minimize response times.
- **Environment Variables**: Stored sensitive information such as API keys and database URI in environment variables for security purposes.
- **Folder Structure**: Organized the code into separate modules (routes, models, utils) for better maintainability and readability.

## Setup and Run
1. Clone the repository: `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add the following environment variables:
   ```
   WEATHER_API_KEY=your_weather_api_code
   DISTANCE_API_KEY=your_distance_api_code
   MONGODB_URI=your_mongodb_uri
   ```
4. Run the Flask app: 
    1. `cd app`
    2. `python main.py`

## API Endpoints

### Data Creation API
- **Endpoint**: `/api/events`
- **Method**: POST
- **Request Body**: CSV file containing event details (event name, city name, date, time, latitude, longitude)
- **Response**: JSON response indicating success or failure

### Event Finder API
- **Endpoint**: `/api/events/find`
- **Method**: GET
- **Query Parameters**:
  - `date`: Specified date in the format `YYYY-MM-DD`
  - `lat`: User's latitude
  - `lon`: User's longitude
  - `page`: Page number for pagination (optional)
- **Response**:
  - `events`: List of events matching the criteria, sorted by date
  - `page`: Current page number
  - `pageSize`: Number of events per page
  - `totalEvents`: Total number of events
  - `totalPages`: Total number of pages

### Error Codes
- `400`: Bad request (e.g., missing query parameters)
- `500`: Internal server error

