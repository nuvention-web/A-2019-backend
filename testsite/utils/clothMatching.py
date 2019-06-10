from utils import colorDetect
from utils import weather


def selectMatchCloth(user, temperature, hsv, matchType, colorTbl):

    possible_answer = calWeatherScore(user, temperature, matchType)
    print('possible-answer =>', possible_answer)

    matchCloth = None
    maxScore = 0.0

    for key, item in user.val()['items'].items():
        if item and item['type'] == matchType:
            tcolor = item['color']
            rgb = colorTbl[tcolor]
            hsv2 = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
            score = colorDetect.CalColorGrade(hsv, hsv2)
            if key in possible_answer:
                score += possible_answer[key]
            if score > maxScore:
                maxScore = score
                matchCloth = item

    return matchCloth, maxScore


def calWeatherScore(user, temperature, matchType):
    possible_answer = {}

    for key, item in user.val()['items'].items():
        if item == None or item['type'] != matchType:
            continue
        possible_answer[key] = 0
        if matchType == 'tops':
            if temperature < -10.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[key] += 10.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[key] += 8.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[key] += 7.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 2.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[key] += 10.0
                    elif item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[key] += 9.0
            elif -10.0 <= temperature < 0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Regular Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[key] += 10.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[key] += 8.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 2.0
                if 'sleeve_length' in item:
                    if (item['sleeve_length'] == 'Extra Long Sleeves' or
                            item['sleeve_length'] == 'Long Sleeves'):
                        possible_answer[key] += 10.0
                else:
                    possible_answer[key] += 0.0
            elif 0.0 <= temperature < 10.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'Regular Length' or
                            item['coat_length'] == 'Midi Length'):
                        possible_answer[key] += 10.0
                    elif (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Long Length' or
                            item['coat_length'] == 'Knee Length' or
                            item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[key] += 9.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 8.0
                elif 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[key] += 10.0
                    elif item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[key] += 8.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[key] += 6.0
            elif 10.0 <= temperature < 20.0:
                if 'coat_length' in item:
                    if item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 10.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[key] += 7.0
                    elif item['coat_length'] == 'Midi Length':
                        possible_answer[key] += 6.0
                    elif (item['coat_length'] == 'High Waist Length' or
                            item['coat_length'] == 'Knee Length'):
                        possible_answer[key] += 5.0
                    elif item['coat_length'] == 'Long Length':
                        possible_answer[key] += 4.0
                    elif item['coat_length'] == 'Ankle&Floor Length':
                        possible_answer[key] += 3.0
                if 'skirt_length' in item:
                    if (item['skirt_length'] == 'Short Length'
                        or item['skirt_length'] == 'Ankle Length'):
                        possible_answer[key] += 7.0
                    elif (item['skirt_length'] == 'Knee Length'
                        or item['skirt_length'] == 'Midi Length'):
                        possible_answer[key] += 8.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[key] += 5.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[key] += 7.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Wrist Length'):
                        possible_answer[key] += 8.0
                    elif (item['sleeve_length'] == 'Short Sleeves'
                            or item['sleeve_length'] == '3/4 Sleeves'):
                        possible_answer[key] += 9.0
                    elif item['sleeve_length'] == 'Long Sleeves':
                        possible_answer[key] += 3.0
                    elif item['sleeve_length'] == 'Extra Long Sleeves':
                        possible_answer[key] += 1.0
            elif 20.0 <= temperature < 30.0:
                if 'coat_length' in item:
                    if (item['coat_length'] == 'High Waist Length'
                            or item['coat_length'] == 'Long Length'
                            or item['coat_length'] == 'Ankle&Floor Length'):
                        possible_answer[key] += 0.0
                    elif item['coat_length'] == 'Regular Length':
                        possible_answer[key] += 6.0
                    elif item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 5.0
                    elif (item['coat_length'] == 'Knee Length'
                            or item['coat_length'] == 'Midi Length'):
                        possible_answer[key] += 1.0
                if 'skirt_length' in item:
                    if (item['skirt_length'] == 'Short Length'
                        or item['skirt_length'] == 'Knee Length'):
                        possible_answer[key] += 9.0
                    elif item['skirt_length'] == 'Midi Length':
                        possible_answer[key] += 8.0
                    elif item['skirt_length'] == 'Ankle Length':
                        possible_answer[key] += 6.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[key] += 3.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[key] += 9.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Short Length'
                            or item['sleeve_length'] == 'Elbow Sleeves'):
                        possible_answer[key] += 10.0
                    elif item['sleeve_length'] == '3/4 Sleeves':
                        possible_answer[key] += 7.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[key] += 5.0
                    else:
                        possible_answer[key] += 0.0
            elif 30.0 <= temperature < 40.0:
                if 'coat_length' in item:
                    if item['coat_length'] == 'Micro Length':
                        possible_answer[key] += 2.0
                if 'skirt_length' in item:
                    if item['skirt_length'] == 'Short Length':
                        possible_answer[key] += 10.0
                    elif item['skirt_length'] == 'Knee Length':
                        possible_answer[key] += 9.0
                    elif item['skirt_length'] == 'Midi Length':
                        possible_answer[key] += 8.0
                    elif item['skirt_length'] == 'Ankle Length':
                        possible_answer[key] += 3.0
                    elif item['skirt_length'] == 'Floor Length':
                        possible_answer[key] += 1.0
                if 'sleeve_length' in item:
                    if item['sleeve_length'] == 'Sleeveless':
                        possible_answer[key] += 10.0
                    elif (item['sleeve_length'] == 'Cup Sleeves'
                            or item['sleeve_length'] == 'Short Length'):
                        possible_answer[key] += 9.0
                    elif item['sleeve_length'] == 'Elbow Sleeves':
                        possible_answer[key] += 8.0
                    elif item['sleeve_length'] == '3/4 Sleeves':
                        possible_answer[key] += 7.0
                    elif item['sleeve_length'] == 'Wrist Length':
                        possible_answer[key] += 6.0

        if matchType == 'bottoms':
            if temperature < -10.0 or -10.0 <= temperature < 0.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[key] += 10.0
            elif 0.0 <= temperature < 10.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[key] += 10.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[key] += 5.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[key] += 3.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[key] += 2.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[key] += 1.0
            elif 10.0 <= temperature < 20.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[key] += 9.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[key] += 10.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[key] += 7.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[key] += 6.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[key] += 5.0
            elif 20.0 <= temperature < 30.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[key] += 6.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[key] += 8.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[key] += 8.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[key] += 8.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[key] += 8.0
            elif 30.0 <= temperature < 40.0:
                if 'pant_length' in item:
                    if item['pant_length'] == 'Full Length':
                        possible_answer[key] += 4.0
                    elif item['pant_length'] == 'Cropped Pant':
                        possible_answer[key] += 7.0
                    elif item['pant_length'] == '3/4 Length':
                        possible_answer[key] += 8.0
                    elif item['pant_length'] == 'Mid Length':
                        possible_answer[key] += 9.0
                    elif item['pant_length'] == 'Short Pant':
                        possible_answer[key] += 10.0

    return possible_answer

