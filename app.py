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

verified_payments = {}
def verify_transaction_on_chain(tx_hash):
    try:
        print(f"verifying transaction:{tx_hash}")

        tx = w3.eth.get_transaction(tx_hash)
        receipt= w3.eth.get_transaction_receipt(tx_hash)

        if receipt['status']!=1:
            return False ,f"insufficient amount. need {PAYMENT_AMOUNT} ETH , got{amount_eth}ETH",None
        

        # Check 2: Sent to correct address
        if tx['to'].lower() != WALLET_ADDRESS.lower():
            return False, f"Wrong recipient. Expected {WALLET_ADDRESS}, got {tx['to']}", None
        
        # Check 3: Correct amount
        amount_eth = w3.from_wei(tx['value'], 'ether')
        if float(amount_eth) < PAYMENT_AMOUNT:
            return False, f"Insufficient amount. Need {PAYMENT_AMOUNT} ETH, got {amount_eth} ETH", None
        
        # Check 4: Not already used
        if tx_hash in verified_payments:
            return False, "Payment already used", None
        

        tx_details = {
            'from':tx['from'],
            'amount':tx['to'],
            'block':receipt['blockNumber'],
            'temstamp':int(time.time())

        }
        return True , "payment verified successfully",tx_details
    

    except Exception as e:
        print(f"Verification error: {str(e)}")
        return False, f"Error verifying transaction: {str(e)}", None
    