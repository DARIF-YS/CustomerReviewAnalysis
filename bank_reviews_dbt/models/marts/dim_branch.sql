-- models/marts/dim_branch.sql
with base as (
    select distinct
        branch_name
    from {{ source('ma_bdd', 'reviews_enriched') }}
),

with_ids as (
    select
        row_number() over (order by branch_name) as branch_id,
        *
    from base
)

select * from with_ids
