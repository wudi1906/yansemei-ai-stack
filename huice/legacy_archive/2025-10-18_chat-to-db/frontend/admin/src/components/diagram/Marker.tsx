/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC80OmFIVnBZMlhsa0xUb3Y2bzZTVFptZVE9PTpiNjNhOTM2ZA==

import React from 'react';

// 关系类型常量
const RELATIONSHIP_TYPES = {
  ONE_TO_ONE: '1-to-1',
  ONE_TO_MANY: '1-to-N',
  MANY_TO_ONE: 'N-to-1',  // 添加多对一关系类型
  MANY_TO_MANY: 'N-to-M'
};
// NOTE  MS80OmFIVnBZMlhsa0xUb3Y2bzZTVFptZVE9PTpiNjNhOTM2ZA==

// 关系类型对应的颜色
const RELATIONSHIP_TYPE_COLORS = {
  [RELATIONSHIP_TYPES.ONE_TO_ONE]: '#8b5cf6', // 紫色
  [RELATIONSHIP_TYPES.ONE_TO_MANY]: '#0ea5e9', // 蓝色
  [RELATIONSHIP_TYPES.MANY_TO_ONE]: '#10b981', // 绿色
  [RELATIONSHIP_TYPES.MANY_TO_MANY]: '#f59e0b', // 橙色
};
// FIXME  Mi80OmFIVnBZMlhsa0xUb3Y2bzZTVFptZVE9PTpiNjNhOTM2ZA==

// 标记组件 - 用于显示关系的端点标记
const Marker = () => {
  return (
    <svg style={{ position: 'absolute', top: 0, left: 0 }}>
      <defs>
        {/* 一对一关系的起点标记 */}
        <marker
          id="one-to-one-start"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_ONE]} strokeWidth="1" />
          <line x1="2" y1="5" x2="8" y2="5" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_ONE]} strokeWidth="1.5" />
        </marker>

        {/* 一对一关系的终点标记 */}
        <marker
          id="one-to-one-end"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_ONE]} strokeWidth="1" />
          <line x1="2" y1="5" x2="8" y2="5" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_ONE]} strokeWidth="1.5" />
        </marker>

        {/* 一对多关系的"一"端标记 */}
        <marker
          id="one-to-many-start"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_MANY]} strokeWidth="1" />
          <line x1="2" y1="5" x2="8" y2="5" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_MANY]} strokeWidth="1.5" />
        </marker>

        {/* 一对多关系的"多"端标记 */}
        <marker
          id="one-to-many-end"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_MANY]} strokeWidth="1" />
          <path d="M2,3 L8,3 M2,5 L8,5 M2,7 L8,7" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.ONE_TO_MANY]} strokeWidth="1.5" fill="none" />
        </marker>

        {/* 多对一关系的“多”端标记 */}
        <marker
          id="many-to-one-start"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_ONE]} strokeWidth="1" />
          <path d="M2,3 L8,3 M2,5 L8,5 M2,7 L8,7" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_ONE]} strokeWidth="1.5" fill="none" />
        </marker>

        {/* 多对一关系的“一”端标记 */}
        <marker
          id="many-to-one-end"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_ONE]} strokeWidth="1" />
          <line x1="2" y1="5" x2="8" y2="5" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_ONE]} strokeWidth="1.5" />
        </marker>

        {/* 多对多关系的起点标记 */}
        <marker
          id="many-to-many-start"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_MANY]} strokeWidth="1" />
          <path d="M2,3 L8,3 M2,5 L8,5 M2,7 L8,7" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_MANY]} strokeWidth="1.5" fill="none" />
        </marker>

        {/* 多对多关系的终点标记 */}
        <marker
          id="many-to-many-end"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="8"
          markerHeight="8"
          orient="auto-start-reverse"
        >
          <circle cx="5" cy="5" r="4" fill="white" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_MANY]} strokeWidth="1" />
          <path d="M2,3 L8,3 M2,5 L8,5 M2,7 L8,7" stroke={RELATIONSHIP_TYPE_COLORS[RELATIONSHIP_TYPES.MANY_TO_MANY]} strokeWidth="1.5" fill="none" />
        </marker>
      </defs>
    </svg>
  );
};
// eslint-disable  My80OmFIVnBZMlhsa0xUb3Y2bzZTVFptZVE9PTpiNjNhOTM2ZA==

export default Marker;