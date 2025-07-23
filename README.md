# Daily Sales ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline for processing daily sales data from CSV files and loading it into a PostgreSQL database.

[Test scenario and use case](https://www.notion.so/Escenario-1-ETL-Batch-Reporte-Diario-de-Ventas-2389cb4af73d803ba8b3cef1c7873dad?source=copy_link)

## Features

- **Extract**: Read sales data from CSV files with robust encoding handling
- **Transform**: Clean and standardize data with currency conversion
- **Load**: Store processed data in PostgreSQL database
- **Containerized**: Full Docker setup with PostgreSQL database
- **Logging**: Comprehensive logging throughout the ETL process

## Project Structure

```
daily-sales/
├── app/
│   ├── config/
│   │   ├── db.py              # Database configuration
│   │   └── logger.py          # Logging configuration
│   ├── core/
│   │   └── etl.py             # Main ETL processing logic
│   └── data/
│       └── raw/
│           └── daily_sales.csv # Sample data file
├── tmp/                       # PostgreSQL data volume
├── .env                       # Environment variables
├── .env.sample               # Environment template
├── docker-compose.yml        # Docker services configuration
├── Dockerfile               # Application container
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (if running locally)
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd daily-sales
```

### 2. Environment Setup

Copy the sample environment file and configure if needed:

```bash
cp .env.sample .env
```

The default `.env` configuration:
```
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DB_NAME=salesdb
DB_HOST=db
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker compose up --build

# Run in background
docker compose up -d --build

# Stop services
docker compose down
```

## Running the Application

### Docker Compose (Recommended)

The easiest way to run the entire pipeline:

```bash
docker compose up --build
```

This will:
1. Start PostgreSQL database with health checks
2. Wait for database to be ready
3. Run the ETL pipeline on the sample data
4. Process and load data into the database

### Local Development

If you prefer to run locally:

1. **Start PostgreSQL only:**
   ```bash
   docker compose up db -d
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update environment variables:**
   ```bash
   # Update .env file to use localhost instead of 'db'
   DB_HOST=localhost
   ```

4. **Run the ETL pipeline:**
   ```bash
   python main.py --source ./app/data/raw/daily_sales.csv
   ```

## Data Format

The ETL pipeline expects CSV files with the following structure:

```csv
date;customer_name;product;amount;currency
2024-01-01;John Doe;Product A;100.00;USD
2024-01-02;Jane Smith;Product B;75.50;EUR
```

### Supported Fields:

- `date`: Date in YYYY-MM-DD format
- `customer_name`: Customer name (will be trimmed)
- `product`: Product name
- `amount`: Numeric amount
- `currency`: Currency code (USD, EUR, COP supported)

## Database Schema

The pipeline creates a `sale` table with the following schema:

```sql
CREATE TABLE sale (
    date DATE,
    customer_name VARCHAR,
    product VARCHAR,
    amount DECIMAL,
    currency VARCHAR,
    file VARCHAR  -- Source file path
);
```

## Currency Conversion

The pipeline automatically converts all amounts to USD using these rates:
- USD: 1.0 (base)
- EUR: 1.2
- COP: 0.00025

## Logging

The application provides detailed logging:

- **INFO**: Process status and progress
- **ERROR**: Error details with full stack traces

Logs are output to the console and can be viewed with:

```bash
docker compose logs app
```

## Troubleshooting

### Common Issues

1. **Database Connection Refused**
   - Ensure PostgreSQL is fully started
   - Check that `DB_HOST=db` in `.env` when using Docker Compose
   - Verify health checks are passing: `docker compose ps`

2. **UTF-8 Encoding Errors**
   - The pipeline handles multiple encodings automatically
   - Supported: utf-8, latin-1, cp1252, iso-8859-1

3. **Port Already in Use**
   ```bash
   # Stop any existing PostgreSQL services
   docker compose down
   # Or change the port in docker-compose.yml
   ```

### Useful Commands

```bash
# View logs
docker compose logs app
docker compose logs db

# Access database
docker exec -it daily-sales-db-1 psql -U postgres -d salesdb

# Rebuild containers
docker compose build --no-cache

# Remove all data
docker compose down -v
rm -rf tmp/*
```

## Development

### Adding New Data Sources

1. Place CSV files in `app/data/raw/`
2. Run with custom source:
   ```bash
   python main.py --source ./app/data/raw/your_file.csv
   ```

### Modifying Transformations

Edit `app/core/etl.py` in the `transform()` method to add custom data transformations.

### Database Queries

Connect to the database and run queries:

```bash
docker exec -it daily-sales-db-1 psql -U postgres -d salesdb
```

```sql
-- View all sales
SELECT * FROM sale;

-- Sales by date
SELECT date, SUM(amount) as total FROM sale GROUP BY date ORDER BY date;

-- Top customers
SELECT customer_name, SUM(amount) as total FROM sale GROUP BY customer_name ORDER BY total DESC;
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
