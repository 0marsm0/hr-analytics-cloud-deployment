
with stg_job_ads as (
    select * from {{ source('jobtech_analysis', 'job_ads') }}
)

select
    id,
    experience_required,
    access_to_own_car,
    driving_license_required
from stg_job_ads
where occupation_field__concept_id in ('apaJ_2ja_LuF', 'ASGV_zcE_bWf', 'NYW6_mP6_vwf')
