
# Django REST Framework Boilerplate

A boilerplate project for building RESTful APIs using Django REST Framework, with configurations for development and production, email settings, CORS headers, and testing using pytest.

## Features

- **Django REST Framework**: Quickly build RESTful APIs.
- **Two Settings**: Easily switch between development and production settings.
- **Email Configuration**: Pre-configured email settings for sending notifications.
- **CORS Headers**: Support for Cross-Origin Resource Sharing.
- **Testing with Pytest**: Built-in support for testing your application.

## Prerequisites

- Python 3.8 or higher
- pip
- Virtual Environment (recommended)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/yusof-shkn/django-restframework-boilerplate.git
cd django-restframework-boilerplate
```

### Set Up a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

- On Windows:

  ```bash
  .venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source .venv/bin/activate
  ```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

#### Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```
DJANGO_SECRET_KEY=your_secret_key
```

#### Development Settings

The development settings are located in `config/settings/dev.py`. You can customize any settings as needed.

#### Production Settings

The production settings are located in `config/settings/prod.py`. Make sure to update the `ALLOWED_HOSTS` and any other necessary configurations.

### CORS Configuration

CORS is configured in the `config/settings/base.py`. You can adjust the `CORS_ALLOWED_ORIGINS` setting to specify which domains can access your API.

### Running Migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

### Running the Development Server

Start the development server:

```bash
python manage.py runserver
```

### Running Tests

To run tests using pytest, use the following command:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests for any improvements!

---

Feel free to modify this template to fit the specific details and structure of your project!
