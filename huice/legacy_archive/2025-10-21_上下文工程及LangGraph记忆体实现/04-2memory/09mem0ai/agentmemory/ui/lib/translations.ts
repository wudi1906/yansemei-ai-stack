// 中文翻译文件
export const translations = {
  // 导航栏
  nav: {
    appName: "智能记忆体",
    dashboard: "仪表板",
    memories: "记忆",
    apps: "应用",
    settings: "设置",
    refresh: "刷新",
    createMemory: "创建记忆"
  },

  // 页面标题和元数据
  meta: {
    title: "智能记忆体 - 开发者仪表板",
    description: "管理您的智能记忆体集成和存储的记忆"
  },

  // 仪表板页面
  dashboard: {
    installTitle: "安装智能记忆体",
    memoriesStats: "记忆统计",
    totalMemories: "总记忆数",
    totalAppsConnected: "已连接应用总数",
    memories: "记忆",
    apps: "应用",
    mcpLink: "MCP 链接",
    installationCommand: "安装命令"
  },

  // 记忆页面
  memories: {
    searchPlaceholder: "搜索记忆...",
    clearFilters: "清除过滤器",
    memory: "记忆",
    appName: "应用名称",
    createdOn: "创建时间",
    categories: "分类",
    source: "来源",
    actions: "操作",
    showing: "显示",
    to: "到",
    of: "共",
    page: "页",
    noMemoriesFound: "未找到记忆",
    noMemoriesDescription: "开始创建您的第一个记忆",
    createFirstMemory: "创建第一个记忆",
    paused: "已暂停",
    archived: "已归档",
    disabled: "已禁用",
    thisMemoryIs: "此记忆已",
    and: "且"
  },

  // 应用页面
  apps: {
    memoriesCreated: "已创建记忆",
    memoriesAccessed: "已访问记忆",
    active: "活跃",
    inactive: "非活跃",
    viewDetails: "查看详情",
    noAppsFound: "未找到匹配过滤条件的应用",
    created: "已创建",
    accessed: "已访问",
    noAccessedMemories: "未找到已访问的记忆"
  },

  // 设置页面
  settings: {
    title: "设置",
    description: "管理您的智能记忆体和 Mem0 配置",
    resetDefaults: "重置默认值",
    save: "保存",
    formView: "表单视图",
    jsonEditor: "JSON 编辑器",
    jsonConfiguration: "JSON 配置",
    jsonDescription: "直接以 JSON 格式编辑完整配置",
    resetConfirmTitle: "重置配置",
    resetConfirmDescription: "您确定要将所有设置重置为默认值吗？此操作无法撤销。",
    cancel: "取消",
    resetConfirm: "重置",
    saveSuccess: "配置保存成功",
    saveError: "保存配置失败",
    loadError: "加载配置失败",
    resetSuccess: "配置重置成功",
    resetError: "重置配置失败"
  },

  // 对话框
  dialogs: {
    createMemoryTitle: "创建新记忆",
    createMemoryDescription: "向您的智能记忆体实例添加新记忆",
    memoryLabel: "记忆",
    memoryPlaceholder: "例如：住在旧金山",
    saveMemory: "保存记忆",
    memoryCreatedSuccess: "记忆创建成功",
    memoryCreatedError: "创建记忆失败",
    updateMemoryTitle: "更新记忆",
    updateMemoryDescription: "编辑现有记忆内容",
    updateMemory: "更新记忆",
    memoryUpdatedSuccess: "记忆更新成功",
    memoryUpdatedError: "更新记忆失败"
  },

  // 错误页面
  errors: {
    pageNotFound: "页面未找到",
    goHome: "返回首页",
    memoryNotFound: "记忆未找到",
    error: "错误"
  },

  // 通用
  common: {
    loading: "加载中...",
    search: "搜索",
    filter: "过滤",
    sort: "排序",
    ascending: "升序",
    descending: "降序",
    all: "全部",
    active: "活跃",
    inactive: "非活跃",
    yes: "是",
    no: "否",
    ok: "确定",
    close: "关闭",
    delete: "删除",
    edit: "编辑",
    view: "查看",
    create: "创建",
    update: "更新",
    save: "保存",
    cancel: "取消"
  },

  // 过滤器
  filters: {
    filterBy: "过滤条件",
    sortBy: "排序方式",
    showArchived: "显示已归档",
    selectAll: "全选",
    clearAll: "清除全部",
    applyFilters: "应用过滤器",
    categories: "分类",
    apps: "应用"
  },

  // 表格列标题
  columns: {
    memory: "记忆",
    appName: "应用名称",
    createdOn: "创建时间"
  }
};

// 获取翻译文本的工具函数
export function t(key: string): string {
  const keys = key.split('.');
  let value: any = translations;
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = value[k];
    } else {
      console.warn(`Translation key not found: ${key}`);
      return key; // 如果找不到翻译，返回原始key
    }
  }
  
  return typeof value === 'string' ? value : key;
}

// 导出默认翻译函数
export default t;