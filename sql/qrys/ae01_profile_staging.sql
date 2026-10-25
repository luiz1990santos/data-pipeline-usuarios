----------------------------------------------------------
-- INVESTIGACAO DA QUALIDADE DOS DADOS NAS EXECUÇOES
----------------------------------------------------------

-- ULTIMAS EXECUCOES CONCLUIDAS COM SUCESSO
SELECT TOP (5)
       run_id,
       started_at,
       status
FROM PIPELINE_RUNS
WHERE status = 'SUCCESS'
ORDER BY started_at DESC
;



-- VOLUME TOTAL DE REGISTROS
SELECT 
    COUNT(*) AS VOLUME_TOTAL 
FROM DBO.STAGING_USERS
WHERE run_id = 'run_36a8c05168c64fb3bb70f58a9d63fb0a'
;


-- REGISTROS COM ID OU EMAIL NULO
SELECT
    COUNT(*) AS VOLUME_TOTAL,

    SUM(CASE
        WHEN ID IS NULL OR TRIM(ID) = ''
        THEN 1 ELSE 0
    END) AS ID_INVALIDO,

    SUM(CASE
        WHEN EMAIL IS NULL OR TRIM(EMAIL) = ''
        THEN 1 ELSE 0
    END) AS EMAIL_INVALIDO

FROM DBO.STAGING_USERS
WHERE run_id = 'run_36a8c05168c64fb3bb70f58a9d63fb0a';


-- VALIDACAO OK E NOK
SELECT
    COALESCE(
        NULLIF(TRIM(VALIDACAO), ''),
        'SEM_CLASSIFICACAO'
    ) AS VALIDACAO,
    COUNT(*) AS VOLUME

FROM DBO.STAGING_USERS
WHERE run_id = 'run_36a8c05168c64fb3bb70f58a9d63fb0a'

GROUP BY
    COALESCE(
        NULLIF(TRIM(VALIDACAO), ''),
        'SEM_CLASSIFICACAO'
    );


-- VALIDACAO DUPLICIDADE DE ID
SELECT 
    ID,
    COUNT(*) AS ID_DUPLICIDADE
FROM DBO.STAGING_USERS
WHERE run_id = 'run_36a8c05168c64fb3bb70f58a9d63fb0a'

GROUP BY ID
HAVING COUNT(*) > 1 
;


