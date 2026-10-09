CREATE SCHEMA IF NOT EXISTS hospital;
USE hospital;
CREATE TABLE MedicalStaff (
    idNumber INT (10) NOT NULL UNIQUE,
    fName VARCHAR(10),
    minit VARCHAR(10),
    lName VARCHAR(10),
    gender VARCHAR(10),
    specialization VARCHAR(20),
    super_id INT (10),
    CONSTRAINT MedicalStaff_PK PRIMARY KEY (idNumber),
    CONSTRAINT MedicalStaff_FK1 FOREIGN KEY (super_id)
        REFERENCES MedicalStaff (idNumber)
);

CREATE TABLE Patient (
    idNumber INT (10) UNIQUE,
    fName VARCHAR(10),
    minit VARCHAR(10),
    lName VARCHAR(20),
    birthDate DATE,
    gender VARCHAR(10),
    fileNumber INT(6) NOT NULL,
    CONSTRAINT patient_PK PRIMARY KEY (fileNumber)
);

CREATE TABLE Reception (
    employeeId INT(10) NOT NULL, 
    fName VARCHAR(10),
    minit VARCHAR(10),
    lName VARCHAR(20),
    gender VARCHAR(6),
    CONSTRAINT Reception_PK PRIMARY KEY (employeeId)
);

CREATE TABLE Medicine(
idNumber INT(10) NOT NULL ,
medicineName VARCHAR(20),
price INT(5) ,
CONSTRAINT Medicine_PK PRIMARY KEY (idNumber)
);


CREATE TABLE Visitor(
pFileNumber INT (10) NOT NULL ,
fName VARCHAR (10) NOT NULL ,
lName VARCHAR(20),
 gender VARCHAR (10) ,
 age INT (2) CHECK (age > 18),
 relationsship VARCHAR (10),
 CONSTRAINT Visitor_PK PRIMARY KEY (pFileNumber, fName),
 CONSTRAINT Visitor_FK1 FOREIGN KEY (pFileNumber) REFERENCES Patient(fileNumber) 
 );
 
  CREATE TABLE Takes(
 pFileNumber INT (6),
  MedicineID  INT (10),
  CONSTRAINT Takes_PK PRIMARY KEY (pFileNumber, MedicineID),
  CONSTRAINT Takes_FK1 FOREIGN KEY (pFileNumber) REFERENCES Patient(fileNumber),
  CONSTRAINT Takes_FK2 FOREIGN KEY (MedicineID) REFERENCES Medicine(idNumber)
 );
 
  CREATE TABLE Manages(
 medicalID INT (10) NOT NULL,
 MedicineID INT (10) NOT NULL,
 CONSTRAINT Manages_PK PRIMARY KEY (medicalID, MedicineID),
  CONSTRAINT Manages_FK1 FOREIGN KEY (medicalID) REFERENCES MedicalStaff(idNumber),
  CONSTRAINT Manages_FK2 FOREIGN KEY (MedicineID) REFERENCES Medicine(idNumber)
  );
  
    CREATE TABLE Visit (
    pFileNumber INT(6) NOT NULL,
    employeeId INT(10) NOT NULL,
    medicalID INT(10) NOT NULL,
    price INT(8),
    CONSTRAINT Visit_PK PRIMARY KEY (pFileNumber , employeeId , medicalID),
    CONSTRAINT Visit_FK1 FOREIGN KEY (pFileNumber) REFERENCES Patient (fileNumber),
    CONSTRAINT Visit_FK2 FOREIGN KEY (medicalID) REFERENCES MedicalStaff (idNumber),
    CONSTRAINT Visit_FK3 FOREIGN KEY (employeeId) REFERENCES Reception (employeeId)
);

 CREATE TABLE PatientLoc(
   pFileNumber INT (6) NOT NULL,
   location VARCHAR (40) NOT NULL,
   CONSTRAINT PatientLoc_PK PRIMARY KEY (pFileNumber , location),
   CONSTRAINT PatientLoc_FK1 FOREIGN KEY (pFileNumber) REFERENCES Patient(fileNumber)
);

  CREATE TABLE PatientPhone(
   pFileNumber INT (6) NOT NULL,
   phoneNumber INT (10) NOT NULL,
   CONSTRAINT PatientPhone_PK PRIMARY KEY (pFileNumber ,phoneNumber),
   CONSTRAINT PatientPhone_FK1 FOREIGN KEY (pFileNumber) REFERENCES Patient(fileNumber)
);

 INSERT INTO hospital.MedicalStaff
 VALUE (1120917163,'Assayil','Asaad','Hawsawi','female','dentalconsultant', null);
