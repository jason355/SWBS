use dbv1;

describe data;
select* from tea_infor;
drop table data;
SHOW FULL FIELDS FROM data;
delete from data where name = "Admin";
select * from data ;

SET SQL_SAFE_UPDATES=1;

create Table tea_infor (
	id int AUTO_INCREMENT primary key,
    lineID varchar(40) NOT NULL,
    name varchar(20) not null,
    office varchar(20) not null,
	isAdmin boolean DEFAULT False,
    verifyStat tinyint default 0
);

use dbv1;


drop table data;

CREATE TABLE data (
    id int AUTO_INCREMENT primary key not null,
    name char(10),
    lineID varchar(45) NOT NULL,
    hash varchar(40) NOT NULL,
    content text,
    is_new tinyint(1) default 1,
    time timestamp default current_timestamp,
    office char(6),
    finish_date char(10),
    des_grade char(3),
    des_class char(1),
    sound int
);


insert into data (name, content, office, des_grade, des_class, finish_date) values ("Admin", "g7", "資訊組", "11", "3", "2024-01-30");
