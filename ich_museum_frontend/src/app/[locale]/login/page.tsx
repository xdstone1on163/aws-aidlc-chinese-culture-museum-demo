'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const t = useTranslations('auth');
  const tc = useTranslations('common');
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const err = await login(email, password, rememberMe);
    if (err) setError(err);
    else router.push('/');
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6">{tc('login')}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input type="email" value={email} onChange={e => setEmail(e.target.value)}
          placeholder={t('email')} required className="w-full border rounded px-4 py-2" />
        <input type="password" value={password} onChange={e => setPassword(e.target.value)}
          placeholder={t('password')} required className="w-full border rounded px-4 py-2" />
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={rememberMe} onChange={e => setRememberMe(e.target.checked)} />
          {t('rememberMe')}
        </label>
        <button type="submit" className="w-full bg-primary text-white py-2 rounded hover:bg-primary-dark">
          {tc('login')}
        </button>
      </form>
    </div>
  );
}
