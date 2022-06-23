from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
  pprint(contacts_list)

# тут сортировка фамилий по столбцам
for i in range(1, len(contacts_list)):
  strc = (str(contacts_list[i][0]) + ' ' + str(contacts_list[i][1]) + ' ' + str(contacts_list[i][2])).split()
  for j in range(len(strc)):
    contacts_list[i][j] = strc[j]

fio = list() # список с повторяющимися фамилиями
plist = list() # типо person list
new_persons_lists = list()
# начинаем попытку объединения
str_contacts_list = str(contacts_list)
for i in range(1, len(contacts_list)):
  if str_contacts_list.find(contacts_list[i][0]) != str_contacts_list.rfind(contacts_list[i][0]) and contacts_list[i][0] not in fio:
    fio.append(contacts_list[i][0])
for f in fio:
  for i in range(1, len(contacts_list)):
    if contacts_list[i][0] == f:
      plist.append(contacts_list[i])
  person_new_list = ['', '', '', '', '', '', '', '']
  for person in plist:
    for i in range(len(person)):
      if person_new_list[i] == '':
        person_new_list[i] = person[i]
  plist = []
  new_persons_lists.append(person_new_list)

new_contacts_list = list()

for p in contacts_list:
  if p[0] not in fio:
    new_contacts_list.append(p)

for p in new_persons_lists:
  new_contacts_list.append(p)

for p in new_persons_lists:
  if len(p) == 8:
    p.pop(7)

# приступаем к "чинке" телефонных номеров
res = str(new_contacts_list)
pattern = r'(\+7|8|\s)?(-|\s)?\(?(\d{3})\)?(-|\s)?(\d{3})(-|\s)?(\d{2})(-|\s)?(\d{2})\s?\(?(доб\.\s?\d*)?\s?\)?'
res = re.sub(pattern, r'+7(\3)\5-\7-\9', res)

# муки обратного преобразовывания в список
res = list(res)
while '[' in res:
  res.remove('[')
while ']' in res:
  res.remove(']')

new_res = ''
for i in res:
  new_res += i
new_res = new_res.split(', ')

for i in range(len(new_res)):
  new_res[i] = new_res[i][1:-1]

new_person = list()
new_contacts_list = list()
while len(new_res) != 0:
  for i in range(7):
    new_person.append(new_res[i])
  new_contacts_list.append(new_person)
  for i in range(7):
    new_res.pop(0)
  new_person = []

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contacts_list)

# фууух, ну главное работает))
