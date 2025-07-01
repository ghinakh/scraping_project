# Project Overview

This project focuses on building a web scraping pipeline to extract institutional / affiliation data from the SINTA (Science and Technology Index) website. The scraping process is automated using Apache Airflow to ensure regular, incremental data collection without manual intervention. The scraped data includes institutional names, id, code, locations, number of departments, number of authors, and SINTA scores, which can be used for competitive analysis, benchmarking, and academic research tracking.

# Objectives

- Develop a reliable web scraper to collect institutional data from the SINTA website.
- Automate the scraping process using Airflow to run at scheduled intervals.
- Provide structured CSV outputs for further analysis and reporting.

# Tools & Technologies

- **Python:** Core programming language for scraping and automation.
- **BeautifulSoup:** HTML parsing and data extraction.
- **Requests:** HTTP request handling with retry mechanism.
- **Apache Airflow:** Workflow scheduling and orchestration.
- **Pandas:** Data processing and CSV export.
- **Airflow Variables:** For dynamic batch progress tracking.

# Data Source
- https://sinta.kemdikbud.go.id/affiliations/

# Schedule
- Every one hour

# Airflow Variable
- sinta_scrapper_current_page