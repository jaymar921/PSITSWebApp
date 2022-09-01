create database psitswebapp;

use psitswebapp;

create table announcements(
    id int not null auto_increment,
    title varchar(100) not null,
    date_published date not null,
    content varchar(9999) not null,
    primary key(id)
) engine = innodb;

create table accounts(
    idno int(11) not null primary key,
    rfid varchar(100),
    firstname varchar(100) not null,
    lastname varchar(100) not null,
    course varchar(5) not null,
    year int(1) not null,
    email varchar(100) not null,
    password varchar(32) not null
) engine = innodb;

create table events (
    uid int primary key,
    title varchar(50) not null,
    date_held date,
    info varchar(100) not null,
    required_payment varchar(3) not null,
    item_to_be_paid varchar(30),
    amount decimal(10,2),
    open varchar(5)
) engine = innodb;

create table order_account(
    uid int not null auto_increment primary key,
	event_uid int not null,
	account_id int not null,
	account_status varchar(50) not null,
	quantity int not null,
	payment_reference varchar(50) not null,
	foreign key(event_uid) references events(uid) on delete cascade on update cascade,
	foreign key(account_id) references accounts(idno) on delete cascade on update cascade
) engine = innodb;

create table logging(
    uid int not null auto_increment primary key,
    date datetime not null,
    message varchar(150) not null
) engine = innodb;