def calScoreBetweenClothes(cloth, matchCloth, type):
    score = 0
    if type == 'formal':
        if 'lapel_design' in cloth:
            if cloth['lapel_design'] == 'Shawl Collar':
                score = 10.0
    elif type == 'semiformal':
        if 'lapel_design' in cloth:
            if cloth['lapel_design'] == 'Notched':
                score = 10.0
    elif type == 'casual':
        if 'lapel_design' in cloth:
            if (cloth['lapel_design'] == 'Collarless'
                or cloth['lapel_design'] == 'Plus Size Shawl'):
                score = 10.0

    return score


def calOccasionScore(user, colorTbl):
    formal = -1
    formalDress = []
    semiformal = -1
    semiformalDress = []
    casual = -1
    casualDress = []
    temperature = weather.getWeatherInfo()

    for key, item in user.val()['items'].items():
        if item == None:
            continue
        if item['type'] == 'tops':
            print('is it here???')
            tcolor = item['color']
            rgb = colorTbl[tcolor]
            hsv = colorDetect.CalHSV(rgb[0], rgb[1], rgb[2])
            matchCloth, matchScore = selectMatchCloth(user, temperature, hsv, 'bottoms', colorTbl)

            tmpFormal = calScoreBetweenClothes(item, matchCloth, 'formal')
            tmpSemiFormal = calScoreBetweenClothes(item, matchCloth, 'semiformal')
            tmpCasual = calScoreBetweenClothes(item, matchCloth, 'casual')

            if tmpFormal > formal or formal == -1:
                formal = tmpFormal
                formalDress = [item, matchCloth]

            if tmpSemiFormal > semiformal or semiformal == -1:
                semiformal = tmpSemiFormal
                semiformalDress = [item, matchCloth]

            if tmpCasual > casual or casual == -1:
                casual = tmpCasual
                casualDress = [item, matchCloth]

    return [formalDress, semiformalDress, casualDress]