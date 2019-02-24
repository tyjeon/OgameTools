# csv 파일을 읽어온 뒤, 각 열을 각각의 리스트에 집어넣기.
# Python
# https://ngee.tistory.com/406

import csv

matrix = []
names = []
numbers = []

#test.csv는 name, number 두 종류의 데이터를 가지고 있다.
with open('test.csv', 'r') as r:
    csvReader=csv.reader(r)
    for row in csvReader:
        name.append(row[0])
        number.append(row[1])

print(name)
print(number)
