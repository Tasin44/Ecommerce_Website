# Django E-commerce Platform
## 📖 About
This Django-based e-commerce platform provides a complete online shopping experience with robust backend functionality. The application includes user registration with email verification, product catalog with categories, shopping cart management, order processing, product reviews,and an admin dashboard.
## ✨ Features

### Authentication System

* User registration with email verification
* Secure login/logout functionality
* Account activation via email links
* Custom user model with additional fields

### Product Management

* Product catalog with categories
* Product search and filtering
* Product details with images
* Product reviews and ratings

### Shopping Experience

* Shopping cart functionality
* Add/remove/update cart items
* Session-based cart for guests
* User-specific cart for authenticated users
* Cart persistence across sessions

### Order Management

* Order creation and processing
* Order history for users
* Order status tracking
* Order confirmation system
* Detailed order information

### Review System

* Product rating (1-5 stars)
* Written reviews
* One review per user per product
* Review editing capability

🛠️ Tools and Technologies

### Frontend:

* HTML
* Tailwind CSS
* JavaScript

### Backend:
* Python
* Django

### Database:
* PostgreSQL

### Email Service:

* Django Email Backend
* SMTP Configuration

### Others:

* Django Admin Interface
* Django Forms
* Django Authentication System
* Django Messages Framework


## 📋Setup Instructions to Run

Follow these steps to set up the project on your local machine.
Prerequisites (Install):
* Python 3.x
* Django 3.x
* A SQL database (e.g., SQLite, PostgreSQL)
* Git
* pip (Python package manager)

  
## 🚀 Run
1. Clone the repository
```
git clone https://github.com/Tasin44/Ecommerce_Website.git
cd django-ecommerce
```
2. Create and activate a virtual environment
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Database Setup
Create a PostgreSQL database and update your settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
5. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```
6. Create a superuser:
```
python manage.py createsuperuser
```
7. Run the development server
```
python manage.py runserver
```
The application will be available at http://127.0.0.1:8000/

## 📁 Project Structure:
```
django-ecommerce/
├── authapp/                 # User authentication app
│   ├── models.py           # Custom user model
│   ├── views.py            # Auth views (login, signup, etc.)
│   ├── forms.py            # Authentication forms
│   └── admin.py            # User admin configuration
|   └── templates            
├── storeapp/               # Main store app
│   ├── models.py           # Product, Category, Review models
│   ├── views.py            # Product listing and detail views
│   ├── forms.py            # Review forms
│   └── admin.py            # Store admin configuration
├── cartapp/                # Shopping cart app
│   ├── models.py           # Cart and CartItem models
│   ├── views.py            # Cart management views
│   └── utils.py            # Cart utility functions
|   └── templates 
├── ordersapp/              # Order management app
│   ├── models.py           # Order and OrderItem models
│   ├── views.py            # Order processing views
│   ├── forms.py            # Order forms
│   └── admin.py            # Order admin configuration
|   └── templates 
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Project Flow and Frontend View:

### Signup

![signup](https://github.com/user-attachments/assets/1571ea00-88ab-436f-8e8f-ed4263850874)


### Login

![login1](https://github.com/user-attachments/assets/a7d16cfe-57e6-4c1d-9231-0a642ce84604)

### Overview of the shoping site

![overview](https://github.com/user-attachments/assets/8e5dd66a-48f1-4ed6-b683-202632dc1d7b)

### Add to cart and giving review: 

![Add to cart and giving review](https://github.com/user-attachments/assets/9d906490-ce28-4e7f-a720-614b9351ae5e)

### My Cart

![mycart1](https://github.com/user-attachments/assets/f1d167e6-2c6d-467f-85ec-71061829bb39)

### Checkout Page

![checkout2](https://github.com/user-attachments/assets/e0b761d8-5751-4503-a50a-71e266205942)

### Order Confirmation 

![orderconfirmation](https://github.com/user-attachments/assets/ebc9f8e6-c07e-4149-8d4d-1c9f39674b8b)

