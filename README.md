# QuickCartz (E‑commerce Web Application)

QuickCartz is a full‑stack **Django-based e‑commerce web application** built to understand real‑world backend development concepts such as authentication, payments, transactional emails, and deployment.

---

## Features

* Product listing & product details
* Product search
* Cart system
* Checkout & order placement
* PayPal payment flow
* Product ratings & reviews
* User dashboard (profile & order details)
* Email verification during signup
* Forgot password & reset via email
* Order confirmation email with order & payment details

---

## Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* JavaScript
* jQuery
* Bootstrap

### Database

* PostgreSQL

### Integrations

* PayPal (Payment Gateway)
* Brevo (Sendinblue) API – transactional emails
* Cloudinary – image & media storage

### Deployment

* Render

---

## Screenshots

Screenshots of the following pages are included:

* Home page
* Product listing
* Product details
* Cart
* Checkout
* Payment & payment success
* Order placed
* Email confirmation

---

## Authentication & Email Flow

* User signup with **email verification**
* Forgot password & reset password via email
* **Automated transactional email** sent after successful order placement with order and payment details

---

## Installation & Setup

1. Clone the repository

```bash
git clone https://github.com/ankush21sali/quickcartz-django.git
cd quickcartz
```

2. Create virtual environment & activate

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables
   Create a `.env` file and add:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
BREVO_API_KEY=your_brevo_api_key
CLOUDINARY_URL=your_cloudinary_url
```

5. Apply migrations

```bash
python manage.py migrate
```

6. Run the server

```bash
python manage.py runserver
```

---

## Learning Outcome

This project helped me gain hands‑on experience with:

* Django backend architecture
* Authentication & authorization flows
* Payment gateway integration
* Transactional email handling
* Media storage using Cloudinary
* Production deployment and debugging

---

## Author

**Ankush Sali**
Aspiring Python Backend Developer and DevOps Enthusiast
