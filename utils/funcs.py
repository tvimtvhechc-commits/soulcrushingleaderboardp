import os
import requests

def get_data(r):
    # Your official Spreadsheet ID
    spreadsheet_id = "1Mc9dVP31CmnEk5VRMalF7CicWBWbLncsHa6HLYYEiW0"
    
    # Since your tab is named 'comps', we use it here.
    # We keep 'r' just in case other parts of your app send a specific range.
    # But if r is just 'Sheet1', this logic ensures it looks at 'comps' instead.
    tab_name = "comps"
    range_to_fetch = r.replace("Sheet1", tab_name) if "Sheet1" in r else f"{tab_name}!A:C"
    
    api_key = os.getenv('GOOGLE_SHEETS_API_KEY')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_to_fetch}?key={api_key}"
    
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
            # IMPORTANT: This matches the 'completions' header in C1
            if header.lower() == "completions":
                item[header] = [int(x) for x in val.split(",") if x] if val else []
            else:
                item[header] = val
        data.append(item)

    return data
