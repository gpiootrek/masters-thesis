export interface NewsBase {
  id: number;
  title: string;
  content: string;
  category: string;
  sentiment_bielik: string | null;
  political_bias_bielik: string | null;
  sentiment_gemma: string | null;
  political_bias_gemma: string | null;
  sentiment_gt: string | null;
  political_bias_gt: string | null;
}

export interface NewsDetail extends NewsBase {
  sentiment_explanation_bielik: string | null;
  political_bias_explanation_bielik: string | null;
  sentiment_explanation_gemma: string | null;
  political_bias_explanation_gemma: string | null;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  news: NewsBase[];
}

export interface ReadHistoryResponse {
  user_id: string;
  read_article_ids: number[];
  total_read: number;
  diversity_score: number;
}

export interface RecommendationResponse {
  recommendations: NewsBase[];
  current_diversity: number;
  potential_diversity: number;
}