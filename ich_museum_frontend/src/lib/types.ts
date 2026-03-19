/** Shared TypeScript types matching Django API responses. */

export interface UserInfo {
  id: string;
  email: string;
  role: 'user' | 'content_manager' | 'admin';
  is_verified: boolean;
  nickname: string;
  avatar: string;
}

export interface Category {
  id: number;
  name: string;
  name_en: string;
  code: string;
}

export interface HeritageItemSummary {
  id: string;
  name: string;
  name_en: string;
  summary: string;
  summary_en: string;
  category_name: string;
  region_name: string;
  status: string;
  is_favorited: boolean;
  created_at: string;
}

export interface HeritageItemDetail extends HeritageItemSummary {
  category: Category;
  region: { id: number; name: string; name_en: string } | null;
  description: string;
  description_en: string;
  history: string;
  history_en: string;
  inheritors: { id: string; name: string; name_en: string; title: string; bio: string }[];
  created_by: string;
  updated_at: string;
}

export interface Review {
  id: string;
  nickname: string;
  rating: number | null;
  content: string;
  replies: { id: string; nickname: string; content: string; created_at: string }[];
  created_at: string;
}

export interface RatingStats {
  average_rating: number;
  review_count: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
