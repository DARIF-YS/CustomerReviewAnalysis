-- models/marts/dim_bank.sql
with base as (
    select distinct
        bank_name,
        bank_rating
    from {{ source('ma_bdd', 'reviews_enriched') }}
),

with_ids as (
    select
        row_number() over (order by bank_name) as bank_id,
        *
    from base
)

select * from with_ids