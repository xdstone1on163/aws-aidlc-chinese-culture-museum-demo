'use client';

import { useTranslations } from 'next-intl';
import { Link, usePathname, useRouter } from '@/i18n/routing';
import { useAuth } from '@/contexts/AuthContext';

export default function Header() {
  const t = useTranslations('common');
  const { state, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const switchLocale = (locale: 'zh' | 'en') => {
    router.replace(pathname, { locale });
  };

  return (
    <header className="bg-primary text-white shadow-md">
      <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold">{t('siteName')}</Link>

        <div className="flex items-center gap-4">
          <Link href="/" className="hover:text-accent-light">{t('home')}</Link>
          <Link href="/search" className="hover:text-accent-light">{t('search')}</Link>

          {state.user ? (
            <>
              <Link href="/profile" className="hover:text-accent-light">{t('profile')}</Link>
              <button onClick={logout} className="hover:text-accent-light">{t('logout')}</button>
            </>
          ) : (
            <>
              <Link href="/login" className="hover:text-accent-light">{t('login')}</Link>
              <Link href="/register" className="hover:text-accent-light">{t('register')}</Link>
            </>
          )}

          <div className="flex gap-1 ml-2 text-sm">
            <button onClick={() => switchLocale('zh')} className="hover:text-accent-light">中</button>
            <span>/</span>
            <button onClick={() => switchLocale('en')} className="hover:text-accent-light">EN</button>
          </div>
        </div>
      </nav>
    </header>
  );
}
