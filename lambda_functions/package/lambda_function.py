import json
import requests
    
def search_hospital_nearby(place_name):
    # search the doctors based on the location and return doctor names, rate and their location
    api_key = 'AIzaSyCLVC_U5LIlNCbSINkahciTmO4kkf63gIs'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
            # 获取第一个结果的经纬度信息
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'key': api_key,
            'location': str(latitude)+","+str(longitude),
            'radius': 5000,
            'type': "doctor",
            'keyword': 'pulmonologists'
        }
        response = requests.get(url, params=params)
        results = response.json()
        res = []
        for result in results['results']:
            res.append(result['name'])
        return res
    except:
        return "no relevant results"
    
def lambda_handler(event, context):
    # Extract the place name from the event
    place_name = event['queryStringParameters']['place_name']
    # Call the search_hospital_nearby function
    results = search_hospital_nearby(place_name)
    # Return the results
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(results)
    }    
