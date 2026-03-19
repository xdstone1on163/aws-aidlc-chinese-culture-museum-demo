'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { api } from '@/lib/api';
import type { HeritageItemSummary } from '@/lib/types';
import HeritageCard from '@/components/heritage/HeritageCard';

export default function SearchPage() {
  const t = useTranslations('search');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<HeritageItemSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [searched, setSearched] = useState(false);

  const doSearch = async () => {
    if (!query.trim()) return;
    const res = await api.get<{ results: HeritageItemSummary[]; total: number }>(
      `/search/?q=${encodeURIComponent(query)}`
    );
    if (res.code === 200) {
      setResults(res.data.results);
      setTotal(res.data.total);
    }
    setSearched(true);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex gap-2 mb-6">
        <input
          value={query} onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && doSearch()}
          placeholder={t('placeholder')}
          className="flex-1 border rounded px-4 py-2"
        />
        <button onClick={doSearch} className="bg-primary text-white px-6 py-2 rounded">
          {t('results')}
        </button>
      </div>

      {searched && (
        <>
          <p className="text-sm text-gray-500 mb-4">{t('totalResults', { count: total })}</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map(item => <HeritageCard key={item.id} item={item} />)}
          </div>
        </>
      )}
    </div>
  );
}
