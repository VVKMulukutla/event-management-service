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
## Database Schema Structure

The database used for this project stores information about events, including event name, city name, date, time, latitude, and longitude. The schema structure is as follows:

### Events Collection

| Field         | Type     | Description                                 |
|---------------|----------|---------------------------------------------|
| _id           | ObjectId | Unique identifier for the event             |
| event_name    | String   | Name of the event                           |
| city_name     | String   | Name of the city where the event is located |
| date          | Date     | Date of the event                           |
| time          | Time     | Time of the event (optional)                |
| latitude      | Float    | Latitude coordinate of the event location   |
| longitude     | Float    | Longitude coordinate of the event location  |


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
### Render Deployment

This application is deployed on Render and can be accessed using the following endpoints:

- **Base URL**: [https://event-management-service-1aw6.onrender.com](https://event-management-service-1aw6.onrender.com)

#### Endpoints

1. **Retrieve Events**: 
   - **URL**: [https://event-management-service-1aw6.onrender.com/api/events/find](https://event-management-service-1aw6.onrender.com/api/events/find)
   - **Method**: GET
   - **Description**: Retrieves events based on the user's location and specified date.
   - **Request Parameters**:
     - `date`: Date in the format YYYY-MM-DD.
     - `lat`: Latitude of the user's location.
     - `lon`: Longitude of the user's location.
     - `page`: (Optional) Page number for pagination (default is 1).
   - **Example CURL Request**:
     ```bash
     curl -X GET "https://event-management-service-1aw6.onrender.com/api/events/find?date=2024-04-10&lat=40.7128&lon=-74.0060&page=1"
     ```

2. **Upload Events from CSV**: 
   - **URL**: [https://event-management-service-1aw6.onrender.com/api/events](https://event-management-service-1aw6.onrender.com/api/events)
   - **Method**: POST
   - **Description**: Uploads events from a CSV file.
   - **Request Parameters**:
     - `file`: CSV file containing event data.
   - **Example CURL Request**:
     ```bash
     curl -X POST -F "file=@events.csv" "https://event-management-service-1aw6.onrender.com/api/events"
     ```
   Replace `"events.csv"` with the path to your CSV file containing event data.

Feel free to interact with the API using the provided endpoints.

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

