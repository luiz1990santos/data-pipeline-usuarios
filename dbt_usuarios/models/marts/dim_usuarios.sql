{{ config(materialized='view') }}

SELECT
    ID_USUARIO,
    NOME,
    SOBRENOME,
    NOME_COMPLETO,
    EMAIL,
    DATA_NASCIMENTO,
    RUN_ID

FROM {{ ref('int_usuarios_validos') }}
