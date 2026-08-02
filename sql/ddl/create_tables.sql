
---------------------------
-- DB - ANALYTICS_HUB     |
---------------------------

-- CREATE DATABASE ANALYTICS_HUB;

-- USE ANALYTICS_HUB;

-- SP_HELP STAGING_USERS

-- DROP TABLE STAGING_USERS

CREATE TABLE STAGING_USERS(
    run_id VARCHAR(50),
    id VARCHAR(50) NULL, 	
    first_name VARCHAR(50),	
    last_name VARCHAR(50),	
    gender VARCHAR(50),	
    email VARCHAR(50) NULL,	
    cpf VARCHAR(50), 
    street VARCHAR(50),	
    number VARCHAR(50),	
    city VARCHAR(50),	
    state VARCHAR(50),	
    country VARCHAR(50),	
    latitude VARCHAR(50),	
    longitude VARCHAR(50),	
    date_of_birth VARCHAR(50) NULL,	
    age VARCHAR(50),	
    registration_date VARCHAR(50),	
    regist_age VARCHAR(50),
    created_at VARCHAR(50),
    validacao VARCHAR(10)
    

) ;



-- DROP TABLE SILVER_USERS

-- SP_HELP SILVER_USERS

/*
SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'SILVER_USERS';
*/

CREATE TABLE SILVER_USERS (
    run_id VARCHAR(50) NOT NULL,
    id VARCHAR(50) PRIMARY KEY NOT NULL, 	
    first_name VARCHAR(50) NOT NULL,	
    last_name VARCHAR(50) NOT NULL,	
    gender VARCHAR(50) NULL,	
    email VARCHAR(50) NOT NULL,
    cpf VARCHAR(50) NOT NULL UNIQUE,	
    street VARCHAR(50) NOT NULL,	
    number INT NOT NULL,	
    city VARCHAR(50) NOT NULL,	
    state VARCHAR(50) NOT NULL,	
    country VARCHAR(50) NOT NULL,	
    latitude DECIMAL(9,4) NULL,	
    longitude DECIMAL(9,4) NULL,	
    date_of_birth DATE NOT NULL,	
    age INT NOT NULL,	
    registration_date DATE NOT NULL,	
    regist_age INT NOT NULL,
    created_at DATE  NOT NULL,
    validacao VARCHAR(10) NOT NULL
) ;

-- run_id,id,first_name,last_name,gender,email,cpf,street,number,city,state,country,latitude,longitude,date_of_birth,age,registration_date,regist_age,created_at




-- SELECT * FROM STAGING_USERS;
-- SELECT * FROM SILVER_USERS;
-- SELECT * FROM GOLD_USERS;

-- DROP VIEW GOLD_USERS


                      WITH ORIGEM_FILTRADA AS (
                            SELECT *,
                                -- Cria um ranking para cada ID. O número 1 será o registro mais recente (ou o primeiro encontrado)
                                ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at DESC) as RN
                            FROM STAGING_USERS
                            WHERE RUN_ID = ?
                        ) 
                        MERGE SILVER_USERS AS DESTINO 
                        -- Agora usamos a CTE filtrada como origem, pegando apenas o registro único (RN = 1)
                        USING ( SELECT * FROM ORIGEM_FILTRADA
                                WHERE RN = 1) AS ORIGEM
                        ON (DESTINO.ID = ORIGEM.ID)

                        WHEN NOT MATCHED THEN 
                            INSERT( run_id,
                                    id, 	
                                    first_name,	
                                    last_name,	
                                    gender,	
                                    email,
                                    cpf,	
                                    street,	
                                    number,	
                                    city,	
                                    state,	
                                    country,	
                                    latitude,	
                                    longitude,	
                                    date_of_birth,	
                                    age,	
                                    registration_date,	
                                    regist_age,
                                    created_at  )
                            
                            VALUES( ORIGEM.run_id,
                                    ORIGEM.id, 	
                                    ORIGEM.first_name,	
                                    ORIGEM.last_name,	
                                    ORIGEM.gender,	
                                    ORIGEM.email,
                                    ORIGEM.cpf,	
                                    ORIGEM.street,	
                                    ORIGEM.number,	
                                    ORIGEM.city,	
                                    ORIGEM.state,	
                                    ORIGEM.country,	
                                    ORIGEM.latitude,	
                                    ORIGEM.longitude,	
                                    ORIGEM.date_of_birth,	
                                    ORIGEM.age,	
                                    ORIGEM.registration_date,	
                                    ORIGEM.regist_age,
                                    TRY_CONVERT(DATETIME2(0), ORIGEM.created_at, 120)   )
                                    
