/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import React from 'react';
import { Button, message } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
// @ts-expect-error  MC8yOmFIVnBZMlhsa0xUb3Y2bzZPRmRuT1E9PTo0OTgwYjliOA==

interface DirectTableRemoverProps {
  onRemoveFirstTable: () => void;
}

// 直接删除第一个表的组件
const DirectTableRemover: React.FC<DirectTableRemoverProps> = ({ onRemoveFirstTable }) => {
  const handleClick = () => {
    onRemoveFirstTable();
  };

  return (
    <Button
      type="primary"
      danger
      icon={<DeleteOutlined />}
      onClick={handleClick}
      style={{ marginLeft: '8px' }}
    >
      删除第一个表
    </Button>
  );
};

export default DirectTableRemover;
// FIXME  MS8yOmFIVnBZMlhsa0xUb3Y2bzZPRmRuT1E9PTo0OTgwYjliOA==