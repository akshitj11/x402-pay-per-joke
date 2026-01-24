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
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
PAYMENT_AMOUNT = float(os.getenv('PAYMENT_AMOUNT', 0.01))

# Joke database
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache!",
    "What's a programmer's favorite hangout? The Foo Bar!",
    "Why do Java developers wear glasses? Because they don't C#!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    "Why do Python programmers prefer snakes? Because they're already working with one!",
    "What do you call a programmer from Finland? Nerdic!",
    "Why did the programmer quit his job? Because he didn't get arrays!",
    "How do you comfort a JavaScript bug? You console it!",
    "Why do programmers always mix up Halloween and Christmas? Because Oct 31 == Dec 25!"
]