INSERT INTO hospital.MedicalStaff
 VALUE (1007180207,'Ahmad','Massad','Alharthi','male','ophthalmologist',1120917163 );
 INSERT INTO hospital.MedicalStaff
 VALUE (1005695598,'Mohammed','Yahia','Albishri','male','internaldoctor',1120917163 );
  INSERT INTO hospital.MedicalStaff
 VALUE (1120344163,'Anas','Jamal','Saggaf','male','surgrydoctor',1120917163 );
 INSERT INTO hospital.MedicalStaff
 VALUE (1005695222,'Asmaa','Walid','Alats','female','pediatrician',1120917163 );
 
  INSERT INTO hospital.Patient
 VALUE (1007180277,'ibrahem','Abdullah','Alzahrani','1991-12-5','male',112300 );
 INSERT INTO hospital.Patient
 VALUE (1120990361,'Najwan','Suleiman','Orif',"2004-03-04",'female', 115399);
 INSERT INTO hospital.Patient
 VALUE (1005698872,'Ghozlan','Akram','Busha','2000-11-8','female',112367 );
  INSERT INTO hospital.Patient 
 VALUE (1120919876,'Sami','Asaad','Saggaf','1995-5-23','male',120100 );
 INSERT INTO hospital.Patient
 VALUE (1115695598,'Zahraa','Ali','Alshahri','1985-3-7','female',100364 );
 
  INSERT INTO hospital.Reception
 VALUE (1197180203,'Ali','Saud','Theban','male');
 INSERT INTO hospital.Reception
 VALUE (1067760207,'Reem','Mohammed','Alharbi','female');
 INSERT INTO hospital.Reception
 VALUE (1143656457,'Amal','Yousef','Alharthi','female');
 INSERT INTO hospital.Reception
 VALUE (1144859027,'Lama','Abdulaziz','Alotaibi','female');
 INSERT INTO hospital.Reception
 VALUE (1159875650,'Batal','Omar','Alqahtani','male');
 
  INSERT INTO hospital.medicine
 VALUE (3330544,'Adolsinus',25);
 INSERT INTO hospital.medicine
 VALUE (4320067,'After-meals',59);
 INSERT INTO hospital.medicine
 VALUE (507465,'Buscopan',30);
 INSERT INTO hospital.medicine
 VALUE (1276500,'Cidamex',100);
 INSERT INTO hospital.medicine
 VALUE (5566321,'Bepra',79);
 
  INSERT INTO hospital.Visitor
 VALUE (112300,'Maryam','Alharbi','female',25,'Wife');
 INSERT INTO hospital.Visitor
 VALUE (115399,'Suleiman','Orif','male',47,'Fhather');
 INSERT INTO hospital.Visitor
 VALUE (112367,'Samara','Busha','female',23,'Sister');
 INSERT INTO hospital.Visitor
 VALUE (120100,'Saad','Saggaf','male',28,'Brother');
 INSERT INTO hospital.Visitor
 VALUE (100364,'Rawan','Alharbi','female',44,'Mother');
 
  INSERT INTO hospital.takes
 VALUE (112300,3330544);
  INSERT INTO hospital.takes
 VALUE (115399,5566321);
   INSERT INTO hospital.takes
 VALUE (112367,4320067);
   INSERT INTO hospital.takes
 VALUE (112367,1276500);
   INSERT INTO hospital.takes
 VALUE (100364,507465);
 
  INSERT INTO hospital.Manages
 VALUE (1120917163,3330544);
  INSERT INTO hospital.Manages
 VALUE (1120917163,4320067);
   INSERT INTO hospital.Manages
 VALUE (1120917163,507465);
   INSERT INTO hospital.Manages
 VALUE (1005695598,1276500);
   INSERT INTO hospital.Manages
 VALUE (1005695598,5566321);
 
 INSERT INTO hospital.visit
 VALUE (112300,1197180203,1007180207,500);
  INSERT INTO hospital.visit
 VALUE (115399,1067760207,1120917163,200);
   INSERT INTO hospital.visit
 VALUE (112367,1143656457,1005695598,750);
   INSERT INTO hospital.visit
 VALUE (120100,1144859027,1120917163,150);
   INSERT INTO hospital.visit
 VALUE (100364,1159875650,1005695598,300);
 
