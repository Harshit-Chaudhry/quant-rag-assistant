from google import genai

client = genai.Client(api_key="AIzaSyB3N43YasKwC_TGyM33e1tVyfcjV5B1_1Y")
for model in client.models.list():
    print(model.name)