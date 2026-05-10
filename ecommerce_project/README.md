# E-Commerce Django Project

A fully-featured e-commerce website built with Django, featuring product catalog, shopping cart, order management, and user authentication.

## Features

- **Product Catalog**: Browse products by category with detailed product pages
- **Shopping Cart**: Add/remove items, update quantities
- **User Authentication**: Register, login, and manage profiles
- **Order Management**: Checkout, order history, and order tracking
- **Product Reviews**: Users can rate and review products
- **Admin Panel**: Manage products, orders, and users
- **Responsive Design**: Mobile-friendly interface

## Project Structure

```
ecommerce_project/
├── ecommerce/          # Project configuration
├── store/              # Product catalog app
├── cart/               # Shopping cart app
├── orders/             # Order management app
├── accounts/           # User authentication app
├── templates/          # HTML templates
├── static/             # CSS, JavaScript files
└── manage.py           # Django management script
```

## Installation

1. **Clone the repository**
   ```bash
   cd ecommerce_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Apps Overview

### Store App
- Product catalog with categories
- Product details and reviews
- Browse by category

### Cart App
- Shopping cart management
- Add/remove items
- Update quantities
- View cart total

### Orders App
- Checkout process
- Order creation
- Order history
- Order tracking

### Accounts App
- User registration
- User login/logout
- User profiles
- Profile management

## Database Models

- **User**: Django built-in user model
- **Product**: Product information and inventory
- **Category**: Product categories
- **ProductReview**: User reviews and ratings
- **Cart**: User shopping cart
- **CartItem**: Individual cart items
- **Order**: Customer orders
- **OrderItem**: Items in an order
- **UserProfile**: Extended user information

## Next Steps

1. Create HTML templates in `templates/` directory
2. Add static CSS and JavaScript files
3. Implement payment gateway integration (Stripe, PayPal)
4. Add search functionality
5. Add product filtering and sorting
6. Set up email notifications
7. Deploy to production (Heroku, AWS, DigitalOcean, etc.)

## Technologies Used

- Django 4.2
- SQLite (development) / PostgreSQL (production)
- Pillow (image handling)
- Bootstrap or Tailwind CSS (for styling)

## License

MIT License
