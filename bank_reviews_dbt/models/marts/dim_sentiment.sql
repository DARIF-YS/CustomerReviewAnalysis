-- models/marts/dim_sentiment.sql
with base as (
    select distinct sentiment
    from {{ source('ma_bdd', 'reviews_enriched') }}
),

with_ids as (
    select
        row_number() over (order by sentiment) as sentiment_id,
        sentiment
    from base
)

select * from with_ids