;

/*

-- DROP VIEW GOLD_USERS

CREATE VIEW GOLD_USERS AS 

    WITH BASE_USERS_TRATADA AS (

            SELECT 
                ID AS ID_CLIENTE,
                FIRST_NAME AS NOME,
                LAST_NAME AS SOBRENOME,
                FIRST_NAME + ' ' + LAST_NAME AS NOME_COMPLETO,
                CASE 
                    WHEN GENDER = 'female' THEN 'Feminino'
                    WHEN GENDER = 'male' THEN 'Masculino'
                    ELSE 'Nâo informado'
                END As GENERO,
                EMAIL,
                CPF,
                STREET AS RUA,
                NUMBER AS NUMERO_ENDERECO,
                CITY AS CIDADE,
                STATE AS UF,
                COUNTRY AS PAIS,
                STREET + ' ' + cast(NUMBER as varchar) + ' ' + CITY + ' ' + STATE AS ENDERECO_COMPLETO,
                latitude AS LATITUDE,
                longitude AS LONGITUDE,
                DATE_OF_BIRTH AS DATA_NASCIMENTO,
                --DATEDIFF(YEAR, DATE_OF_BIRTH, GETDATE()) AS IDADE, 
                DATEDIFF(YEAR, DATE_OF_BIRTH, GETDATE()) -
                CASE -- AJUSTE PARA TER A IDADE PRECISA!!!
                    WHEN MONTH(GETDATE()) < MONTH(DATE_OF_BIRTH)
                    OR (MONTH(GETDATE()) = MONTH(DATE_OF_BIRTH) 
                    AND DAY(GETDATE()) < DAY(DATE_OF_BIRTH)) THEN 1 
                    ELSE 0 
                END AS IDADE,   
                REGISTRATION_DATE AS DATA_CADASTRO,
                DATEDIFF(YEAR, REGISTRATION_DATE,  GETDATE()) AS ANOS_CADASTRO,
                created_at AS DATA_BATCH


            FROM SILVER_USERS

    ) SELECT
            ID_CLIENTE,
            NOME,
            SOBRENOME,
            NOME_COMPLETO,
            GENERO,
            EMAIL,
            CPF,
            CASE 
                WHEN (IDADE - ANOS_CADASTRO) < 18 OR (IDADE - ANOS_CADASTRO) > 80 THEN 'BLOCKED'
                ELSE 'ACTIVE'
            END AS STATUS_CONTA,
            IDADE - ANOS_CADASTRO AS IDADE_CADASTRO,            
            RUA,
            NUMERO_ENDERECO,
            CIDADE,
            UF,
            PAIS,
            ENDERECO_COMPLETO,
            LATITUDE,
            LONGITUDE,
            DATA_NASCIMENTO,
            IDADE,
            DATA_CADASTRO,
            ANOS_CADASTRO,
            CASE 
                WHEN IDADE < 18 THEN '00 - MENOR DE 18 ANOS'
                WHEN IDADE >= 18 AND IDADE <= 21 THEN '01 - DE 18 A 21 ANOS'
                WHEN IDADE >= 22 AND IDADE <= 30 THEN '02 - DE 22 A 30 ANOS'
                WHEN IDADE >= 31 AND IDADE <= 40 THEN '03 - DE 31 A 40 ANOS'
                WHEN IDADE >= 41 AND IDADE <= 50 THEN '04 - DE 41 A 50 ANOS'
                WHEN IDADE >= 51 AND IDADE <= 60 THEN '05 - DE 51 A 60 ANOS'
                WHEN IDADE >= 61 AND IDADE <= 70 THEN '06 - DE 61 A 70 ANOS'
                WHEN IDADE >= 71 AND IDADE <= 80 THEN '07 - DE 71 A 80 ANOS'
                ELSE '08 - MAIOR DE 81 ANOS'
            END AS FAIXA_IDADE,
            DATA_BATCH
    FROM BASE_USERS_TRATADA

;

*/


-- SELECT * FROM GOLD_USERS