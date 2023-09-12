import requests

def check_shipment_status(AWB, CompanyID, AccessToken):
    # Define the base URL of the API
    base_url = 'https://vsoftapi.com-eg.net/api/ClientUsers/V6/GetShipmentDetails/'

    # Construct the full URL with the AWB parameter
    url = f'{base_url}{AWB}'

    # Define headers
    headers = {
        'CompanyID': CompanyID,
        'AccessToken': AccessToken,
        'Language': 'en',  # You can change the language as needed
        'accept': '*/*'
    }

    try:
        # Send the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            shipment_details = response.json()

            # Extract the "Reason" from the response
            reason = shipment_details.get("shipmentInfo", [{}])[0].get("Reason", "")

            return f"{reason}"  # Print the reason for debugging
        else:
            return " not"  # Request was not successful

    except requests.exceptions.RequestException as e:
        return "error"

# Example usage:
AWB = 'ECS21475013'
CompanyID = '191307'
AccessToken = '5ED339A9-5C4C-4348-9A09-F2AAA6CF049D'
result = check_shipment_status(AWB, CompanyID, AccessToken)

if  result == "Collected" :
    print('ok')
