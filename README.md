# x402 Pay-Per-Joke API

Learning the x402 payment protocol by building a simple micropayment API. Pay crypto, get jokes.

## What is this?

HTTP 402 "Payment Required" implementation using blockchain payments. No auth, no accounts—just pay 0.01 ETH per joke.

## Stack

- Python/Flask
- Web3.py for blockchain interaction
- Base Sepolia testnet

## Setup

```bash
pip install flask web3 python-dotenv
```

Create `.env`:
```
ALCHEMY_URL=https://base-sepolia.g.alchemy.com/v2/YOUR_KEY
WALLET_ADDRESS=0xYourAddress
PAYMENT_AMOUNT=0.01
```

Run:
```bash
python app.py
```

## Usage

1. Request joke → get 402 with payment address
2. Send ETH via MetaMask → copy tx hash
3. Verify payment: `POST /verify-payment` with tx hash
4. Request joke again with `X-Payment-Proof: <tx_hash>` header

## Flow

```
Client → GET /joke
       ← 402 Payment Required

Client sends 0.01 ETH on-chain
       → POST /verify-payment {transactionHash}
       ← 200 Verified

Client → GET /joke (with X-Payment-Proof header)
       ← 200 {joke, paid}
```

## Key Implementation

- Flask returns 402 status code with payment details
- Web3.py verifies transactions on Base Sepolia
- In-memory storage for verified payments (use Redis/DB for prod)
- No user accounts or API keys needed


Built as a learning project for the x402 protocol. Testnet only.
