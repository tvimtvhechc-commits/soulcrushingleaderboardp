import os
import requests

def get_data(r):
    # Updated to your new Spreadsheet ID
    spreadsheet_id = "1Mc9dVP31CmnEk5VRMalF7CicWBWbLncsHa6HLYYEiW0"
    api_key = os.getenv('GOOGLE_SHEETS_API_KEY')
    
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{r}?key={api_key}"
    
    response = requests.get(url).json()
    values = response.get("values", [])
    
    if len(values) < 2:
        return []

    headers = values[0]
    data = []

    for row in values[1:]:
        item = {}
        for i, header in enumerate(headers):
            val = row[i] if i < len(row) else ""
            if header.lower() == "completions":
                # Keeps the logic that turns "1,2,3" into [1, 2, 3]
                item[header] = [int(x) for x in val.split(",") if x] if val else []
            else:
                item[header] = val
        data.append(item)

    return data
