create database Portfolios;

use Portfolios;

-- TODO: add users and the relationships that come with it

create table accounts(
    account_no varchar(255) primary key,
    bank_name varchar(255),
    account_type enum('current', 'savings'),
    amount float
);

create table stocks(
    ticker varchar(10) primary key, -- allow for nyse tickers upto 10 characters
    exchange varchar(255),
    market_cap enum('small', 'medium', 'high'),
    full_name varchar(255),
    quantity bigint,
    amount_invested float,
    account_no varchar(255),
    foreign key (account_no) references accounts(account_no)
);

create table mutual_funds(
    name varchar(255) ,
    mf_id int primary key,
    net_asset_value float,
    quantity bigint,
    amount_invested float,
    account_no varchar(255),
    foreign key (account_no) references accounts(account_no)
);

create table value(
    day date primary key,
    value float,
    inflow float,
    outflow float
);
