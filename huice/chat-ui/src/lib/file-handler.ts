/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 * 
 * File Handler - 处理文件上传到RAG Core
 * 
 * 这个模块解决了Gemini不支持file类型消息的问题：
 * 1. 拦截PDF文件上传
 * 2. 将PDF上传到RAG Core进行索引（使用Ollama处理）
 * 3. 转换为文本引用发送给Gemini
 * 4. 图片保持原样（Gemini支持image_url类型）
 */

import type { OptimizedContentBlock, FileContentBlock } from "./multimodal-utils";
import { toast } from "sonner";

// Next.js环境变量（必须以NEXT_PUBLIC_开头才能在客户端访问）
const RAG_CORE_URL = process.env.NEXT_PUBLIC_RAG_CORE_URL || "http://localhost:9621";

/**
 * 将PDF文件上传到RAG Core进行索引
 */
async function uploadPdfToRagCore(fileBlock: FileContentBlock): Promise<string> {
  try {
    console.log(`📤 Uploading PDF to RAG Core: ${fileBlock.metadata.filename}`);
    
    // 将base64转换为Blob
    const byteCharacters = atob(fileBlock.data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: fileBlock.mime_type });
    
    // 创建FormData
    const formData = new FormData();
    formData.append("file", blob, fileBlock.metadata.filename);
    
    // 显示上传提示
    toast.info(`正在上传文档: ${fileBlock.metadata.filename}...`);
    
    // 上传到RAG Core
    const response = await fetch(`${RAG_CORE_URL}/documents/upload`, {
      method: "POST",
      body: formData,
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Upload failed (${response.status}): ${errorText}`);
    }
    
    const result = await response.json();
    const docId = result.track_id || result.document_id || fileBlock.metadata.filename;
    
    console.log(`✅ PDF uploaded successfully: ${docId}`);
    toast.success(`文档已上传并开始索引: ${fileBlock.metadata.filename}`);
    
    return docId;
  } catch (error) {
    console.error("Failed to upload PDF to RAG Core:", error);
    toast.error(`文档上传失败: ${fileBlock.metadata.filename}`);
    throw error;
  }
}

/**
 * 处理消息内容块，将文件转换为合适的格式
 * 
 * 处理逻辑：
 * 1. PDF文件 → 上传到RAG Core → 转换为文本引用
 * 2. 图片文件 → 保持image_url格式（Gemini支持）
 * 3. 其他文件类型 → 上传到RAG Core → 转换为文本引用
 * 4. 文本/image_url → 保持原样
 */
export async function processContentBlocks(
  blocks: OptimizedContentBlock[]
): Promise<Array<{ type: string; text?: string; image_url?: any }>> {
  const processedBlocks: Array<{ type: string; text?: string; image_url?: any }> = [];
  
  for (const block of blocks) {
    // 处理文件类型
    if (block.type === "file") {
      const fileBlock = block as FileContentBlock;
      
      // 检查是否是图片（Gemini支持直接处理）
      if (fileBlock.mime_type?.startsWith("image/")) {
        // 图片：转换为image_url格式
        processedBlocks.push({
          type: "image_url",
          image_url: {
            url: `data:${fileBlock.mime_type};base64,${fileBlock.data}`,
          },
        });
      } else {
        // PDF或其他文档：上传到RAG Core
        try {
          const docId = await uploadPdfToRagCore(fileBlock);
          processedBlocks.push({
            type: "text",
            text: `[已上传文档: ${fileBlock.metadata.filename}，文档ID: ${docId}。请使用RAG工具查询此文档内容。]`,
          });
        } catch (error) {
          // 如果上传失败，添加错误提示
          processedBlocks.push({
            type: "text",
            text: `[文档上传失败: ${fileBlock.metadata.filename}]`,
          });
        }
      }
    } else if (block.type === "image_url") {
      // 已经是image_url格式，保持原样
      processedBlocks.push(block);
    } else if (block.type === "text") {
      // 文本，保持原样
      processedBlocks.push(block);
    }
    // 忽略其他未知类型
  }
  
  return processedBlocks;
}
