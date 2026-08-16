
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



SELECT 
    *
FROM PIPELINE_RUNS
ORDER BY started_at DESC;






SELECT * FROM PIPELINE_RUNS
Order by started_at desc;


SELECT 'PIPELINE_RUNS' AS origem, run_id
FROM PIPELINE_RUNS
WHERE run_id = 'run_31527a302eac45b69dd2fe6c25ab8721'

UNION ALL

SELECT 'STAGING_USERS', run_id
FROM STAGING_USERS
WHERE run_id = 'run_31527a302eac45b69dd2fe6c25ab8721'
GROUP BY run_id

UNION ALL

SELECT 'SILVER_USERS', run_id
FROM SILVER_USERS
WHERE run_id = 'run_31527a302eac45b69dd2fe6c25ab8721'
GROUP BY run_id;