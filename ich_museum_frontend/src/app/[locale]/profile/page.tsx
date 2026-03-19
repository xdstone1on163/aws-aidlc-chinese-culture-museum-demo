'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';

export default function ProfilePage() {
  const tc = useTranslations('common');
  const { state, refreshUser } = useAuth();
  const user = state.user;
  const [nickname, setNickname] = useState(user?.nickname || '');
  const [bio, setBio] = useState('');
  const [message, setMessage] = useState('');

  if (!user) return <p className="text-center py-10">请先登录</p>;

  const handleSave = async () => {
    const res = await api.put('/accounts/me/profile/', { nickname, bio });
    if (res.code === 200) {
      setMessage('保存成功');
      refreshUser();
    } else {
      setMessage(res.message);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6">{tc('profile')}</h1>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">邮箱</label>
          <input value={user.email} disabled className="w-full border rounded px-4 py-2 bg-gray-100" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">昵称</label>
          <input value={nickname} onChange={e => setNickname(e.target.value)}
            className="w-full border rounded px-4 py-2" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">个人简介</label>
          <textarea value={bio} onChange={e => setBio(e.target.value)}
            maxLength={200} className="w-full border rounded px-4 py-2" rows={3} />
        </div>
        {message && <p className="text-sm text-green-600">{message}</p>}
        <button onClick={handleSave} className="bg-primary text-white px-6 py-2 rounded hover:bg-primary-dark">
          {tc('save')}
        </button>
      </div>
    </div>
  );
}
