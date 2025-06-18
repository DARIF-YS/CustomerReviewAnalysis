-- models/marts/dim_location.sql
with base as (
    select distinct
        bank_location
    from {{ source('ma_bdd', 'reviews_enriched') }}
),

with_ids as (
    select
        row_number() over (order by bank_location) as location_id,
        *
    from base
)

select * from with_ids
