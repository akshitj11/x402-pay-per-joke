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


@app.route('/')
def home():
    return jsonify({
        'service': 'x402 pay-per-joke API',
        'version':'1.0.0',
        'price': f'{PAYMENT_AMOUNT}ETH per joke',
        'payment_address':WALLET_ADDRESS,
        'NETWORK':'BASE SEPOLIA TESTNET',
        'blockchain_connected':w3.is_connected(),
        'endpoints':{
            'GET/JOKE':'get a joke',
            'POST/verify':'verify your payment',
            'GET /stats':'API statistics'
        }

    })
@app.route('/joke',methods=['GET'])
def get_joke():
        payment_proof=request.headers.get('X-Payment-Proof')
    if not payment_proof:
        return jsonify({
            "error": "Payment Required",
            "code": 402,
            "message": "You need to pay to access this joke",
            "payment_details": {
                "amount": f"{PAYMENT_AMOUNT} ETH",
                "recipient": WALLET_ADDRESS,
                "network": "Base Sepolia Testnet",
                "chain_id": 84532
            },
            "instructions": [
                "1. Send payment via phantom to the address above",
                "2. Copy the transaction hash",
                "3. POST to /verify with your transaction hash",
                "4. Retry this request with X-Payment-Proof header"
            ]
        })
    
    # Check if payment is verified
    if payment_proof not in verified_payments:
        return jsonify({
            "error": "Payment Not Verified",
            "code": 402,
            "message": "Payment proof not recognized. Have you verified it?",
            "instructions": "POST your transaction hash to /verify first"
        }), 402
    
    # Payment verified - return joke
    joke = random.choice(JOKES)
    payment_info = verified_payments[payment_proof]
    return jsonify({
        "joke": joke,
        "payment": {
            "verified": True,
            "amount": payment_info['amount'],
            "transaction": payment_proof,
            "from": payment_info['from']
        },
        "timestamp": int(time.time())
    })

@app.route('/verify',method=['POST'])
def verify_payment():
     data=request.get_json()
     if not data or'transactionhash' not in data:
          return jsonify({
               'error':'missing transaction hash',
               'message':'please provide transactionhash in request body'

          }),400

tx_hash = data['transactionHash']

if not tx_hash.startswith('0x') or len(tx_hash) !=66:
     return jsonify({
          'error':'invalid transaction hash format',
          'message':'transaction hash should be 66 characters starting 0x'

     }),400

if tx_hash in verified_payments:
     return jsonify({
          'verified':True,
          'message':'payment already verified',
          'transaction':tx_hash
          'note':'you can use this transaction hash in X-Payment-Proof'

     })

is_valid,message,tx_details = verofy_transaction_on_chain(tx_hash)

if is_valid:
     verified_payments[tx_hash] = tx_details
     return jsonify({
          'verfied':True,
          'message':'payment verified successfully',
          'details':{
               'amount':f'{tx_details['amount']}ETH',
               'block':tx_details['block'],
               'from':tx_details['from']
          }
          'next_step':'now request /joke with x-payment-proof header set to this transaction hash'
     })
 else:
     return jsonify({
          'verified':False,
          'message':message,
          'transaction':tx_hash
     }),400
@app.route('/stats', methods=['GET'])
def stats():
    """API statistics"""
    return jsonify({
        "total_payments": len(verified_payments),
        "price_per_joke": f"{PAYMENT_AMOUNT} ETH",
        "total_revenue": f"{sum(p['amount'] for p in verified_payments.values())} ETH",
        "blockchain_connected": w3.is_connected(),
        "network": "Base Sepolia"
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 x402 Pay-Per-Joke API Starting...")
    print("=" * 60)
    print(f"💰 Payment Address: {WALLET_ADDRESS}")
    print(f"💵 Price: {PAYMENT_AMOUNT} ETH per joke")
    print(f"🌐 Network: Base Sepolia Testnet")
    print(f"🔗 Blockchain Connected: {w3.is_connected()}")
    print("=" * 60)
    print("📝 Endpoints:")
    print("   GET  /          - API info")
    print("   GET  /joke      - Get joke (needs payment)")
    print("   POST /verify    - Verify payment")
    print("   GET  /stats     - Statistics")
    print("=" * 60)
    print("🎯 Running on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
  