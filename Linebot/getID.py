import requests


url = "https://docs.google.com/forms/d/1dVLgIKjuJBe0otxKrqz4yEChKev4O3fQAAA5fKxBJWw/edit#responses"

response = requests.get(url)
data = response.content
print(data)
