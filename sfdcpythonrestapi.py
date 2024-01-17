import requests # pip install requests
# from consumer_details import CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD
import pandas as pd # pip install pandas

CONSUMER_KEY = '3MVG9NYvTkhtdEI6.d.cIoRezGbs91JH.1Cu.LAdRyFmtWXVKk9D4OO9wYH1DM3.YO8rv7FPk5NYvtS5cEnXd'
CONSUMER_SECRET = 'E95455DBCE13800BDB5FBA1C03E2FF76930EA1AE07545881B56082C78FBA1580'
USERNAME = 'duntee.silver@teleflex.com.sandbox'
PASSWORD = 'Antoine@12@'
access_token = '00D7c000006tfGR!ARwAQP31kB61kWxL6A.G60gt.pAlb0cgy93rvBXpqEQ7xN05jfCm8Mt9BwErBKI2YIcJJLVgzJv7gs6rmhfS45hz0CVfPI4m'
DOMAIN = 'https://teleflex--sandbox.sandbox.my.salesforce.com'


# Generate Access Token
def generate_token():    
    payload = {
        'grant_type': 'password',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'username': USERNAME,
        'password': PASSWORD
    }
    oauth_endpoint = '/services/oauth2/token'
    response = requests.post(DOMAIN + oauth_endpoint, data=payload)
    return response.json()


access_token = generate_token()['access_token']
headers = {
    'Authorization': 'Bearer ' + access_token
}


# Example 1. Run a SOQL query
def query(soql_query):
    try:
        # soql_query = 'SELECT name FROM opportunity'
        endpoint = '/services/data/v58.0/query/'
        records = []
        response = requests.get(DOMAIN + endpoint, headers=headers, params={'q': soql_query})
        total_size = response.json()['totalSize']
        records.extend(response.json()['records'])


        while not response.json()['done']:
            response = requests.get(DOMAIN + endpoint + response.json()['nextRecordsUrl'], headers=headers)
            records.extend(response.json()['records'])
        return {'record_size': total_size, 'records': records}
    except Exception as e:
        print(e)
        return


records = query('SELECT id, name, type FROM opportunity LIMIT 2000')
#print(records)
#records['record_size']
df = pd.DataFrame(records['records'])
df.drop(['attributes'], axis=1, inplace=True)
df.to_csv('oppData.csv', index=False)
#print(df)


# Example 2. Retrieve an object's metadata
def retrieve_object_metadata(object_api_name):
    response = requests.get(DOMAIN + f'/services/data/v58.0/sobjects/{object_api_name}/describe', headers=headers)
    return response.json()


object_id = 'account'
object_metadata = retrieve_object_metadata(object_id)
#print(object_metadata)
df_metadata = pd.DataFrame(object_metadata['fields'])
df_metadata.to_csv('account metadata information.csv', index=False)
