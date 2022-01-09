drop database health_insurance_company;
create database health_insurance_company;
use health_insurance_company;
CREATE table Customer (
	Cust_id	 VARCHAR(50) NOT NULL ,
	fName 	VARCHAR(50) NOT NULL,
	lName 	VARCHAR(50) NOT NULL,
	Money 	numeric(12,2) check (Money > 0),
	visa_card varchar(50) ,
	Phone 	VARCHAR(20) ,
	Gender 	VARCHAR(20)  ,
	date_of_birth varchar(20) ,
  Plan_id	 varchar(50) ,
	PRIMARY KEY (Cust_id)

    );
insert into  Customer values('1','jony' ,'mark' ,'100000000.00' ,'123456789' ,'01026564923' , 'male','10-10-2010' ,'1'); 
insert into  Customer values('2','michal' ,'mena' ,'200000000.00' ,'987654321' ,'0113595456' , 'male','5-5-1998' ,'2');
insert into  Customer values('3','ali' ,'mohamed' ,'300000000.00' ,'147852369' ,'01236589454' , 'male','3-2-2000' ,'3');

create table Dependents(
	Cust_id	 VARCHAR(50), 
	Dept_id 	varchar(50),
	D_name 	varchar(50),
	date_of_birth varchar(50),
	Gender 	varchar(50),
	Relationship varchar(50),
	Plan_id	 varchar(50) ,
	primary key (Cust_id, D_name, Dept_id,Gender, Relationship,date_of_birth),
	CONSTRAINT fk_Dependents_Customer	 foreign key (Cust_id ) references Customer  (Cust_id) on update cascade
	
	);
insert into Dependents values('1','12' ,'ali' ,'3-2-2022','male','son','4');
insert into Dependents values('2','14' ,'abanod' ,'4-2-2010','male','son','5');
insert into Dependents values('3','13' ,'mohamed' ,'6-2-2023','male','son','6');

CREATE TABLE Plan (
  Plan_id	 varchar(50) primary key,
  Type_plan 	varchar(50),
  expire_date	 varchar(50),
  purchase_cust_id VARCHAR(50),
  CONSTRAINT fk_Plan_Customer foreign key (purchase_cust_id) references Customer (Cust_id) on update cascade
);
create index Type_plan_index on Plan(Type_plan);
insert into Plan values('1' ,'Basic','20-20-2029','1'); 
insert into Plan values('2' ,'Premium','20-20-2029','2'); 
insert into Plan values('3','Golden','20-20-2029','3'); 
insert into Plan values('4' ,'Premium','20-20-2029','1');
insert into Plan values('5' ,'Golden','20-20-2029','2');
insert into Plan values('6' ,'Basic','20-20-2029','3');

Alter table Customer add CONSTRAINT fk_Customer_PLan	 foreign key (Plan_id ) references Plan  (Plan_id) on update cascade;
Alter table Dependents add CONSTRAINT fk_Dependents_PLan	 foreign key (Plan_id ) references Plan  (Plan_id) on update cascade;


CREATE TABLE sub_Plan (
  Other_Plan_details varchar(250),
  Type_plan 	varchar(50),
  Price 	numeric(12,2) check (Price > 0),
  primary key(Other_Plan_details,Type_plan,Price),
  CONSTRAINT fk_Plan_plan	 foreign key (Type_plan) references Plan (Type_plan) on update cascade
);
insert into sub_Plan values('Unlimited access','Golden','1800.00'); 
insert into sub_Plan values('Only 80% of Hospitals are accessable' ,'Premium','800.00');
insert into sub_Plan values('Only 40% of Hospitals are accessable' ,'Basic','400.00');
CREATE TABLE  Hospital (
  hospital_id 	INT NOT NULL,
  hospital_name VARCHAR(50) NULL,
  Phone VARCHAR(50) NULL,
  Location VARCHAR(100) NULL,
  Time_of_work VARCHAR(50) NULL,
  specialization VARCHAR(50) NULL,
  details VARCHAR(250) NULL,
  PRIMARY KEY (hospital_id)
  );
