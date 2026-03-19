'use client';

import { useLocale } from 'next-intl';
import { Link } from '@/i18n/routing';
import type { HeritageItemSummary } from '@/lib/types';

export default function HeritageCard({ item }: { item: HeritageItemSummary }) {
  const locale = useLocale();
  const name = locale === 'en' && item.name_en ? item.name_en : item.name;
  const summary = locale === 'en' && item.summary_en ? item.summary_en : item.summary;

  return (
    <Link href={`/heritage/${item.id}`} className="block">
      <div className="bg-white rounded-lg shadow hover:shadow-md transition-shadow overflow-hidden">
        <div className="h-48 bg-gray-200 flex items-center justify-center text-gray-400">
          {/* Placeholder for cover image */}
          <span className="text-4xl">🏛️</span>
        </div>
        <div className="p-4">
          <span className="text-xs text-primary font-medium">{item.category_name}</span>
          <h3 className="font-semibold mt-1 line-clamp-1">{name}</h3>
          <p className="text-sm text-gray-600 mt-1 line-clamp-2">{summary}</p>
        </div>
      </div>
    </Link>
  );
}
