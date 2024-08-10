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
    ticker varchar(10) primary key, -- allow for bse tickers upto 10 characters
    exchange varchar(255),
    market_cap enum('small', 'medium', 'high'),
    full_name varchar(255),
    quantity bigint,
    amount_invested float,
    account_no varchar(255),
    foreign key (account_no) references accounts(account_no)
);

create table mutual_funds(
    name varchar(255) primary key,
    amount float,
    net_asset_value float,
    total_return float,
    date_invested date
);

create table value(
    day date primary key,
    value float,
    inflow float,
    outflow float
);

create table transactions(
    id uuid primary key default uuid_generate_v4(),
    day date,
    price float,
    quantity bigint,
    amount float
)

insert into accounts values('aaa', 'Zerodha', 'demat', 200000);
insert into accounts values('bbb', 'growww', 'demat', 100000);

insert into stocks values('AAPL', 'NASDAQ', 'large', 'Apple Inc', 100, 20700, 'aaa');
insert into stocks values('NVDA', 'NASDAQ', 'large', 'NVIDIA Corp', 100, 10425, 'bbb');
insert into stocks values('MSFT', 'NASDAQ', 'large', 'Microsoft Corp', 100, 40000, 'bbb');
insert into stocks values('UL', 'NASDAQ', 'large', 'Teradata Corp', 100, 2505, 'bbb');
insert into stocks values('WMT', 'NYSE', 'large', 'Walmart Inc', 100, 6700, 'aaa');
