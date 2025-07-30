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

## ⚠️ Data Synchronization Notice

**Important:** The seizure times stored in the database are aligned with **hospital data** and not guaranteed to be synchronized with **wearable recordings**.

There are two critical issues to be aware of:

1. **Incorrect Wearable Timestamps:**  
   Some sessions contain wearable files where the initial timestamp is incorrect (e.g., starts exactly at `10:00:00`, which may be a placeholder or default value).
2. **No Guaranteed Synchronization:**  
   Even when the wearable data has plausible timestamps, they are **not guaranteed to be aligned** with hospital data for the same session.

The patient codes for which the wearable timestamps are known to be reliable are: **BLIW, BSEA, GPPF, OFUF, RGNI, UDZG, YIVL**.

> ⚠️ If you are comparing or aligning events between wearable and hospital data, **you must implement a synchronization method** (e.g., heart rate signal alignment).

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
