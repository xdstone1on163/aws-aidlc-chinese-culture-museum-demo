import { useTranslations } from 'next-intl';
import HeritageList from '@/components/heritage/HeritageList';

export default function HomePage() {
  const t = useTranslations('heritage');
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('title')}</h1>
      <HeritageList />
    </div>
  );
}