insert into  Hospital values  (73354597, 'DEBORAH HEART AND LUNG CENTER', '01103217789 ', '200 TRENTON ROAD','6am to 10pm','SPECIAL','DEBORAH HEART AND LUNG CENTER is a SPECIALhospital in 200 TRENTON ROAD website: http://www.deborah.org');
insert into Hospital   values(89255485, 'CAPE REGIONAL MEDICAL CENTER', '01103217792','2 STONE HARBOR BOULEVARD', '24h','GENERAL ACUTE CARE','CAPE REGIONAL MEDICAL CENTERi is a GENERAL ACUTE CARE in 2 STONE HARBOR BOULEVARD website: http://www.caperegional.com');
insert into Hospital   values(61804435, 'BRISTOL MYERS SQUIBB CHILDRENS HOSPITAL', '0952285355','1 ROBERT WOOD JOHNSON PLACE','24h','CHILDREN','BRISTOL MYERS SQUIBB CHILDRENS HOSPITAL is a CHILDREN in 1 ROBERT WOOD JOHNSON PLACE website:http://www.bmsch.org/');
insert into Hospital   values(67184582, 'NORTHBROOK BEHAVIORAL HEALTH HOSPITAL', '20952277194','20 NORTH WOODBURY TURNERSVILLE ROAD','9am to 9pm','PSYCHIATRIC','	CAMDEN COUNTY HEALTH SERVICES CENTER is PSYCHIATRIC hospital in 20 NORTH WOODBURY TURNERSVILLE ROAD	website: http://www.cchsc.com');
insert into Hospital   values(32432583, 'NEW JERSEY STATE PRISON HOSPITAL','20952359394','425 WOODBURY TURNERSVILLE ROAD','9am to 9pm','PSYCHIATRIC','NORTHBROOK BEHAVIORAL HEALTH HOSPITAL is a PSYCHIATRIC hospital in 425 WOODBURY TURNERSVILLE ROAD website:http://www.northbrookbhh.com/');

  CREATE TABLE enroll(
  hospital_id INT,
  Type_plan varchar(50),
  PRIMARY KEY (hospital_id, Type_plan),
  CONSTRAINT fk_Hospital_has_Plan_Hospi FOREIGN KEY (hospital_id)REFERENCES Hospital (hospital_id)on update cascade,
  CONSTRAINT fk_Hospital_has_Plan_Pla foreign key (Type_plan ) references Plan (Type_plan)on update cascade
);
insert into enroll values(73354597,'Basic');
insert into enroll values(73354597,'Golden');
insert into enroll values(73354597,'Premium');
insert into enroll values(89255485, 'Basic');
insert into enroll values(89255485, 'Premium');
insert into enroll values(89255485, 'Golden');
insert into enroll values(61804435, 'Premium');
insert into enroll values(61804435, 'Golden');
insert into enroll values(67184582, 'Premium');
insert into enroll values(67184582, 'Golden');
insert into enroll values(32432583, 'Golden');

CREATE TABLE  examine(
hospital_id INT,
Cust_id VARCHAR(50)  ,
primary key(Cust_id,hospital_id),
CONSTRAINT fk_Hospital_Customer	 foreign key (Cust_id  ) references Customer  (Cust_id ),
CONSTRAINT fk_Hospit_Customer	 foreign key (hospital_id ) references Hospital  (hospital_id)
  );
insert into examine values(73354597,'1');
insert into examine values(89255485, '2');
insert into examine values(61804435, '3');

CREATE TABLE  Claims (
	Claim_id 	INT NOT NULL, 
	amount_of_expense numeric(12,2) NOT NULL,
	Other_claim_details varchar(250) null, 
	plan_id  varchar(250),
	status varchar(50),
	Benefitiary_claims varchar(50) not null,
	date_claim varchar(50),
	PRIMARY KEY (Claim_id),
	Cust_id 	VARCHAR(50),
	CONSTRAINT fk_Customr_Claim FOREIGN KEY (Cust_id) REFERENCES Customer (Cust_id)on update cascade,
	CONSTRAINT fk_plan_Claim FOREIGN KEY (plan_id) REFERENCES Plan (plan_id)on update cascade,
	hospital_id INT,
   CONSTRAINT fk_hospital_id_Claim FOREIGN KEY (hospital_id) REFERENCES  Hospital  (hospital_id)on update cascade
    );
 
insert into Claims   values('20661526', 2500.00, 'diabetes','1','New','12','1-1-2001','1',73354597);
insert into Claims   values('15205452', 1500.00,null,'2','Resolved','2','3-5-2006','2',89255485);
insert into Claims   values('95764258', 750.50,null,'3','unsolved','13','3-9-2030','3',61804435);

 


CREATE TABLE  Bill(
	bill_id varchar(50),
	desc_Expenses varchar(250),
	amount_of_expense numeric(12,2) NOT NULL,
	hospital_id INT,
	Cust_id VARCHAR(50) ,
	bill_date varchar(50),
	primary key(bill_id),
	CONSTRAINT fk_bill_hospita	 foreign key (hospital_id ) references Hospital  (hospital_id)on update cascade,
	CONSTRAINT fk_bill_Customer	 foreign key (Cust_id  ) references Customer (Cust_id )on update cascade
  );

insert into Bill   values('23','  ', 2500.00, 73354597,'1','1-1-2001');
insert into Bill   values('122', '  ' ,1500.00,89255485,'2','3-5-2006');
insert into Bill   values('98', '  ',750.50,32432583,'3','3-9-2030');

