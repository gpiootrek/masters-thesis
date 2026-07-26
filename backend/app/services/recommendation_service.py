import numpy as np
import pandas as pd
from app.db.datastore import news_df, row_to_dict

# Column names used for the entropy calculation
TOPIC_COL = 'label'
SENTIMENT_COL = 'sentiment_bielik'
BIAS_COL = 'political_bias_bielik'

def _get_tsp_tuple(row) -> tuple:
    """Extract (topic, sentiment, political_bias) tuple from a dataframe row."""
    return (row[TOPIC_COL], row[SENTIMENT_COL], row[BIAS_COL])

def calculate_entropy(articles_data: list[dict]) -> float:
    """Calculate joint entropy H(T, S, P) from a list of article dicts."""
    if not articles_data:
        return 0.0
    counts = {}
    total = len(articles_data)
    for article in articles_data:
        key = (article.get(TOPIC_COL, ''), article.get(SENTIMENT_COL, ''), article.get(BIAS_COL, ''))
        counts[key] = counts.get(key, 0) + 1
    entropy = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * np.log2(p)
    return entropy

def calculate_normalized_diversity(articles_data: list[dict]) -> float:
    """Calculate normalized diversity D = H(T,S,P) / log2(|T|*|S|*|P|)."""
    if not articles_data:
        return 0.0
    # Count actual number of unique topics in the dataset
    all_topics = news_df[TOPIC_COL].dropna().unique()
    all_sentiments = news_df[SENTIMENT_COL].dropna().unique()
    all_biases = news_df[BIAS_COL].dropna().unique()
    max_combos = len(all_topics) * len(all_sentiments) * len(all_biases)
    if max_combos <= 1:
        return 0.0
    max_entropy = np.log2(max_combos)
    entropy = calculate_entropy(articles_data)
    return entropy / max_entropy

def _compute_entropy_from_counts(counts: dict, total: int) -> float:
    """Compute entropy from a frequency dict and total count."""
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * np.log2(p)
    return entropy

def _compute_d_from_counts(counts: dict, total: int, max_entropy: float) -> float:
    """Compute normalized diversity D from frequency counts."""
    if max_entropy == 0 or total == 0:
        return 0.0
    return _compute_entropy_from_counts(counts, total) / max_entropy

def get_diversity_recommendations(read_article_ids: list[int], count: int = 10) -> dict:
    """
    Get article recommendations that maximize the growth of normalized diversity D.
    
    Uses a greedy sequential algorithm:
    1. Start with the user's current (T,S,P) distribution
    2. For each slot (up to `count`):
       a. Group unread articles by (T,S,P) combo
       b. For each combo, compute delta_D if we add one article
       c. Pick the combo with highest delta_D
       d. Select a random article from that combo
       e. Update the distribution
    3. Return selected articles + diversity metrics
    """
    if news_df.empty:
        return {'recommendations': [], 'current_diversity': 0.0, 'potential_diversity': 0.0}
    
    # Determine max entropy from actual unique values in dataset
    all_topics = news_df[TOPIC_COL].dropna().unique()
    all_sentiments = news_df[SENTIMENT_COL].dropna().unique()
    all_biases = news_df[BIAS_COL].dropna().unique()
    max_combos = len(all_topics) * len(all_sentiments) * len(all_biases)
    max_entropy = np.log2(max_combos) if max_combos > 1 else 0.0
    
    # Build current distribution from read articles
    read_set = set(read_article_ids)
    read_rows = news_df[news_df['news_id'].isin(read_set)]
    
    counts = {}
    for _, row in read_rows.iterrows():
        key = _get_tsp_tuple(row)
        counts[key] = counts.get(key, 0) + 1
    total = len(read_rows)
    
    current_d = _compute_d_from_counts(counts, total, max_entropy)
    
    # Get unread articles (exclude rows with null sentiment/bias)
    unread_df = news_df[
        (~news_df['news_id'].isin(read_set)) &
        (news_df[SENTIMENT_COL].notna()) &
        (news_df[BIAS_COL].notna())
    ].copy()
    
    if unread_df.empty:
        return {'recommendations': [], 'current_diversity': current_d, 'potential_diversity': current_d}
    
    # Add TSP column for grouping
    unread_df['_tsp'] = list(zip(unread_df[TOPIC_COL], unread_df[SENTIMENT_COL], unread_df[BIAS_COL]))
    
    selected_ids = []
    sim_counts = dict(counts)  # simulated counts (mutable copy)
    sim_total = total
    
    for _ in range(min(count, len(unread_df))):
        # Group remaining unread by TSP combo
        available = unread_df[~unread_df['news_id'].isin(selected_ids)]
        if available.empty:
            break
        
        tsp_groups = available.groupby('_tsp')['news_id'].apply(list).to_dict()
        
        best_delta = -float('inf')
        best_combo = None
        
        for combo, ids in tsp_groups.items():
            # Simulate adding one article with this combo
            test_counts = dict(sim_counts)
            test_counts[combo] = test_counts.get(combo, 0) + 1
            test_total = sim_total + 1
            new_d = _compute_d_from_counts(test_counts, test_total, max_entropy)
            delta = new_d - _compute_d_from_counts(sim_counts, sim_total, max_entropy)
            
            if delta > best_delta:
                best_delta = delta
                best_combo = combo
        
        if best_combo is None:
            break
        
        # Pick a random article from the best combo
        combo_ids = tsp_groups[best_combo]
        chosen_id = int(np.random.choice(combo_ids))
        selected_ids.append(chosen_id)
        
        # Update simulated distribution
        sim_counts[best_combo] = sim_counts.get(best_combo, 0) + 1
        sim_total += 1
    
    potential_d = _compute_d_from_counts(sim_counts, sim_total, max_entropy)
    
    # Build response
    recommended_articles = []
    for nid in selected_ids:
        row = news_df[news_df['news_id'] == nid]
        if not row.empty:
            recommended_articles.append(row_to_dict(row.iloc[0]))
    
    return {
        'recommendations': recommended_articles,
        'current_diversity': round(current_d, 6),
        'potential_diversity': round(potential_d, 6),
    }


def get_bubble_breaking_recommendations(news_id: int):
    if news_df.empty:
        return []

    target_news = news_df[news_df['news_id'] == news_id]
    if target_news.empty:
        return None

    target_row = target_news.iloc[0]
    target_label = target_row['label']
    target_sentiment = target_row['sentiment_bielik']
    target_bias = target_row['political_bias_bielik']

    candidates = news_df[news_df['news_id'] != news_id]

    condition_same_topic = candidates['label'] == target_label
    condition_diff_perspective = (candidates['sentiment_bielik'] != target_sentiment) | (
        candidates['political_bias_bielik'] != target_bias)

    recommended_df = candidates[condition_same_topic &
                                condition_diff_perspective]

    if len(recommended_df) < 5:
        shortfall = 5 - len(recommended_df)
        filler_condition = (candidates['label'] == target_label) & ~candidates.index.isin(
            recommended_df.index)
        filler_df = candidates[filler_condition].sample(
            min(shortfall, len(candidates[filler_condition])))
        recommended_df = pd.concat([recommended_df, filler_df])

    final_sample = recommended_df.sample(min(5, len(recommended_df)))
    return [row_to_dict(row) for _, row in final_sample.iterrows()]
