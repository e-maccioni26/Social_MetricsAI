import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report
import os
from config import MODEL_PATH
import logging

logging.basicConfig(level=logging.INFO)

# Liste personnalisée de stop words en français
french_stop_words = [
    "alors", "au", "aucuns", "aussi", "autre", "avant", "avec", "avoir", "bon", "car", "ce", "cela", "ces", "ceux",
    "chaque", "ci", "comme", "comment", "dans", "des", "du", "dedans", "dehors", "depuis", "devrait", "doit",
    "donc", "dos", "début", "elle", "elles", "en", "encore", "essai", "est", "et", "eu", "fait", "faites", "fois",
    "font", "hors", "ici", "il", "ils", "je", "juste", "la", "le", "les", "leur", "là", "ma", "maintenant", "mais",
    "mes", "mine", "moins", "mon", "mot", "même", "ni", "nommés", "notre", "nous", "nouveaux", "ou", "où", "par",
    "parce", "parole", "pas", "personnes", "peu", "peut", "plupart", "pour", "pourquoi", "quand", "que", "quel",
    "quelle", "quelles", "quels", "qui", "sa", "sans", "ses", "seulement", "si", "sien", "son", "sont", "sous",
    "soyez", "sujet", "sur", "ta", "tandis", "tellement", "tels", "tes", "ton", "tous", "tout", "trop", "très",
    "tu", "valeur", "voie", "voient", "vont", "votre", "vous", "vu", "ça", "étaient", "état", "étions", "été",
    "être"
]

def train_model(texts, positive_labels, negative_labels):
    vectorizer_params = {
        'ngram_range': (1, 2),  
        'stop_words': french_stop_words  
    }
    
    model_positive = Pipeline([
        ('tfidf', TfidfVectorizer(**vectorizer_params)),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    model_positive.fit(texts, positive_labels)
    logging.info("Modèle positif entraîné.")

    model_negative = Pipeline([
        ('tfidf', TfidfVectorizer(**vectorizer_params)),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    model_negative.fit(texts, negative_labels)
    logging.info("Modèle négatif entraîné.")

    joblib.dump((model_positive, model_negative), MODEL_PATH)
    logging.info("Modèles sauvegardés dans %s", MODEL_PATH)
    return model_positive, model_negative

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    model_positive, model_negative = joblib.load(MODEL_PATH)
    return model_positive, model_negative

def predict_sentiment(tweets):
    models = load_model()
    if models is None:
        raise Exception("Le modèle n'est pas encore entraîné.")
    model_positive, model_negative = models
    scores = {}
    for tweet in tweets:
        p_positive = model_positive.predict_proba([tweet])[0][1]
        p_negative = model_negative.predict_proba([tweet])[0][1]
        score = p_positive - p_negative  # Score dans [-1, 1]
        logging.info("Tweet: '%s' -> p_positive: %.3f, p_negative: %.3f, score: %.3f", tweet, p_positive, p_negative, score)
        scores[tweet] = score
    return scores

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return cm, report
