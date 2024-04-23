-- Create database dbv1;

use dbv1;
drop table tea_infor;

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
alter table data add column group_send char(1);

create Table tea_infor (
	id int AUTO_INCREMENT primary key,
    lineID varchar(45) NOT NULL,
    name varchar(10) not null,
    office varchar(6) not null,
	isAdmin boolean DEFAULT False,
    verifyStat tinyint default 0
);

create Table class_list (
	id int auto_increment primary key,
    classCode varchar(3) not null,
    className varchar(10) not null
);

insert into data (name, content, office, des_grade, des_class, finish_date, sound) values ("Admin", "1", "資訊組", "07", "1", "2024-02-03", 1);
insert into data (name, content, office, des_grade, des_class, finish_date, sound) values ("Admin", "2", "資訊組", "11", "3", "2024-02-03", 1);
insert into data (name, content, office, des_grade, des_class, finish_date, sound) values ("Admin", "3", "資訊組", "11", "3", "2024-04-30", 0);

insert into data (name, lineID, hash,content ,office, des_grade, des_class, finish_date, sound) values ("Admin", "Uaf14190a82dbcf01d7b0e3bfb2e003e2", "c09f6f23f05c8cff77b7db35b8fbb7211ad4b148", "1test https://www.ahs.nccu.edu.tw/home https://chat.openai.com/c/dba4f64a-b8c2-48a9-989d-6996bcf5479b", "資訊組", "11", "3", "2024-03-30",1);

drop table class_list;

insert into class_list (classCode, className) values ("112", "112班");


describe `data`;
select * from tea_infor;
select * from data;
select * from class_list;