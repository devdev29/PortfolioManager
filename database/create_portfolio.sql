create database Portfolios;

use Portfolios;

create table stocks(
    ticker varchar(5) primary,
    market_cap int,
    full_name varchar(255),
    quantity bigint,
    bought_price float
)

create table cash(
    account_no varchar(255) primary,
    bank_name varchar(255),
    account_type varchar(255),
    amount float
)

create table mutual_funds(
    name varchar(255),
    amount float,
    net_asset_value float,
    total_return float,
    date_invested date
)

create table value(
    day date primary,
    value float
)
