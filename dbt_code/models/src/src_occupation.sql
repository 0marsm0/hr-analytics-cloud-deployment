with stg_job_ads as (
    select * from {{ source('jobtech_analysis', 'stg_ads') }}
)

select distinct 
    occupation__label as occupation,
    occupation_group__label as occupation_group,
    occupation_field__label as occupation_field,
from stg_job_ads
where occupation_field__concept_id in ["apaJ_2ja_LuF", "ASGV_zcE_bWf", "NYW6_mP6_vwf"]