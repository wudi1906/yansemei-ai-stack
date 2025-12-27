/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 * 
 * 简单的登录保护组件 - 瓶口验证模式
 * 验证成功后设置 Cookie，后续访问自动通过
 */

"use client";

import React, { useState, useEffect, ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LangGraphLogoSVG } from "@/components/icons/langgraph";

// 配置：用户名和密码（生产环境建议使用环境变量）
const AUTH_CONFIG = {
  username: "wudi1906",
  password: "wudi123456",
  cookieName: "aurora_auth",
  cookieMaxAge: 7 * 24 * 60 * 60, // 7天
};

function setCookie(name: string, value: string, maxAge: number) {
  document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Strict`;
}

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

function generateAuthToken(username: string): string {
  // 简单的 token 生成（生产环境建议使用更安全的方式）
  const timestamp = Date.now();
  const data = `${username}:${timestamp}:aurora_secret_2025`;
  return btoa(data);
}

function validateAuthToken(token: string): boolean {
  try {
    const decoded = atob(token);
    const parts = decoded.split(":");
    if (parts.length !== 3) return false;
    
    const timestamp = parseInt(parts[1], 10);
    const now = Date.now();
    const maxAge = AUTH_CONFIG.cookieMaxAge * 1000;
    
    // 检查 token 是否过期
    return now - timestamp < maxAge;
  } catch {
    return false;
  }
}

interface AuthGuardProps {
  children: ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // 检查是否已登录
    const token = getCookie(AUTH_CONFIG.cookieName);
    if (token && validateAuthToken(token)) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    // 模拟网络延迟
    await new Promise((resolve) => setTimeout(resolve, 500));

    if (username === AUTH_CONFIG.username && password === AUTH_CONFIG.password) {
      const token = generateAuthToken(username);
      setCookie(AUTH_CONFIG.cookieName, token, AUTH_CONFIG.cookieMaxAge);
      setIsAuthenticated(true);
    } else {
      setError("用户名或密码错误");
    }

    setIsLoading(false);
  };

  // 加载中状态
  if (isAuthenticated === null) {
    return (
      <div className="flex h-screen items-center justify-center bg-gradient-to-br from-violet-50 to-indigo-50">
        <div className="flex items-center gap-2">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-violet-600 border-t-transparent"></div>
          <span className="text-gray-600">加载中...</span>
        </div>
      </div>
    );
  }

  // 已登录，显示子组件
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // 未登录，显示登录页面
  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-violet-50 to-indigo-50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl shadow-violet-100/50">
        <div className="mb-8 flex flex-col items-center gap-3">
          <LangGraphLogoSVG className="h-12 w-12" />
          <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
            AuroraAI
          </h1>
          <p className="text-gray-500 text-sm">企业级智能助手平台</p>
        </div>

        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          <div className="flex flex-col gap-2">
            <Label htmlFor="username" className="text-gray-700">
              用户名
            </Label>
            <Input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="请输入用户名"
              className="h-11"
              required
              autoComplete="username"
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="password" className="text-gray-700">
              密码
            </Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="请输入密码"
              className="h-11"
              required
              autoComplete="current-password"
            />
          </div>

          {error && (
            <p className="text-sm text-red-500 bg-red-50 px-3 py-2 rounded-lg">
              {error}
            </p>
          )}

          <Button
            type="submit"
            className="h-11 mt-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                登录中...
              </span>
            ) : (
              "登录"
            )}
          </Button>
        </form>

        <p className="mt-6 text-center text-xs text-gray-400">
          © 2025 AuroraAI. All rights reserved.
        </p>
      </div>
    </div>
  );
}
