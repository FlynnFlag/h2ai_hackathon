import json
import requests
    
def search_doctor_nearby(place_name):
    # search the doctors based on the location and return doctor names, rate and their location
    import requests
    api_key = 'AIzaSyCLVC_U5LIlNCbSINkahciTmO4kkf63gIs'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={api_key}'
    detail_url = 'https://maps.googleapis.com/maps/api/place/details/'
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
            'keyword': 'pulmonologists',
            "rankby" : "prominence"
        }
        response = requests.get(url, params=params)
        results = response.json()['results'][:5]

        place_ids = []
        
        for result in results:
            place_ids.append(result['place_id'])

        res = []        
        for place_id in place_ids:
            place_id_url = f'{detail_url}json?place_id={place_id}&key={api_key}'
            details = requests.get(f'{detail_url}json?place_id={place_id}&key={api_key}').json()['result']
            item = {}
            item['name'] = details.get('name')
            item["address"] = details.get('formatted_address')
            item["phone"] = details.get('formatted_phone_number')
            item["website"] = details.get('website')
            item['rating'] = details.get("rating")
            try:
                item["top_review"] = details.get("reviews")[0]['text']
            except:
                item["top_review"] = None
            item["wheelchair_accessible_entrance"] = details.get('wheelchair_accessible_entrance')
            res.append(item)

        return res
    except:
        return "no relevant results"
    
def lambda_handler(event, context):
    # Extract the place name from the event
    place_name = event['queryStringParameters']['place_name']
    # Call the search_hospital_nearby function
    results = search_doctor_nearby(place_name)
    # Return the results
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(results)
    }    
