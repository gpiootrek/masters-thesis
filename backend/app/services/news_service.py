from app.db.datastore import news_df, row_to_dict


def get_all(skip: int, limit: int):
    if news_df.empty:
        return []
    return [row_to_dict(row) for _, row in news_df.iloc[skip: skip + limit].iterrows()]


def get_by_category(category_name: str, skip: int, limit: int):
    if news_df.empty:
        return []
    filtered_df = news_df[news_df['label'].str.lower() ==
                          category_name.lower()]
    return [row_to_dict(row) for _, row in filtered_df.iloc[skip: skip + limit].iterrows()]


def get_random_diverse():
    if news_df.empty:
        return []
    grouped = news_df.groupby('label').apply(
        lambda x: x.sample(1)).reset_index(drop=True)
    diverse_sample = grouped.sample(min(5, len(grouped)))
    return [row_to_dict(row) for _, row in diverse_sample.iterrows()]


def get_by_id(news_id: int):
    if news_df.empty:
        return None
    news = news_df[news_df['news_id'] == news_id]
    if news.empty:
        return None
    return row_to_dict(news.iloc[0])
