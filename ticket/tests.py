from django.test import TestCase
from django.db import connection

# Create your tests here.
# import requests
#
# url = "http://127.0.0.1:8000/APItickets/"
#
# response = requests.get(url)
#
# json_content = response.json()
#
# for goods in json_content:
#     print(goods)

cursor = connection.cursor()
cursor.execute(
    "select ticket_ticket_subtype.name,COUNT(*) AS subtypeSum from ticket_ticket_subtype inner join ticket_ticket ON  ticket_ticket_subtype.id = ticket_ticket.ticket_type_id group by ticket_ticket.ticket_type_id, ticket_ticket_subtype.name")

rows = cursor.fetchall()
rows = dict(rows)
# for i in rows:
#     print(i)
print(rows)