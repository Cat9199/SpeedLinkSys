<p align="center">
  <img src="https://raw.githubusercontent.com/Cat9199/SpeedLinkSys/main/static/images/logob.png" alt="SpeedLink Logo" width="512">
</p>
# SpeedLink Flask Application


SpeedLink is a Flask-based web application that manages shipments, shippers, deliveries, and related functionalities.

## Description

This application provides functionalities for managing shipments, shippers, deliveries, and more. It uses Flask as the web framework and SQLAlchemy for database interaction. Users with different roles, such as admins, shippers, and deliveries, can log in and perform various actions related to shipments and accounts.

## Features

- **Authentication:** Users can log in using their credentials, and their roles determine their access rights.

- **Admin Dashboard:** Admins can view and manage shipments, shippers, and deliveries.

- **Shipper Dashboard:** Shippers can manage their own shipments, track status, and more.

- **Delivery Dashboard:** Deliveries have a dedicated dashboard for their tasks.

- **Adding Shipments:** Shippers can add new shipments, providing recipient details, pricing, and more.

- **Barcode Handling:** The application includes barcode extraction and decoding functionalities.

- **Price Management:** Shipping prices for various cities can be configured and managed.

## Setup Instructions

1. Clone the repository to your local machine:
```
git clone https://github.com/your-username/speedlink-flask-app.git
```

2. Navigate to the project directory:
```
cd speedlink-flask-app
```

3. Install the required dependencies using pip:
```
pip install -r requirements.txt
```


4. Configure the application:
- Update the `app.config['SQLALCHEMY_DATABASE_URI']` with your database URI in the `app.py` file.
- Modify other configuration settings if needed.

5. Run the application:
```
python app.py
```


6. Access the application in your web browser at `http://localhost:2000`.


## Routes

1. `/setting`

   - Description: Displays settings page for the logged-in user.
   - Method: GET
   - Template: `setting.html`
   - Access: Authenticated users (admin, shipper, delivery)

2. `/`

   - Description: Displays the homepage.
   - Method: GET
   - Template: `index.html`
   - Access: Public

3. `/users`

   - Description: Displays a page listing all shippers.
   - Method: GET
   - Template: `users.html`
   - Access: Authenticated users (admin)

4. `/track/<int:barcode>`

   - Description: Displays shipment details and tracking for a specific barcode.
   - Method: GET
   - Template: `product.html`
   - Access: Authenticated users (admin, shipper, delivery)

5. `/login`

   - Description: Handles user authentication.
   - Method: GET, POST
   - Template: `login.html`
   - Access: Public

6. `/logout`

   - Description: Logs out the current user and clears session.
   - Method: GET
   - Access: Authenticated users

7. `/dashboard`

   - Description: Displays user-specific dashboard with relevant information.
   - Method: GET
   - Templates: `dashboard.html` (admin and shipper), `delivery-dashboard.html` (delivery)
   - Access: Authenticated users (admin, shipper, delivery)

8. `/adds`

   - Description: Displays a page for adding a new shipper account.
   - Method: GET
   - Template: `adds.html`
   - Access: Authenticated users (admin)

9. `/addd`

   - Description: Displays a page for adding a new delivery account.
   - Method: GET
   - Template: `addd.html`
   - Access: Authenticated users (admin)

10. `/addushipment`

    - Description: Displays a page for adding a new shipment by a shipper.
    - Method: GET
    - Template: `addushipment.html`
    - Access: Authenticated users (shipper)

11. `/addfile`

    - Description: Displays a page for adding a file.
    - Method: GET
    - Template: `addfile.html`
    - Access: Authenticated users (admin)

12. `/viweshipping`

    - Description: Displays all shipments for viewing.
    - Method: GET
    - Template: `allshipments.html`
    - Access: Authenticated users (admin)

13. `/viwewallets/<wallet_code>`

    - Description: Displays wallet details and transactions for a specific shipper.
    - Method: GET
    - Template: `wallet.html`
    - Access: Authenticated users (admin)

14. `/notifications`

    - Description: Displays notifications page.
    - Method: GET
    - Template: `notifications.html`
    - Access: Authenticated users

15. `/extract_barcode`

    - Description: Handles barcode extraction from images.
    - Method: POST
    - Access: Authenticated users

16. `/changstates/<int:barcode>`

    - Description: Changes shipment status based on form data.
    - Method: POST
    - Access: Authenticated users (admin)

17. `/profile`

    - Description: Displays the profile page for the logged-in user.
    - Method: GET
    - Template: `profile.html`
    - Access: Authenticated users (shipper)

18. `/viwewallets`

    - Description: Displays all shippers' wallets and total assets.
    - Method: GET
    - Template: `allw.html`
    - Access: Authenticated users (admin)

19. `/submitS`

    - Description: Handles submission of shipper registration form.
    - Method: POST
    - Access: Authenticated users (admin)

20. `/submit_delivery`

    - Description: Handles submission of delivery registration form.
    - Method: POST
    - Access: Authenticated users (admin)

21. `/adds1`

    - Description: Handles submission of shipment creation form by shippers.
    - Method: POST
    - Access: Authenticated users (shipper)

22. `/update_profile/<int:admin_id>`

    - Description: Updates admin profile information.
    - Method: GET, POST
    - Template: `setting.html`
    - Access: Authenticated users (admin)

23. `/dprice/<int:sid>`

    - Description: Displays and manages price settings for a specific shipper.
    - Method: GET
    - Template: `dprice.html`
    - Access: Authenticated users (admin)

24. `/saveprice/<int:sid>`

    - Description: Saves shipping price settings for a specific shipper.
    - Method: POST
    - Access: Authenticated users (admin)

25. `/setting`

    - Description: Displays settings page for the logged-in user.
    - Method: GET
    - Template: `setting.html`
    - Access: Authenticated users (admin, shipper, delivery)

26. `/`

    - Description: Displays the homepage.
    - Method: GET
    - Template: `index.html`
    - Access: Public
## Contributing

Contributions are welcome! If you find any issues or want to enhance the application, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
