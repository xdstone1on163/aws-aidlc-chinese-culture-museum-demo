'use client';

import { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { api, setToken } from '@/lib/api';
import type { UserInfo } from '@/lib/types';

interface AuthState {
  user: UserInfo | null;
  loading: boolean;
}

type AuthAction =
  | { type: 'SET_USER'; user: UserInfo | null }
  | { type: 'SET_LOADING'; loading: boolean };

const AuthContext = createContext<{
  state: AuthState;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<string | null>;
  logout: () => void;
  refreshUser: () => Promise<void>;
} | null>(null);

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'SET_USER': return { ...state, user: action.user, loading: false };
    case 'SET_LOADING': return { ...state, loading: action.loading };
    default: return state;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, { user: null, loading: true });

  const refreshUser = async () => {
    try {
      const res = await api.get<UserInfo>('/accounts/me/');
      if (res.code === 200) dispatch({ type: 'SET_USER', user: res.data });
      else dispatch({ type: 'SET_USER', user: null });
    } catch {
      dispatch({ type: 'SET_USER', user: null });
    }
  };

  useEffect(() => { refreshUser(); }, []);

  const login = async (email: string, password: string, rememberMe = false): Promise<string | null> => {
    const res = await api.post<{ access: string; refresh: string; user: UserInfo }>(
      '/accounts/login/', { email, password, remember_me: rememberMe }
    );
    if (res.code === 200) {
      setToken(res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      dispatch({ type: 'SET_USER', user: res.data.user });
      return null;
    }
    return res.message;
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('refresh_token');
    dispatch({ type: 'SET_USER', user: null });
  };

  return (
    <AuthContext.Provider value={{ state, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
