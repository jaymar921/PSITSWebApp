create table events (
    uid int primary key,
    title varchar(50) not null,
    date_held date,
    info varchar(100) not null,
    required_payment varchar(3) not null,
    item_to_be_paid varchar(30),
    amount decimal(10,2)
) engine = innodb;

create table event_accounts(
	uid int not null,
	account_id int not null,
	account_status varchar(50) not null,
	payment_reference varchar(50) not null,
	foreign key(uid) references events(uid),
	foreign key(account_id) references accounts(idno)
) engine = innodb;