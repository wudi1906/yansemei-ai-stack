/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZjV0kxYmc9PTo1MzVlZjQzNg==

export function LangGraphLogoSVG({
  className,
  width,
  height,
}: {
  width?: number;
  height?: number;
  className?: string;
}) {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* 定义渐变 */}
      <defs>
        <linearGradient id="auroraGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: "#7c3aed", stopOpacity: 1 }} />
          <stop offset="50%" style={{ stopColor: "#8b5cf6", stopOpacity: 1 }} />
          <stop offset="100%" style={{ stopColor: "#6366f1", stopOpacity: 1 }} />
        </linearGradient>
        <linearGradient id="goldAccent" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: "#fbbf24", stopOpacity: 1 }} />
          <stop offset="100%" style={{ stopColor: "#f59e0b", stopOpacity: 1 }} />
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="1" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      {/* 主圆形背景 */}
      <circle
        cx="20"
        cy="20"
        r="18"
        fill="url(#auroraGradient)"
      />
      
      {/* 内圈装饰 */}
      <circle
        cx="20"
        cy="20"
        r="15"
        fill="none"
        stroke="rgba(255,255,255,0.2)"
        strokeWidth="0.5"
      />

      {/* Aurora 极光波浪效果 */}
      <path
        d="M8 22 Q14 16, 20 20 T32 18"
        stroke="url(#goldAccent)"
        strokeWidth="2"
        fill="none"
        strokeLinecap="round"
        filter="url(#glow)"
        opacity="0.9"
      />
      <path
        d="M10 26 Q16 20, 22 24 T34 22"
        stroke="rgba(255,255,255,0.5)"
        strokeWidth="1"
        fill="none"
        strokeLinecap="round"
        opacity="0.6"
      />

      {/* "A" 字母 */}
      <text
        x="20"
        y="25"
        fontFamily="'Inter', 'SF Pro Display', -apple-system, sans-serif"
        fontSize="16"
        fontWeight="700"
        fill="#ffffff"
        textAnchor="middle"
        letterSpacing="-0.5"
      >
        A
      </text>

      {/* 顶部光点 */}
      <circle cx="20" cy="6" r="1.5" fill="url(#goldAccent)" opacity="0.8" />
    </svg>
  );
}
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZjV0kxYmc9PTo1MzVlZjQzNg==