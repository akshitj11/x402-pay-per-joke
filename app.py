from flask import Flask, jsonify, request
from web3 import web3
import os
from dotenv import load_dotenv
import random 
import time
load_dotenv()
app = flask(__name__)

#blockchain implementation
w3=web3(web3.HTTPProvider(os.getenv('alchemy url')))

