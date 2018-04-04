import requests
data ={
  'username':'admin',
  'password':'admin'

}
html = requests.post('http://127.0.0.1:8080/login',data=data)
print(html.text)