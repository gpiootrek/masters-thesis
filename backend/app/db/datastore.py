import pandas as pd
import os

# Ścieżka relatywna do pliku z danymi
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/news_sample_24s_annotated.csv")

def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        df = df.where(pd.notnull(df), None) 
        return df
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku pod ścieżką {DATA_PATH}")
        return pd.DataFrame()

# Globalna zmienna z wczytanymi danymi (nasza "baza danych" w pamięci)
news_df = load_data()

def row_to_dict(row) -> dict:
    """Helper do konwersji wiersza z Pandas do słownika dla Pydantic."""
    return {
        "id": int(row["id"]),
        "title": str(row["title"]),
        "content": str(row["content"]),
        "category": str(row["category"]),
        "sentiment_bielik": str(row["sentiment_bielik"]) if row["sentiment_bielik"] else None,
        "political_bias_bielik": str(row["political_bias_bielik"]) if row["political_bias_bielik"] else None,
        "sentiment_explanation_bielik": str(row["sentiment_explanation_bielik"]) if "sentiment_explanation_bielik" in row and row["sentiment_explanation_bielik"] else None,
        "political_bias_explanation_bielik": str(row["political_bias_explanation_bielik"]) if "political_bias_explanation_bielik" in row and row["political_bias_explanation_bielik"] else None,
        "sentiment_gemma": str(row["sentiment_gemma"]) if row["sentiment_gemma"] else None,
        "political_bias_gemma": str(row["political_bias_gemma"]) if row["political_bias_gemma"] else None,
        "sentiment_explanation_gemma": str(row["sentiment_explanation_gemma"]) if "sentiment_explanation_gemma" in row and row["sentiment_explanation_gemma"] else None,
        "political_bias_explanation_gemma": str(row["political_bias_explanation_gemma"]) if "political_bias_explanation_gemma" in row and row["political_bias_explanation_gemma"] else None,
        "sentiment_gt": str(row["sentiment_gt"]) if row["sentiment_gt"] else None,
        "political_bias_gt": str(row["political_bias_gt"]) if row["political_bias_gt"] else None,
    }