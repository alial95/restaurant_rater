def change_none_values_postcode(data):
    for i in data:
        if i['Postcode'] == None:
            i['Postcode'] = '0'
        else:
            continue
    return data