INSERT INTO hospital.patientloc
 VALUE (112300,'Alaziziyah ');
  INSERT INTO hospital.patientloc
 VALUE (112300,'Alawali ');
  INSERT INTO hospital.patientloc
 VALUE (115399,'Alshawqiyya');
   INSERT INTO hospital.patientloc
 VALUE (112367,'Alrashidiya ');
   INSERT INTO hospital.patientloc
 VALUE (120100,'Alzahir ');
   INSERT INTO hospital.patientloc
 VALUE (100364,'Altanaim ');
 
  INSERT INTO hospital.patientphone
 VALUE (112300,0552888163);
  INSERT INTO hospital.patientphone
 VALUE (115399,0507343755);
   INSERT INTO hospital.patientphone
 VALUE (112367,0566972247);
   INSERT INTO hospital.patientphone
 VALUE (120100,0502772995);
   INSERT INTO hospital.patientphone
 VALUE (100364,0558991226);
  INSERT INTO hospital.patientphone
 VALUE (100364,0555054263);
 
DELETE FROM hospital.patientphone
WHERE phoneNumber=0502772995 ;
 
 DELETE FROM hospital.visit
 WHERE pFileNumber =120100;
 
UPDATE hospital.MedicalStaff
SET specialization = 'generalSurgeon' 
WHERE specialization = 'ophthalmologist' ;

UPDATE hospital.Medicine
SET price = price*2 ;

 SELECT *
 FROM hospital.medicalstaff
 WHERE specialization='generalSurgeon';
 
SELECT *
FROM hospital.patient
WHERE fileNumber IN ( 
SELECT PfileNumber 
FROM hospital.visit
WHERE price BETWEEN 100 AND 500 );

SELECT *
FROM hospital.Patient
WHERE gender = 'female'
ORDER BY fName ;

SELECT COUNT(fName) AS countOfVisito, age AS VisitorAge
FROM hospital.Visitor
GROUP BY age
HAVING age >=25
ORDER BY age ASC; 

SELECT *
FROM hospital.Reception
ORDER BY fName ASC;

SELECT *
FROM hospital.Medicine
ORDER BY idNumber DESC;

SELECT  CONCAT(v.fName," ",v.lName) AS VisitorName, relationsship, CONCAT(p.fName," ",p.lName) AS patientName,
 fileNumber, p.gender ,birthDate
FROM Patient p INNER JOIN Visitor v ON p.fileNumber = v.pFileNumber
WHERE v.age >= 25;

SELECT CONCAT(p.fName," ",p.lName) AS patientName,
 fileNumber, location , phoneNumber
FROM Patient p , patientloc pl , patientphone pp
WHERE p.fileNumber = pl.pFileNumber AND p.fileNumber = pp.pFileNumber;

SELECT COUNT(phoneNumber) AS countOfphonNumber, pFileNumber
FROM hospital.patientphone
GROUP BY pFileNumber;

SELECT * 
FROM Patient 
WHERE fileNumber IN ( SELECT pFileNumber
FROM Visit 
WHERE medicalID IN ( SELECT idNumber 
FROM hospital.medicalstaff 
WHERE fName = 'Mohammed' ));


                        

 
 
 
 