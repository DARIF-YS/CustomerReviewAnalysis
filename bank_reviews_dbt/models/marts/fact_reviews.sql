-- models/marts/fact_reviews.sql
with source as (

    select * from {{ source('ma_bdd', 'reviews_enriched') }}
),

joined as (

    select
        src.id as review_id,
        b.bank_id,
        br.branch_id,
        l.location_id,
        s.sentiment_id,
        src.review_date,
        src.review_rating,
        src.language,
        src.topic_name

    from source src

    left join {{ ref('dim_bank') }} b
        on src.bank_name = b.bank_name
        and src.bank_rating = b.bank_rating

    left join {{ ref('dim_branch') }} br
        on src.branch_name = br.branch_name

    left join {{ ref('dim_location') }} l
        on src.bank_location = l.bank_location

    left join {{ ref('dim_sentiment') }} s
        on src.sentiment = s.sentiment

)

select * from joined
