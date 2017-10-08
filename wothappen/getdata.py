from flask import Flask, render_template, request, session, url_for, redirect, json

import requests

def getMessages(_roomId):
  url = (
    "https://api.ciscospark.com/v1/messages?roomId=%s" %_roomId+
    "&max=1000"
  )
  headers = {
    'Content-type': 'application/json; charset=utf-8',
    'Authorization': 'Bearer NmZlNGIzNjktMTc3YS00MDM1LTk0NDAtNzQ0MzFkZWJmNzk0Zjc2M2E1YTItOWU1',
  }
  roomMessages = requests.get(url, headers=headers)
  return roomMessages
