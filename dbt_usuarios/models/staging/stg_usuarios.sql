{{ config(materialized='view') }}

SELECT
    ID AS ID_USUARIO,
    FIRST_NAME AS NOME,
    LAST_NAME AS SOBRENOME,
    EMAIL,
    CAST(DATE_OF_BIRTH AS DATE) AS DATA_NASCIMENTO,
    RUN_ID,
    VALIDACAO

FROM {{ source('bronze', 'bronze_usuarios') }}