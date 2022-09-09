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

create table event(
    uid int not null auto_increment primary key,
    title varchar(100) not null,
    date_published date not null,
    information varchar(2999) not null,
    image_file varchar(200) not null
) engine = innodb;

create table merchandise(
    uid int not null auto_increment primary key,
    title varchar(100) not null,
    information varchar(2999) not null,
    price decimal(10,2) not null,
    discount int not null, -- can be changed, in percentage form
    stock int not null
) engine = innodb;

create table orders(
    uid int not null auto_increment primary key,
    account_id int not null,
    FOREIGN KEY (account_id) REFERENCES accounts(idno) on delete cascade on update cascade,
    order_date date not null,
    merch_id int not null,
    FOREIGN KEY (merch_id) REFERENCES merchandise(uid) on delete cascade on update cascade,
    status varchar(20) not null,
    quantity int not null,
    additional_info varchar(200),
    reference varchar(100)
) engine = innodb;

/*
    STATUS -----
    - NONE or UNRESERVED
    - ORDER
    - PAID
    - CLAIMED
*/
create table logging(
    uid int not null auto_increment primary key,
    date datetime not null,
    message varchar(150) not null
) engine = innodb;

create table faculty_personnel(
    uid int not null auto_increment primary key,
    name varchar(100) not null,
    position varchar(100) not null,
    description varchar(2999) not null,
    job varchar(50) not null,
    image_src varchar(100) not null
) engine = innodb;

create table psits_officers(
    uid int not null,
    FOREIGN KEY (uid) REFERENCES accounts(idno) on delete cascade on update cascade,
    position varchar(50) not null,
    birthday date not null,
    image_src varchar(50) not null
) engine = innodb;