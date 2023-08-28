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

## Contributing

Contributions are welcome! If you find any issues or want to enhance the application, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
