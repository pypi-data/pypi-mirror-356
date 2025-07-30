# Lisk Name Service SDK (Python)

> A lightweight Python SDK to resolve `.lisk` names into wallet addresses via the Lisk Name Service API.

## ✨ Features

- 🔐 Secure resolution via API key
- 🧠 Simple `resolve(name)` method
- 📦 Supports tree-shaking and Python modules

---

## 📦 Install

```bash
pip install lisk-name-service
```

## Usage

```
from lns_sdk import LNSClient

client = LNSClient("your-api-key")
print(client.resolve("myname"))
```

## API

client = LNSClient("your-api-key")

Create a new client instance.

    `apiKey` – your unique API key (provided after wallet connect).


`resolve(name: string): Promise<string>`

Resolves a .lisk name to its associated Ethereum-compatible wallet address.

Returns:

    address: string – the resolved Ethereum-compatible wallet address.

    ValueError if the name is missing or not found

	RuntimeError for other network issues

## 🧪 Build (for contributors)

```
# from inside sdk/python/
pip install -e .
python3 -m tests.test_client
```

## 🔐 Notes

    You must generate your API key by authenticating with your wallet on the LNS frontend.

    Make sure your API key is kept secret and never exposed in frontend code.
