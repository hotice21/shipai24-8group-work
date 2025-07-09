import pyinputplus
def food_type(list):
    food = pyinputplus.inputMenu(list)
    return food
list = []
print('What kinds of broad do you like')
list.append(food_type(['wheat','white','sourdough']))
print('What kinds of protein do you like')
list.append(food_type(['chicken','turkey','ham','tofu']))
cheese =pyinputplus.inputYesNo('Is cheese OK?')
if cheese == 'yes':
    list.append(food_type(['cheddar','swiss','mozzarella']))
for i in ['mayo','mustard','lettuce','tomato']:
    check = pyinputplus.inputYesNo(f'Is {i} OK?')
    if check == 'yes':
        list.append(i)
print(list)

