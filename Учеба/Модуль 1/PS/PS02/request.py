import requests as rq
import pprint as pp

from requests import Response

def get_task_1()-> Response:
   param = {
      "q": "html"
   }

   return rq.request("GET", "https://api.github.com/", params=param)

def get_task_2()-> Response:
   param = {
      "userId": 1
   }

   return rq.request("GET", "https://jsonplaceholder.typicode.com/posts", params=param)

def post_task_3()-> Response:
   param = {
      'title': 'foo',
      'body': 'bar',
      'userId': 1
   }

   return rq.request("POST", "https://jsonplaceholder.typicode.com/posts", params=param)

if __name__ == '__main__':
   response_1 = get_task_1()
   pp.pprint(response_1.status_code)
   pp.pprint(response_1.content)

   response_2 = get_task_2().json()
   pp.pprint(response_2)

   response_3 = post_task_3()
   pp.pprint(response_3.status_code)
   pp.pprint(response_3.content)
