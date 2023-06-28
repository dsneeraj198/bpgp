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
                        [{"product": "t-shirt", "price": "$23"}, {"product": "trousers", "price": "$15"}, {"product": "shoes", "price": "$39"}]
                        """
    query =  f"""This is the product catalogue: {product_catalogue} \
              Please calculate the deal size:{content} \
               "Try to give a priority score to this email based on how likely this email will leads to a good \
              business opportunity, from 0 to 10; 10 most important" \
              Also, extract order details information, including which product clients want to buy, how many they want to buy \
              What is the recommendation for the Sales Team to move this forward? \
              Also, Try to identify the amount of products the client wants to purchase, if any \
              Also, Write an acknowledgement to the client in persuading tone in not more than 20 words \
              Format your response as a JSON object with \
              "DealSize", "ProductName", "CompanyName", "Priority", "Recommendation", "Amount", "Acknowledgement" as the key. \
              If information isn't present, use "unknown" as the value. \
              If "ProductName" is not present in {product_catalogue} then us unknown in "DealSize"
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
    priority = eval(arguments).get("Priority")
    recommendation = eval(arguments).get("Recommendation")
    amount = eval(arguments).get("Amount")
    reply = eval(arguments).get("Acknowledgement")

    return {
          "dealsize": deal_size,
          "company": company_name,
          "product": product_name,
          "recommendation":recommendation,
          "priority":priority,
          "amount":amount,
          "reply":reply
      }
