'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { api } from '@/lib/api';
import type { PaginatedResponse } from '@/lib/types';
import HeritageCard from '@/components/heritage/HeritageCard';

export default function FavoritesPage() {
  const tc = useTranslations('common');
  const [favorites, setFavorites] = useState<any[]>([]);

  useEffect(() => {
    api.get<PaginatedResponse<any>>('/heritage/favorites/').then(res => {
      if (res.code === 200) setFavorites(res.data.results);
    });
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{tc('favorites')}</h1>
      {favorites.length === 0 ? (
        <p className="text-gray-500">{tc('noResults')}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map(fav => (
            <HeritageCard key={fav.id} item={fav.heritage_item} />
          ))}
        </div>
      )}
    </div>
  );
}
