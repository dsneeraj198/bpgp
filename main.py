import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):

    content = email.content
    product_catalogue = """
                        [{"product": "t-shirt", "price": "$23"}, {"product": "pants", "price": "$15"}, {"product": "shoes", "price": "$39"}]
                        """
    query =  f"""This is the product catalogue: {product_catalogue} \
              Please calculate the deal size:{content} \
              Also, extract order details information, including which product clients want to buy, how many they want to buy \
              Format your response as a JSON object with \
              "DealSize", "ProductName", "CompanyName" as the key. \
              If the information isn't present, use "unknown" as the value. \
              Make your response as short as possible."""

    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
      # functions = function_descriptions,
      # function_call="auto"
  )

    arguments = response.choices[0].message["content"]
    deal_size = eval(arguments).get("DealSize")
    product_name = eval(arguments).get("ProductName")
    company_name = eval(arguments).get("CompanyName")

    return {
          "dealsize": deal_size,
          "product": product_name,
          "company": company_name
      }

