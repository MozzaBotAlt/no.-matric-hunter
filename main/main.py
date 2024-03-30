from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Union

from bs4 import BeautifulSoup
from pydantic import BaseModel
import requests

app = FastAPI(title='Epelajar API MRSM Langkawi', description='An API server for the epelajar MRSM Langkawi asp systems written by the bypasser')

#Basemodel Classes ==========================================
class userDat(BaseModel):
  id: str
  ic: str
  year: str

#Functions ==========================================
def preparehtml(response : str) :
  datA= """
  <html>
  <head>
  <title>AI API Chat</title>
  </head>
  <body>
  <h1>"""

  datB = """</h1>
  </body>
  </html>
  """
  return datA + response + datB

#GET Methods ==========================================
@app.get("/")
def read_root():
  return {"value": "ok"}

@app.get("/DataPeribadi/{year}/{id}")
def get_profile(year: str, id: str) :
  returndat = {"error" : "unknown"}

  url = "https://uppmmrsmlangkawi.com/epelajar/DataPeribadi.asp"

  payload = {
    "txtNoMak": id,
    "txtPwd": "",
    "cboTahun": year
  }

  #send request
  response = requests.post(url, data=payload)

  if response.status_code == 200:
    returndat = response.text
  else:
    fail = "Failed to retrieve. Status code: " + str(response.status_code)
    returndat = preparehtml(fail)

  return HTMLResponse(content=returndat)

#POST Methods ==========================================
@app.post("/profile/") #get DM message list
async def sendprofile(dat : userDat) :
  returndat = {"error" : "unknown"}

  url = "https://uppmmrsmlangkawi.com/epelajar/DataPeribadi.asp"

  payload = {
    "txtNoMak": dat.id,
    "txtPwd": dat.ic,
    "cboTahun": dat.year
  }

  #send request
  response = requests.post(url, data=payload)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    p_elements = soup.find_all("span")
    num = 0
    profile = {}

    while num <= 22 :
      if (num % 2) == 0:
        profile[p_elements[num].text.strip()] = p_elements[num+1].text.strip()

      num += 1
    profile['ALAMAT SURAT MENYURAT'] = [p_elements[25].text.strip(), p_elements[26].text.strip(), p_elements[27].text.strip(), p_elements[28].text.strip()]
    profile[p_elements[29].text.strip()] = p_elements[30].text.strip()
    returndat = profile
  else:
    fail = "Failed to retrieve. Status code: " + str(response.status_code)
    returndat = {"error" : fail}

  return returndat


