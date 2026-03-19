import { useTranslations } from 'next-intl';

export default function Footer() {
  const t = useTranslations('common');
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 mt-auto">
      <div className="container mx-auto px-4 text-center text-sm">
        <p>© 2026 {t('siteName')}. All rights reserved.</p>
      </div>
    </footer>
  );
}
