import google.generativeai as genai

genai.configure(api_key="AIzaSyDYbXVgAX-9N-RLXXCxfbwv_D3jQ4e12eM")

for m in genai.list_models():
    print(m.name)