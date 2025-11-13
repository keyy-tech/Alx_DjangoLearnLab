# Django Permissions and Groups Setup

## Overview
This application demonstrates how to use **custom permissions** and **user groups** in Django to control access to different model actions.

## 1️⃣ Model Permissions
Custom permissions are defined in the `Book` model (`bookshelf/models.py`) as:

```python
permissions = [
    ("can_view", "Can view book records"),
    ("can_create", "Can create new book records"),
    ("can_edit", "Can edit existing book records"),
    ("can_delete", "Can delete book records"),
]
