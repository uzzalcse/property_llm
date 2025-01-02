# Property LLM Project

A Django CLI application that leverages Gemini 2.0 Flash (experimental) to enhance property listings by automatically rewriting descriptions, generating summaries, and providing ratings and reviews.

## Features

- Automated property description rewriting using Gemini 2.0 Flash
- Summary generation for property listings
- AI-powered property ratings and reviews
- Command-line interface for batch processing
- Docker support for easy deployment

## Project Structure

```
property_llm/
|-- property_llm/                  # Django project folder
|   |-- __init__.py               # Project initialization
|   |-- asgi.py                   # ASGI configuration
|   |-- settings.py               # Project settings
|   |-- urls.py                   # URL configuration
|   |-- wsgi.py                   # WSGI configuration
|
|-- properties/                   # Django app for managing properties
|   |-- management/              # Custom management commands
|   |   |-- commands/
|   |       |-- __init__.py
|   |       |-- rewrite_properties.py
|   |-- migrations/              # Django migrations
|   |   |-- 0001_initial.py      # Initial migration file
|   |   |-- __init__.py
|   |-- __init__.py              # App initialization
|   |-- admin.py                 # Admin configuration
|   |-- apps.py                  # App configuration
|   |-- service.py               # Contains reusable service logic
|   |-- models.py                # Database models
|   |-- tests.py                 # Unit tests
|
|-- Dockerfile                    # Docker configuration
|-- docker-compose.yml            # Docker Compose configuration
|-- .env                         # Environment variables
|-- .gitignore                   # Ignored files for Git
|-- manage.py                    # Django's management script
|-- README.md                    # Project documentation
|-- requirements.txt             # Python dependencies
```

## Prerequisites

- Docker and Docker Compose


## To run this project first you need to go to the following link and `clone` and `run` the project first. Then you have to proceed for this project.
Link: https://github.com/uzzalcse/tripscraper.git

## Installation and Setup

After running the above linked project now follow the steps to build and run this project. 

1. Clone the repository:
```bash
git clone https://github.com/uzzalcse/property_llm.git
cd property_llm
```


3. Build and start the Docker containers:
```bash
docker-compose up --build -d
```

4. Run migrations:
```bash
docker-compose exec property_llm-web-1 python manage.py migrate
```

## Usage

### Rewrite Property Descriptions

Run the management command in the Docker container to process property descriptions:

```bash
docker-compose exec property_llm-web-1 python manage.py rewrite_properties
```

### To see the results
 you have to go to pgadmin of the scrappy project and login with proper credentials. Then see

This command will:
1. Read existing property titles and descriptions
2. Use Gemini 2.0 Flash to generate improved versions
3. Store the updated content in the database
4. Generate and store property summaries
5. Create AI-powered ratings and reviews


### Database Schema

The project uses the following main models:

1. Property (existing table)
   - Title
   - Description
   - Other property-related fields

2. PropertySummary
   - property_id (ForeignKey to Property)
   - summary (TextField)

3. PropertyReview
   - property_id (ForeignKey to Property)
   - rating (DecimalField)
   - review (TextField)

## Environment Variables

Create a `.env` file with the following variables:

```
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=trip_scraper
DB_PORT=5432
DB_HOST=db
SECRET_KEY='django-insecure-nc4($e*vaa^7ftbpg^5y8yz-5a(-n18-*#ln^wpbtw5a0-@e5('
GEMINI_API_KEY='AIzaSyCSwJa3keQN01uythpR7_Dn1etiGBK1znU'
```

Note: The database host should be `db` as defined in the Docker Compose configuration.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.