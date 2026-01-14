from langchain_google_genai import genai
model=ChatGoogleGenerativeAI(model="gemini-2.5-pro",temperature=0.7)
pront="hi"
response=model.generate_content(pront)
print(response)