'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { api } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import type { Review, PaginatedResponse } from '@/lib/types';

export default function ReviewSection({ itemId }: { itemId: string }) {
  const t = useTranslations('review');
  const { state } = useAuth();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [content, setContent] = useState('');
  const [rating, setRating] = useState(0);

  const loadReviews = () => {
    api.get<PaginatedResponse<Review>>(`/reviews/items/${itemId}/reviews/`).then(res => {
      if (res.code === 200) setReviews(res.data.results);
    });
  };

  useEffect(() => { loadReviews(); }, [itemId]);

  const submitReview = async () => {
    if (!content.trim()) return;
    await api.post(`/reviews/items/${itemId}/reviews/create/`, {
      content, rating: rating || null,
    });
    setContent('');
    setRating(0);
    loadReviews();
  };

  return (
    <section>
      <h2 className="text-xl font-semibold mb-4">{t('title')}</h2>

      {state.user && (
        <div className="bg-white p-4 rounded shadow-sm mb-6">
          <div className="flex gap-1 mb-2">
            {[1, 2, 3, 4, 5].map(star => (
              <button key={star} onClick={() => setRating(star)}
                className={`text-2xl ${star <= rating ? 'text-yellow-400' : 'text-gray-300'}`}>
                ★
              </button>
            ))}
          </div>
          <textarea
            value={content} onChange={e => setContent(e.target.value)}
            placeholder={t('writeReview')} maxLength={500}
            className="w-full border rounded p-2 text-sm" rows={3}
          />
          <button onClick={submitReview}
            className="mt-2 bg-primary text-white px-4 py-2 rounded text-sm hover:bg-primary-dark">
            {t('submitReview')}
          </button>
        </div>
      )}

      {reviews.length === 0 ? (
        <p className="text-gray-500">{t('noReviews')}</p>
      ) : (
        <div className="space-y-4">
          {reviews.map(review => (
            <div key={review.id} className="bg-white p-4 rounded shadow-sm">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-medium text-sm">{review.nickname}</span>
                {review.rating && <span className="text-yellow-400 text-sm">{'★'.repeat(review.rating)}</span>}
                <span className="text-xs text-gray-400">{new Date(review.created_at).toLocaleDateString()}</span>
              </div>
              <p className="text-sm">{review.content}</p>
              {review.replies.length > 0 && (
                <div className="ml-6 mt-2 space-y-2">
                  {review.replies.map(reply => (
                    <div key={reply.id} className="text-sm border-l-2 border-gray-200 pl-3">
                      <span className="font-medium">{reply.nickname}</span>
                      <span className="text-xs text-gray-400 ml-2">{new Date(reply.created_at).toLocaleDateString()}</span>
                      <p>{reply.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
