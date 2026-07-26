from app.db.datastore import news_df, row_to_dict

users_db = {}

def get_or_create_user(user_id: str) -> dict:
    if user_id not in users_db:
        users_db[user_id] = {'user_id': user_id, 'read_article_ids': set()}
    return users_db[user_id]

def mark_article_read(user_id: str, news_id: int) -> bool:
    user = get_or_create_user(user_id)
    if news_id in user['read_article_ids']:
        return False
    user['read_article_ids'].add(news_id)
    return True

def get_read_history(user_id: str) -> list[int]:
    user = get_or_create_user(user_id)
    return sorted(list(user['read_article_ids']))

def get_read_articles_data(user_id: str) -> list[dict]:
    history = get_read_history(user_id)
    if not history or news_df.empty:
        return []
    
    # Filter rows based on the history
    read_rows = news_df[news_df['news_id'].isin(history)]
    return [row_to_dict(row) for _, row in read_rows.iterrows()]
