'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import ReactMarkdown from 'react-markdown';
import { api } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import type { HeritageItemDetail, RatingStats } from '@/lib/types';
import ReviewSection from '@/components/reviews/ReviewSection';

export default function HeritageDetailPage() {
  const { id } = useParams<{ id: string }>();
  const t = useTranslations('heritage');
  const locale = useLocale();
  const { state } = useAuth();
  const [item, setItem] = useState<HeritageItemDetail | null>(null);
  const [stats, setStats] = useState<RatingStats | null>(null);
  const [favorited, setFavorited] = useState(false);

  useEffect(() => {
    api.get<HeritageItemDetail>(`/heritage/items/${id}/`).then(res => {
      if (res.code === 200) {
        setItem(res.data);
        setFavorited(res.data.is_favorited);
      }
    });
    api.get<RatingStats>(`/reviews/items/${id}/rating/`).then(res => {
      if (res.code === 200) setStats(res.data);
    });
  }, [id]);

  const toggleFavorite = async () => {
    const res = await api.post<{ is_favorited: boolean }>(`/heritage/items/${id}/favorite/`);
    if (res.code === 200) setFavorited(res.data.is_favorited);
  };

  if (!item) return <p className="text-center py-10">{t('detail')}...</p>;

  const name = locale === 'en' && item.name_en ? item.name_en : item.name;
  const desc = locale === 'en' && item.description_en ? item.description_en : item.description;
  const history = locale === 'en' && item.history_en ? item.history_en : item.history;

  return (
    <article className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">{name}</h1>
      <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
        <span>{item.category?.name}</span>
        {item.region && <span>{item.region.name}</span>}
        {stats && <span>⭐ {stats.average_rating} ({stats.review_count})</span>}
        {state.user && (
          <button onClick={toggleFavorite} className="text-red-500 hover:text-red-600">
            {favorited ? '❤️ ' + t('unfavorite') : '🤍 ' + t('favorite')}
          </button>
        )}
      </div>

      <div className="prose max-w-none mb-8">
        <ReactMarkdown>{desc}</ReactMarkdown>
      </div>

      {history && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-3">{t('history')}</h2>
          <div className="prose max-w-none"><ReactMarkdown>{history}</ReactMarkdown></div>
        </section>
      )}

      {item.inheritors.length > 0 && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-3">{t('inheritors')}</h2>
          <div className="grid gap-4">
            {item.inheritors.map(inh => (
              <div key={inh.id} className="bg-white p-4 rounded shadow-sm">
                <p className="font-medium">{inh.name} {inh.title && `(${inh.title})`}</p>
                {inh.bio && <p className="text-sm text-gray-600 mt-1">{inh.bio}</p>}
              </div>
            ))}
          </div>
        </section>
      )}

      <ReviewSection itemId={id} />
    </article>
  );
}
