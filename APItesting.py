from google import genai

client = genai.Client(api_key="AIzaSyD2-0BIDMFlJdnE0vQ2aV-wbhhHcuE4mZw")
for model in client.models.list():
    print(model.name)