create table psits_intercampus_admin(
    idno int primary key,
    firstname varchar(50) not null,
    lastname varchar(50) not null,
    course varchar(10) not null,
    year varchar(5) not null,
    campus varchar(20) not null,
    email varchar(100) not null,
    password varchar(100) not null,
    isadmin varchar(10) not null
) engine = innodb;

create table psits_intercampus_events (
    id int primary key auto_increment,
    event_name varchar(150) not null,
    venue varchar(150) not null,
    attendees int not null,
    host varchar(20) not null,
    registration_price int not null,
    tshirt_price int not null,
    deleted varchar(10) not null
) engine = innodb;

create table psits_intercampus_registry(
    id int primary key auto_increment,
    idno int not null,
    foreign key (idno) references psits_intercampus_admin(idno) on delete cascade on update cascade,
    event_id int not null,
    foreign key (event_id) references psits_intercampus_events(id) on delete cascade on update cascade,
    payment varchar(15) not null,
    shirt_size varchar(15),
    attended varchar(15) not null,
    claimed varchar(15) not null,
    meta_data varchar(200)
) engine = innodb;