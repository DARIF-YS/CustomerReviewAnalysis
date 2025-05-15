# 📊 Data Warehouse Project
## Analyzing Customer Reviews of Bank Agencies in Morocco using a Modern Data Stack

[screen-capture.webm](https://github.com/user-attachments/assets/0a41d414-4bd6-44ea-992b-8df586a69d2e)

## 🎬 Project Introduction

## 🎯 Objective
The goal of this project is to **collect**, **process**, and **analyze** Google Maps reviews of bank agencies in Morocco to extract actionable insights through **sentiment analysis**, **topic modeling**, and other key analytical techniques.

We built a **fully operational data pipeline** using modern tools to ensure efficient **data extraction**, **transformation**, **storage**, and **visualization**.

## 🗺️ Project Scope

### 🔹 Use Case Description
Banks in Morocco receive thousands of customer reviews on Google Maps. These reviews contain valuable, unstructured data about customer satisfaction, service quality, and operational issues.  
The project aims to **centralize**, **clean**, and **analyze** this data to drive meaningful insights.

### 📈 Expected Insights
- **Sentiment Analysis:** Track customer satisfaction trends over time.
- **Topic Modeling:** Identify common complaints and praise points.
- **Branch Performance:** Rank branches based on customer feedback.
- **Customer Experience Metrics:** Highlight recurring issues and success factors.

## 🛠️ Tech Stack

| Stage              | Technology                                  |
|--------------------|---------------------------------------------|
| Data Collection    | Python, Google Maps API, BeautifulSoup/Scrapy |
| Scheduling         | Apache Airflow                              |
| Data Storage       | PostgreSQL (Data Warehouse)                 |
| Transformation     | DBT (Data Build Tool)                       |
| Analysis & BI      | Looker Studio (Google Data Studio)          |
| Version Control    | GitHub                                      |

## 🚀 Project Roadmap

### ✅ Phase 1: Data Collection
- Extract reviews using **Google Maps API** or **Web Scraping**.
- Fields collected: `Bank Name`, `Branch Name`, `Location`, `Review Text`, `Rating`, `Review Date`.
- Store raw data in **JSON/CSV** and push to a **PostgreSQL staging table**.
- Automate collection with an **Apache Airflow DAG**.

### ✅ Phase 2: Data Cleaning & Transformation
- **Clean data** using DBT and SQL: remove duplicates, normalize text, handle missing values.
- **Enrich data**: 
  - Detect language.
  - Perform **Sentiment Analysis** (Positive, Negative, Neutral).
  - Extract common topics using **NLP** (LDA).

### ✅ Phase 3: Data Modeling (Star Schema)
- Design a **Data Mart** with a **Star Schema**:
  - **Fact Table:** `fact_reviews`
  - **Dimension Tables:** `dim_bank`, `dim_branch`, `dim_location`, `dim_sentiment`
- Implement transformations with **DBT** and automate with **Airflow**.

### ✅ Phase 4: Data Analytics & Reporting
- Build interactive dashboards in **Looker Studio**:
  - Sentiment trends.
  - Top topics (positive and negative).
  - Branch performance rankings.
  - Customer experience KPIs.

### ✅ Phase 5: Deployment & Automation
- Automate the full pipeline with **Airflow** (daily/weekly updates).
- Implement monitoring and alerts for failures.

## 🗓️ Summary of Project Timeline

| Week | Focus Area                    | Key Deliverables |
|------|--------------------------------|------------------|
| 1    | Data Collection (Scraping)     | Google Maps API/Scraping, Airflow DAG, Raw Data in PostgreSQL |
| 2    | Data Cleaning & Transformation | DBT models, Sentiment Analysis, Airflow Update |
| 3    | Data Modeling (Star Schema)    | Fact & Dimension Tables, SQL Scripts, Data Loading |
| 4    | Analytics & BI Dashboards      | Looker Studio Dashboards, Topic Modeling |
| 5    | Final Report & Presentation    | Documentation, GitHub Repository, Project Presentation |

## 🤝 Contribution

Feel free to fork this repository and open pull requests if you'd like to contribute or improve the project!

## 📫 Contact

For any questions, please contact me via [GitHub Issues](https://github.com/DARIF-YS) or reach out to me on LinkedIn.
