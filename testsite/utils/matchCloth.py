from utils import colorDetect


def selectMatchCloth(user, temperature, hsv, matchType, colorTbl):
    score = 0

    for item in user.val()['items'].values():
        if item and item['type'] == matchType:
            tcolor = item['color']
            rgb = colorTbl[tcolor]
            hsv2 = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
            score = colorDetect.CalColorGrade(hsv, hsv2)
            if score > maxScore:
                maxScore = score
                matchCloth = item


def calWeatherScore(user, temperature, matchType):
    possible_answer = {}

    for item in user.val()['items'].values():
        if item == None or item['type'] != matchType:
            continue
        possible_answer[item] = 0
        if matchType == 'tops':
            if temperature < -10.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[item] += 10.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[item] += 8.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[item] += 7.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 2.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[item] += 10.0
                    elif item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[item] += 9.0
            elif -10.0 <= temperature < 0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Regular Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[item] += 10.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[item] += 8.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 2.0
                if 'sleeve_length' in item:
                    if (item['sleeve_length'] == 'Extra Long Sleeves' or
                            item['sleeve_length'] == 'Long Sleeves'):
                        possible_answer[item] += 10.0
                else:
                    possible_answer[item] += 0.0
            elif 0.0 <= temperature < 10.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'Regular Length' or
                            item['coat_length'] == 'Midi Length'):
                        possible_answer[item] += 10.0
                    elif (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[item] += 9.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 8.0
                elif 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[item] += 10.0
                    elif item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[item] += 8.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[item] += 6.0
            elif 10.0 <= temperature < 20.0:
                if 'coat_length' in item:
                    if item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 10.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[item] += 7.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[item] += 6.0
                    elif (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length'):
                        possible_answer[item] += 5.0
                    elif item['coat_length'] == 'Long Length':
                        possible_answer[item] += 4.0
                    elif item['coat_length'] == 'Ankle&Floor Length':
                        possible_answer[item] += 3.0
                if 'skirt_length' in item:
                    if (item['skirt_length'] == 'Short Length'
                        or item['skirt_length'] == 'Ankle Length'):
                        possible_answer[item] += 7.0
                    elif (item['skirt_length'] == 'Knee Length'
                        or item['skirt_length'] == 'Midi Length'):
                        possible_answer[item] += 8.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[item] += 5.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[item] += 7.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Wrist Length'):
                        possible_answer[item] += 8.0
                    elif (item['sleeve_length'] == 'Short Sleeves'
                            or item['sleeve_length'] == '3/4 Sleeves'):
                        possible_answer[item] += 9.0
                    elif item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[item] += 3.0
                    elif item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[item] += 1.0
            elif 20.0 <= temperature < 30.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length'
                            or item['coat_length'] == 'Long Length'
                            or item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[item] += 0.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[item] += 6.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 5.0
                    elif (item['coat_length'] == 'Knee Length'
                            or item['coat_length'] == 'Midi Length'):
                        possible_answer[item] += 1.0
                if 'skirt_length' in item:
                    if (item['skirt_length'] == 'Short Length'
                        or item['skirt_length'] == 'Knee Length'):
                        possible_answer[item] += 9.0
                    elif item['skirt_length'] == 'Midi Length':
                        possible_answer[item] += 8.0
                    elif item['skirt_length'] == 'Ankle Length':
                        possible_answer[item] += 6.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[item] += 3.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[item] += 9.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Short Length'
                            or item['sleeve_length'] == 'Elbow Sleeves'):
                        possible_answer[item] += 10.0
                    elif item['sleeve_length'] == '3/4 Sleeves':
                        possible_answer[item] += 7.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[item] += 5.0
                    else:
                        possible_answer[item] += 0.0
            elif 30.0 <= temperature < 40.0:
                if 'coat_length' in item:
                    if item['coat_length'] == 'Micro Length':
                        possible_answer[item] += 2.0
                if 'skirt_length' in item:
                    if item['skirt_length'] == 'Short Length':
                        possible_answer[item] += 10.0
                    elif item['skirt_length'] == 'Knee Length':
                        possible_answer[item] += 9.0
                    elif item['skirt_length'] == 'Midi Length':
                        possible_answer[item] += 8.0
                    elif item['skirt_length'] == 'Ankle Length':
                        possible_answer[item] += 3.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[item] += 1.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[item] += 10.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Short Length'):
                        possible_answer[item] += 9.0
                    elif item['sleeve_length'] == 'Elbow Sleeves':
                        possible_answer[item] += 8.0
                    elif item['sleeve_length'] == '3/4 Sleeves':
                        possible_answer[item] += 7.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[item] += 6.0

        if matchType == 'bottoms':
            if temperature < -10.0 or -10.0 <= temperature < 0.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[item] += 10.0
            elif 0.0 <= temperature < 10.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[item] += 10.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[item] += 5.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[item] += 3.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[item] += 2.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[item] += 1.0
            elif 10.0 <= temperature < 20.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[item] += 9.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[item] += 10.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[item] += 7.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[item] += 6.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[item] += 5.0
            elif 20.0 <= temperature < 30.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[item] += 6.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[item] += 8.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[item] += 8.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[item] += 8.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[item] += 8.0
            elif 30.0 <= temperature < 40.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[item] += 4.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[item] += 7.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[item] += 8.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[item] += 9.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[item] += 10.0