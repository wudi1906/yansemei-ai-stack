/**
 * 获取保存在 localStorage 里的 API Key。
 *
 * - 只在浏览器环境下访问 window.localStorage
 * - 服务端渲染阶段（typeof window === "undefined"）返回 null
 */
export function getApiKey(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    return window.localStorage.getItem("lg:chat:apiKey");
  } catch {
    return null;
  }
}
