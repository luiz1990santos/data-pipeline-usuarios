
USE ANALYTICS_HUB;

SELECT COUNT(*) AS VOLUME_STAGING FROM STAGING_USERS;

SELECT COUNT(*) AS VOLUME_SIVLER FROM SILVER_USERS;

SELECT COUNT(*) AS VOLUME_GOLD FROM GOLD_USERS;

-- TESTES DE DUPLICIDADE
SELECT 
    ID, 
    count(*) as duplicidados 
FROM STAGING_USERS
GROUP BY ID
HAVING count(*) > 1
--ORDER BY created_at desc
;



SELECT 
    ID, 
    count(*) as duplicidados 
FROM SILVER_USERS
GROUP BY ID
HAVING count(*) > 1
--ORDER BY created_at desc
;



SELECT 
    ID_CLIENTE, 
    count(*) as duplicidados 
FROM GOLD_USERS
GROUP BY ID_CLIENTE
HAVING count(*) > 1
;