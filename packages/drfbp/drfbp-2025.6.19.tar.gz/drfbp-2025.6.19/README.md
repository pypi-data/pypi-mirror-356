# drfbp

**drfbp** (Django REST Framework Boilerplate) is a command-line tool that automatically generates boilerplate code for a Django REST Framework (DRF) app, including:

- `permissions.py`
- `serializers.py`
- `views.py`
- `urls.py`

Ideal for quickly scaffolding consistent DRF modules for any Django model.

---

## ✨ Features

- Clean and minimal boilerplate
- Generates DRF `ModelViewSet`, serializers, and permissions
- Fast CLI usage with a single command
- Easy to integrate into existing Django apps

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install drfbp
```

## 🚀 Usage

Inside your Django project directory, run:

```bash
drfbp <app_name> <model_name> <target_directory>
```

Example

```bash
drfbp core User ./core/api/user
```

This generates the following files under `./core/api/user/`:

- permissions.py
- serializers.py
- views.py
- urls.py

## 📂 Output Structure

Each generated file contains minimal boilerplate:

- permissions.py: A BasePermission allowing all access by default.
- serializers.py: A basic ModelSerializer for your model.
- views.py: A ModelViewSet using the serializer and permission.
- urls.py: A DRF router that registers the viewset.

You can freely modify these after generation.

## 🧪 Requirements

- Python 3.8+
- Django (expected installed in your project)
- Django REST Framework

**Note**: `drfbp` itself has no external dependencies — it assumes you're working inside a Django + DRF environment.

## 🛠️ Development

To build from source:

```bash
git clone https://github.com/gerardoaballesterjr/drfbp.git
cd drfbp
pip install .
```

Then use it just like the installed version:

```bash
drfbp core User ./core/api/user
```
