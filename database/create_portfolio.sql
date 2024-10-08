create database Portfolios;

use Portfolios;

-- TODO: add users and the relationships that come with it

create type account as enum('current', 'savings');
create type mcap as enum('small', 'medium', 'large');

create table accounts(
    account_no varchar(255) primary key,
    bank_name varchar(255),
    account_type account,
    amount float
);

create table stocks(
    ticker varchar(10) primary key, -- allow for nyse tickers upto 10 characters
    exchange varchar(255),
    market_cap mcap,
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

create table transactions(
    day date,
    ticker varchar(15),
    price float,
    quantity bigint,
    amount float,
    account_no varchar(255),
    id uuid primary key,
    foreign key (account_no) references accounts (account_no)
  );

insert into accounts values('aaa', 'Zerodha', 'demat', 200000);
insert into accounts values('bbb', 'growww', 'demat', 100000);

insert into stocks values('AAPL', 'NASDAQ', 'large', 'Apple Inc', 100, 20700, 'aaa');
insert into stocks values('NVDA', 'NASDAQ', 'large', 'NVIDIA Corp', 100, 10425, 'bbb');
insert into stocks values('MSFT', 'NASDAQ', 'large', 'Microsoft Corp', 100, 40000, 'bbb');
insert into stocks values('UL', 'NASDAQ', 'large', 'Teradata Corp', 100, 2505, 'bbb');
insert into stocks values('WMT', 'NYSE', 'large', 'Walmart Inc', 100, 6700, 'aaa');
