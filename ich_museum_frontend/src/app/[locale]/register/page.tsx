'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/routing';
import { api } from '@/lib/api';

export default function RegisterPage() {
  const t = useTranslations('auth');
  const tc = useTranslations('common');
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '', confirm_password: '', nickname: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const res = await api.post('/accounts/register/', form);
    if (res.code === 201) router.push('/login');
    else setError(res.message);
  };

  const update = (field: string, value: string) => setForm(prev => ({ ...prev, [field]: value }));

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6">{tc('register')}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <input type="email" value={form.email} onChange={e => update('email', e.target.value)}
          placeholder={t('email')} required className="w-full border rounded px-4 py-2" />
        <input value={form.nickname} onChange={e => update('nickname', e.target.value)}
          placeholder={t('nickname')} required className="w-full border rounded px-4 py-2" />
        <input type="password" value={form.password} onChange={e => update('password', e.target.value)}
          placeholder={t('password')} required className="w-full border rounded px-4 py-2" />
        <input type="password" value={form.confirm_password} onChange={e => update('confirm_password', e.target.value)}
          placeholder={t('confirmPassword')} required className="w-full border rounded px-4 py-2" />
        <button type="submit" className="w-full bg-primary text-white py-2 rounded hover:bg-primary-dark">
          {tc('register')}
        </button>
      </form>
    </div>
  );
}
