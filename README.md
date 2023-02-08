# b2-transaction-tracker


<!-- ABOUT THE PROJECT -->
## About The Project


This is a simple tool built on [selenium](https://selenium-python.readthedocs.io/), to scrape api transactions from Backblaze's [b2 cloud-storage](https://www.backblaze.com/b2/cloud-storage.html) reports. Transactions are stored in SQL. 

## Why this exists?

**tl;dr** I was annoyed that Backblaze does not offer the ability to gather your api transactions in an automated way, e.g. through their [b2 cli](https://www.backblaze.com/b2/docs/quick_command_line.html).

 Modern backup solutions can backup your data directly to the cloud using the b2 api. This means that deduplication, snapshots and compression can all be performed in your cloud storage blob directly. However, the number of api transactions is non-trivial for sufficiently large backups and calculating the transaction costs with any amount of granularity i.e day to day or hour to hour is not possible currently. In theory you could expose the api transaction calls in your respective backup client but this is very messy and prone to mistakes.



## Prerequisites

- **YOU MUST DISABLE 2FA** on your account for this tool to work. Do not use this tool if this is unacceptable to you. If there's a better way for this tool to work, I welcome any suggestions.

- Valid credentials to your Backblaze account. The same username/password you use to login to their website.


## Getting Started

1. Clone repo
   ```bash
   git clone https://github.com/oregonpillow/b2-transaction-tracker.git

   cd b2-transaction-tracker
   ```


2. Create docker-network
   ```bash
   docker network create b2
   ```
3. Export your B2 Username / Password to your shell environment
   ```bash
   echo 'export B2_EMAIL="<YOUR EMAIL HERE>"' >> ~/.zshrc

   echo 'export B2_PWD="<YOUR EMAIL HERE>"' >> ~/.zshrc

   # or replace with your respective shell environment. E.g. for bash ~/.bashrc
   ```
4. Start Selenium + SQL containers

  First change the following SQL variables in the docker-compose:

  *  MYSQL_ROOT_PASSWORD
  *  MYSQL_USER
  *  MYSQL_PASSWORD

**m1 users:** change the selenium image from 
  'selenium' to 'seleniarm'

  ```bash
   docker-compose up -d
   ```

5. Build b2-transaction-tracker docker
  ```bash
   docker build -t b2-transaction-tracker .
   ```

6. Run the container

* DB_USER must match MYSQL_USER
* DB_PWD must match MYSQL_PASSWORD

  ```bash
  docker run \
  -e B2_EMAIL \
  -e B2_PWD \
  -e DB_USER=user \
  -e DB_PWD=password \
  --network=b2 \
  --rm b2-transaction-tracker:latest
  ```
  
  The container typically takes about 10 seconds to run.

To schedule automatic collection of api transactions it's recommended to use cron schedule this container.

Example SQL:
![db beaver example](./screenshot.png)



## b2-transaction-tracker Environment Variables

| ENV      | Description | Default |
| ----------- | ----------- | --- |
| B2_EMAIL      | b2 email       | --- |
| B2_PWD   | b2 password        | --- |
| DB_HOST   | name of sql container name        | **b2-db** |
| DB_USER   | sql user, must match MYSQL_USER set in SQL container        | **user** |
| DB_PWD   | sql password, must match MYSQL_PASSWORD set in SQL container        | **password** |
| DB_PORT   | default sql port        | **3306** |
| DB_NAME   | sql database name, must match MYSQL_DATABASE set in SQL container        | **b2** |
| TIMESTAMP   | When set to **TRUE**, SQL date entry includes time as well "2023-01-01 20:30:45" (each entry is unique and kept). When set to **FALSE**, only the date is recorded "2023-02-07 00:00:00", meaning that subsequent runs within same day will overwrite any previous data recorded that day (keeps the latest)       | **TRUE** |
