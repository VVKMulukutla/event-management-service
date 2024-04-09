from flask import Flask, request, jsonify
import pymongo
import csv
from io import StringIO
from datetime import datetime, timedelta
import math
import aiohttp
import asyncio
from dotenv import load_dotenv
import os 

app = Flask(__name__)
load_dotenv()
# client = pymongo.MongoClient("mongodb://localhost:27017/eventdb")
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client['eventdb']['events']


@app.route("/api/events", methods=['POST'])
def add_events():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        csv_data = file.stream.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(csv_data))
        for row in csv_reader:
            db.insert_one(row)
            print('Done')
        return jsonify({'message': 'CSV file uploaded successfully'}), 200
    return jsonify({'error': 'Something went wrong'}), 500


async def fetch_weather(session, city, date):
    url = 'https://gg-backend-assignment.azurewebsites.net/api/Weather'
    params = {'code': os.getenv('WEATHER_API_KEY'), 'city': city, 'date': date}
    async with session.get(url, params=params) as response:
        return await response.json()


async def fetch_distance(session, lat1, lon1, lat2, lon2):
    url = 'https://gg-backend-assignment.azurewebsites.net/api/Distance'
    params = {'code': os.getenv('DISTANCE_API_KEY'),
              'latitude1': lat1, 'longitude1': lon1, 'latitude2': lat2, 'longitude2': lon2}
    async with session.get(url, params=params) as response:
        return await response.json()


@app.route("/api/events/find", methods=['GET'])
async def find():
    try:
        search_date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
        end_date = search_date + timedelta(days=14)

        query = {
            'date':{
                '$gte':search_date.strftime('%Y-%m-%d'),
                '$lte':end_date.strftime('%Y-%m-%d')
            }
        }

        total_events = db.count_documents(query)

        page = int(request.args.get('page', 1))
        page_size = 10
        skip = (page - 1) * page_size

        events = db.find(query).sort('date', pymongo.ASCENDING).skip(skip).limit(page_size)

        response = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for event in events:
                tasks.append(process_event(session, event))
            response = await asyncio.gather(*tasks)

        total_pages = math.ceil(total_events / page_size)

        return jsonify({
            "events": response,
            "page": page,
            "pageSize": page_size,
            "totalEvents": total_events,
            "totalPages": total_pages
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


async def process_event(session, event):
    
    weather = await fetch_weather(session, event['city_name'], event['date'])

    distance_km = await fetch_distance(session, request.args.get('lat'), request.args.get('lon'), event['latitude'], event['longitude'])

    new_record = {
        "event_name": event["event_name"],
        "city_name": event["city_name"],
        "date": event["date"],
        "weather": weather['weather'],
        "distance_km": distance_km['distance']
    }

    return new_record


if __name__ == '__main__':
    app.run(debug=True, port=7777)
