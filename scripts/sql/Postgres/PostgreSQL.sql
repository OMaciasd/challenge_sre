CREATE TABLE APPX_DEPARTMENT (
	ID SERIAL PRIMARY KEY,
	DEPARTMENT_NAME VARCHAR(100),
	DEPARTMENT_CITY VARCHAR(100)
);

CREATE TABLE APPX_EMPLOYEE (
	ID SERIAL PRIMARY KEY,
	FIRSTNAME VARCHAR(100),
	LASTNAME VARCHAR(100),
	DEPARTMENT_ID INTEGER REFERENCES APPX_DEPARTMENT(ID),
	SALARY DECIMAL(10, 2),
	EDUCATIONLEVEL_ID INTEGER
);

CREATE TABLE APPX_EDUCATIONLEVEL (
	ID SERIAL PRIMARY KEY,
	DESCRIPTION VARCHAR(100)
);

INSERT INTO APPX_DEPARTMENT (
	DEPARTMENT_NAME,
	DEPARTMENT_CITY
) VALUES (
	'HR',
	'New York'
),
(
	'IT',
	'San Francisco'
),
(
	'Finance',
	'Chicago'
);

INSERT INTO APPX_EMPLOYEE (
	FIRSTNAME,
	LASTNAME,
	DEPARTMENT_ID,
	SALARY,
	EDUCATIONLEVEL_ID
) VALUES (
	'John',
	'Doe',
	1,
	50000,
	1
),
(
	'Jane',
	'Smith',
	2,
	75000,
	2
),
(
	'Emily',
	'Jones',
	2,
	60000,
	3
),
(
	'Michael',
	'Brown',
	3,
	80000,
	1
);

INSERT INTO APPX_EDUCATIONLEVEL (
	DESCRIPTION
) VALUES (
	'High School'
),
(
	'Bachelor\'S DEGREE'),
('MASTER\'s Degree'
);

SELECT
	D.DEPARTMENT_NAME,
	COUNT(E.ID)       AS EMPLOYEE_COUNT,
	SUM(E.SALARY)     AS TOTAL_SALARY
FROM
	APPX_EMPLOYEE   E
	JOIN APPX_DEPARTMENT D
	ON E.DEPARTMENT_ID = D.ID
GROUP BY
	D.DEPARTMENT_NAME
ORDER BY
	TOTAL_SALARY ASC;
