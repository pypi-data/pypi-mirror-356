# Spire API Python Client

A robust and extensible Python client for interacting with the [Spire Business Software API](https://developer.spiresystems.com/reference). This client provides an object-oriented interface to get, create, update, delete, query, filter, sort, and manage various Spire modules such as Sales Orders, Invoices, Inventory Items, and more.

---

## ✨ Features

- ✅ Object-oriented resource wrappers for each module (e.g., `salesOrder`, `invoice`, `item`)
- 🔍 Full-text search via `q` parameter
- 🔁 Pagination with `start` and `limit` support
- 🧾 JSON-based advanced filtering (supports `$gt`, `$lt`, `$in`, `$or`, etc.)
- ↕️ Multi-field sorting with ascending/descending control
- 🔧 Clean abstraction layer for API endpoints
- 📦 Powered by `pydantic` models for validation

---

## 📦 Installation

```bash
pip install -r requirements.txt
