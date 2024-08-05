create database Portfolios;

use Portfolios;

create table stocks(
    ticker varchar(10) primary, -- allow for bse tickers upto 10 characters
    exchange: varchar(255),
    market_cap int,
    full_name varchar(255),
    quantity bigint,
    amount_invested float,
    foreign key (account_no) references cash(account_no)
)

create table accounts(
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

create table values(
    day date primary,
    value float,
    inflow float,
    outflow float
)
