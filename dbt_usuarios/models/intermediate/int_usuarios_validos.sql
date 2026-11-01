{{ config(materialized='view') }}

SELECT
    ID_USUARIO,
    NOME,
    SOBRENOME,
    NOME||' '||SOBRENOME AS NOME_COMPLETO,
    EMAIL,
    DATA_NASCIMENTO,
    RUN_ID,
    VALIDACAO

FROM {{ ref('stg_usuarios') }}

WHERE VALIDACAO = 'OK'