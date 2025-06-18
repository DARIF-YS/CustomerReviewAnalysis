from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import gensim
from gensim import corpora
import nltk
from langdetect import detect, LangDetectException
from nltk.stem import WordNetLemmatizer
from gensim.utils import simple_preprocess
import pandas as pd

from sqlalchemy import inspect, text, create_engine
from dotenv import load_dotenv
import os


# Fonction pour enrichir les données
def enrich_reviews():
    
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Lire les paramètres de connexion depuis les variables d'environnement
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host     = os.getenv("DB_HOST")
    port     = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    # Construire l'URL de connexion PostgreSQL
    DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    # Créer le moteur SQLAlchemy
    engine = create_engine(DATABASE_URL)

    # Charger les données
    query = "SELECT * FROM reviews_transformed"
    df = pd.read_sql(query, engine)

    #with engine.begin() as conn:
    #    conn.execute(text("DROP Table reviews_transformed"))
    #    conn.execute(text("DROP Table bank_reviews"))

    def safe_detect(text):
        try:
            if isinstance(text, str) and text.strip():
                return detect(text)
            else:
                return "unknown"
        except LangDetectException:
            return "unknown"

    df["language"] = df["review_text"].apply(safe_detect)
    
    # Détection de langue
    #df["language"] = df["review_text"].apply(lambda x: detect(x) if isinstance(x, str) else "unknown")

     # Analyse de sentiment
    sia = SentimentIntensityAnalyzer()

    def get_sentiment(text):
        vader_score = sia.polarity_scores(text)["compound"]
        if vader_score > 0.05:
            return "Positive"
        elif vader_score < -0.05:
            return "Negative"
        else:
            return "Neutral"
    df["sentiment"] = df["en_review"].apply(get_sentiment)

    # Topic Modeling With LDA
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    
    lemmatizer = WordNetLemmatizer()

    def Tokenize_lemmatize(review):
        # Tokenization 
        tokens = simple_preprocess(review)  

        # Lemmatization (et on enlève les tokens trop courts)
        tokens = [lemmatizer.lemmatize(word) for word in tokens if len(word) > 2]

        return tokens
    
    df['tokens'] = df['en_review'].apply(Tokenize_lemmatize)

    # Créer dictionnaire et corpus
    dictionary = corpora.Dictionary(df['tokens'])
    corpus = [dictionary.doc2bow(text) for text in df['tokens']]

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=13, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
    
    # 1. Générer les noms des topics à partir des mots-clés dominants
    def generate_topic_names(lda_model, topn=4):
        topic_names = {}
        for topic_id, topic_words in lda_model.show_topics(num_topics=lda_model.num_topics, formatted=False, num_words=topn):
            keywords = [word for word, _ in topic_words]
            topic_name = "_".join(keywords)
            topic_name = topic_name
            topic_names[topic_id] = topic_name
        return topic_names

    topic_names = generate_topic_names(lda_model)

    # 2. Fonction pour récupérer directement le nom du topic dominant
    def get_dominant_topic_name(doc_bow, lda_model, topic_names):
        topics = lda_model.get_document_topics(doc_bow)
        topics = sorted(topics, key=lambda x: x[1], reverse=True)
        dominant_topic_id = topics[0][0]
        # Protection contre les index de topic inexistants
        if dominant_topic_id in topic_names:
            return topic_names[dominant_topic_id]
        else:
            return f"Topic not found" 

    # 3. Appliquer à tous les documents
    df['topic_name'] = [get_dominant_topic_name(bow, lda_model, topic_names) for bow in corpus]
    df = df.drop(columns=['tokens'])

    # Enregistrer dans une nouvelle table
    inspector = inspect(engine)

    if inspector.has_table('reviews_enriched', schema='public'):

        with engine.begin() as conn:
            conn.execute(text("DELETE FROM reviews_enriched"))
        df.to_sql("reviews_enriched", engine, if_exists="append", index=False)

    else:
        df.to_sql("reviews_enriched", engine, if_exists="replace", index=False)

