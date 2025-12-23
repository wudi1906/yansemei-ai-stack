/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import axios from 'axios';

// 数据库连接类型定义
export interface DBConnection {
  id: number;
  name: string;
  db_type: string;
  host: string;
  port: number;
  username: string;
  database_name: string;
  created_at: string;
  updated_at: string;
}
// TODO  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWa3RxYkE9PToxYzY0MTZhYQ==

// API基础URL配置
const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWa3RxYkE9PToxYzY0MTZhYQ==

// 数据库连接相关API
export const getConnections = () => api.get<DBConnection[]>('/connections');

export default api;