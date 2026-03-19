'use client';

import { useEffect, useState } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { api } from '@/lib/api';
import type { HeritageItemSummary, Category, PaginatedResponse } from '@/lib/types';
import HeritageCard from './HeritageCard';

export default function HeritageList() {
  const t = useTranslations('heritage');
  const locale = useLocale();
  const [items, setItems] = useState<HeritageItemSummary[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<Category[]>('/heritage/categories/').then(res => {
      if (res.code === 200) setCategories(res.data);
    });
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = selectedCategory ? `?category=${selectedCategory}` : '';
    api.get<PaginatedResponse<HeritageItemSummary>>(`/heritage/items/${params}`).then(res => {
      if (res.code === 200) setItems(res.data.results);
      setLoading(false);
    });
  }, [selectedCategory]);

  return (
    <div>
      <div className="flex gap-2 mb-6 flex-wrap">
        <button
          onClick={() => setSelectedCategory('')}
          className={`px-3 py-1 rounded-full text-sm ${!selectedCategory ? 'bg-primary text-white' : 'bg-gray-200'}`}
        >
          {t('allCategories')}
        </button>
        {categories.map(cat => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.code)}
            className={`px-3 py-1 rounded-full text-sm ${selectedCategory === cat.code ? 'bg-primary text-white' : 'bg-gray-200'}`}
          >
            {locale === 'en' && cat.name_en ? cat.name_en : cat.name}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-center text-gray-500">{t('allCategories')}...</p>
      ) : items.length === 0 ? (
        <p className="text-center text-gray-500">暂无项目</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {items.map(item => (
            <HeritageCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
