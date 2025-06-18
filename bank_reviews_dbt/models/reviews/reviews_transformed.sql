{{ config(materialized='table') }}

{% set stop_words = [
    'between', 'd', "it''ll", 'over', 'whom', 'mightn', 'it'
    , "he''s", 'if', 'so', 'off', 'when', 'and', 'couldn', 'up'
    , 'are', 'y', 'my', 'their', 'just', "he''d", 'where', 'i'
    , "shan''t", "doesn''t", 'were', "didn''t", 'for', 'his', 'by'
    , 'should', 'that', 'same', 'other', 'both', 'she', "i''d"
    , 'aren', 'but', 'yours', 'isn', 'against', 'a', 'of'
    , 'such', 'no', 'themselves', 've', 'mustn', 'at', 'can'
    , "should''ve", "won''t", "weren''t", 'ma', "mightn''t", 'her'
    , "needn''t", "they''ve", 'after', 'having', 'them', 'its'
    , 'nor', 'is', 'm', 'am', 'do', 'any', 'own', "shouldn''t"
    , 'into', 'under', 'our', "couldn''t", 'each', 'before'
    , 'wasn', 'he', 'ourselves', 'ain', 'hasn', "we''d", 'him'
    , 'there', "hadn''t", 'on', 'who', 'most', 'hers', 'be'
    , 'or', "they''ll", 'not', 'above', 'with', 'through'
    , 'shouldn', "he''ll", 'during', "wasn''t", 'an', 'itself'
    , 'they', "she''s", 'why', 'll', 'further', 'yourself'
    , "i''ve", 'in', 'until', 'what', 'which', "you''ve", 'we'
    , 'the', 'herself', 'doing', 'how', 't', 'o', 'himself'
    , 'some', "i''m", 'you', "you''ll", "you''re", 'down', 'few'
    , 'will', 'these', 'while', 's', "i''ll", 'been', "don''t"
    , 'hadn', 'your', "mustn''t", 'about', "isn''t", "she''d"
    , 'don', 'doesn', "wouldn''t", 'all', 'from', 'has'
    , 'below', 'because', 'now', 'once', 'myself', "we''re"
    , "that''ll", 'very', 'was', "aren''t", 'wouldn', "hasn''t"
    , "it''d", 'too', "haven''t", 'does', 'again', 'only'
    , 'more', 'had', 're', 'as', 'needn', 'theirs', 'out'
    , "it''s", 'to', "you''d", 'weren', 'yourselves', "they''d"
    , 'then', 'won', 'shan', 'being', 'than', "she''ll", 'this'
    , 'haven', 'me', "we''ll", 'did', "we''ve", 'didn', 'ours'
    , 'have', "they''re", 'those', 'here','c'
] %}

{% set stop_words_regex = '\\m(' + '|'.join(stop_words) + ')\\M' %}

WITH reviews_raw AS (
    SELECT 
        id,
        TRIM(REGEXP_REPLACE(LOWER(bank_name), '\s*\(.*?\)', '', 'g')) AS bank_name,
        CAST(REPLACE(bank_rating, ',', '.') AS FLOAT) AS bank_rating,
        TRIM(REGEXP_REPLACE(LOWER(bank_location), '[-،؛]', ',', 'g')) AS bank_location,
        REGEXP_REPLACE(review_date, '[\s\u00A0]', ' ', 'g') AS review_date,
        TRIM(REGEXP_REPLACE(lower(en_review), '[\n\t\r]|[^a-zA-Z\s]+', ' ', 'g')) AS en_review,
        review_text,
        review_rating::INTEGER AS review_rating
    FROM {{ source('raw_data', 'bank_reviews') }}
),

reviews_enhanced AS (
    SELECT 
        id,
        bank_name,
        bank_rating,
        bank_location,
        CASE
            WHEN ARRAY_LENGTH(STRING_TO_ARRAY(bank_location, ','), 1) = 2 THEN bank_name || ',' || bank_location
            ELSE bank_name || ', ' || split_part(bank_location, ',', -2) || ', ' || split_part(bank_location, ',', -1)  
        END AS branch_name,
        -- Simplified date handling with regex
        CASE 
            WHEN review_date = 'il y a un jour' THEN DATE(CURRENT_DATE - INTERVAL '1 day')
            WHEN review_date LIKE 'il y a % jours' THEN DATE(CURRENT_DATE - CAST(REGEXP_REPLACE(review_date, '[^0-9]', '', 'g') AS INTEGER) * INTERVAL '1 day')
            WHEN review_date = 'il y a une semaine' THEN DATE(CURRENT_DATE - INTERVAL '7 days')
            WHEN review_date LIKE 'il y a % semaines' THEN DATE(CURRENT_DATE - CAST(REGEXP_REPLACE(review_date, '[^0-9]', '', 'g') AS INTEGER) * INTERVAL '7 days')
            WHEN review_date = 'il y a un mois' THEN DATE(CURRENT_DATE - INTERVAL '1 month')
            WHEN review_date LIKE 'il y a % mois' THEN DATE(CURRENT_DATE - CAST(REGEXP_REPLACE(review_date, '[^0-9]', '', 'g') AS INTEGER) * INTERVAL '1 month')
            WHEN review_date = 'il y a un an' THEN DATE(CURRENT_DATE - INTERVAL '1 year')
            WHEN review_date LIKE 'il y a % ans' THEN DATE(CURRENT_DATE - CAST(REGEXP_REPLACE(review_date, '[^0-9]', '', 'g') AS INTEGER) * INTERVAL '1 year')
            ELSE DATE(CURRENT_DATE)
        END AS review_date,
        TRIM(regexp_replace(regexp_replace(en_review, '{{ stop_words_regex }}', '', 'gi'), '\s+', ' ', 'g')) AS en_review,
        review_text,
        review_rating 
    FROM reviews_raw
)

SELECT DISTINCT * FROM reviews_enhanced
WHERE en_review IS NOT NULL AND en_review <> '' AND review_text IS NOT NULL AND review_text ~ '[A-Za-z]'