with stg_job_ads as (select * from {{ source('jobtech_analysis', 'job_ads') }})
select
    id, -- the thrre coulmns above will all make auxilliary_attributes_id and job_details_id
    employer__workplace,
    workplace_address__municipality, -- will be used as employer_id
    occupation__label, -- will be used as occupation_id
    number_of_vacancies as vacancies,
    application_deadline,
    publication_date
from stg_job_ads
where occupation_field__concept_id in ('apaJ_2ja_LuF', 'ASGV_zcE_bWf', 'NYW6_mP6_vwf')