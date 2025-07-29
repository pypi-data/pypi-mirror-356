# preepiseizures-api-client

Python client for interacting with the [PreEpiSeizures API](https://github.com/anascacais/preepiseizures-api).

This client simplifies access to authorized endpoints for researchers working with seizure-related data.

---

## 🚀 Installation

Install from PyPI:

```bash
pip install preepiseizures-api-client
```

---

## 📦 Usage

```python
from preepiseizures_api_client.client import PreEpiSeizuresDBClient

client = PreEpiSeizuresDBClient(
    api_url="http://localhost:8000", # or your remote server URL
    username="myusername",
    password="mypassword"
)
```

---

## 🔐 Authentication

The client handles authentication automatically:

- Authenticates with the provided username and password
- Requests a bearer token from the API
- Uses the token to authorize future requests

---

## 📂 Examples

See the `examples/example_query.py` file for a complete usage example.

---

## 🧾 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙋‍♀️ Author

Created by Ana Sofia Carmo  
Email: anascacais@gmail.com  
GitHub: [@anascacais](https://github.com/anascacais)
