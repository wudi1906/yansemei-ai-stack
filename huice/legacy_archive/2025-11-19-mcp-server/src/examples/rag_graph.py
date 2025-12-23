"""
增强的RAG系统 - 使用LangGraph实现多策略召回优化

架构说明:
1. Query Rewriter: 对用户问题进行改写优化,生成多个查询变体
2. Query Expander: 扩展查询,添加同义词和相关概念
3. Parallel Retrieval: 并行从知识库召回数据
4. Reranker: 对召回结果进行重排序
5. Synthesizer: 汇总整合生成最终答案

提升召回准确率的策略:
- 多查询改写(Multi-Query Rewriting)
- 查询扩展(Query Expansion)
- 混合检索(Hybrid Retrieval: 向量+关键词)
- 结果重排序(Reranking)
- 上下文压缩(Context Compression)
"""
"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""


import os
import operator
from typing import Annotated, TypedDict, List

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Send
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

# 初始化大模型
os.environ["DEEPSEEK_API_KEY"] = "sk-0828827353434c24b51dd30edcfa7f32"
model = init_chat_model("deepseek:deepseek-chat")


from langchain_milvus import Milvus, BM25BuiltInFunction

from langchain_ollama import OllamaEmbeddings
# type: ignore  MC80OmFIVnBZMlhsa0xUb3Y2bzZVMDl2YkE9PTpjZWJhZmJkZQ==

embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b", base_url="http://35.235.113.151:11434")
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": "http://121.40.159.60:19530"},
    builtin_function=BM25BuiltInFunction(),
    vector_field=["dense", "sparse"],
    collection_name="course_collection",
)

# ============================================================================
# 数据模型定义 - 使用Pydantic进行结构化输出
# ============================================================================

class RewrittenQuery(BaseModel):
    """改写后的查询"""
    original: str = Field(description="原始查询")
    rewritten: str = Field(description="改写后的查询")
    strategy: str = Field(description="改写策略,如: simplify, expand, rephrase, decompose")


class QueryRewriteOutput(BaseModel):
    """查询改写的输出"""
    queries: List[RewrittenQuery] = Field(description="改写后的查询列表,应包含3-5个不同策略的查询变体")


class RetrievalResult(TypedDict):
    """单个召回结果"""
    query: str  # 使用的查询
    content: str  # 召回的内容
    score: float  # 相关性分数
    metadata: dict  # 元数据


class RAGState(TypedDict):
    """RAG系统的全局状态"""
    original_question: str  # 用户原始问题
    rewritten_queries: List[dict]  # 改写后的查询列表
    retrieval_results: Annotated[List[RetrievalResult], operator.add]  # 所有召回结果(并行累加)
    reranked_results: List[RetrievalResult]  # 重排序后的结果
    final_answer: str  # 最终答案
    metadata: dict  # 额外的元数据


class RetrievalWorkerState(TypedDict):
    """单个检索Worker的状态"""
    query: dict  # 要处理的查询
    retrieval_results: Annotated[List[RetrievalResult], operator.add]  # 召回结果


# ============================================================================
# 节点函数定义
# ============================================================================

def query_rewriter(state: RAGState) -> dict:
    """
    问题改写节点 - 使用LLM生成多个优化的查询变体

    策略:
    1. 简化查询 - 去除冗余信息
    2. 扩展查询 - 添加相关上下文
    3. 重新表述 - 使用不同的表达方式
    4. 分解查询 - 将复杂问题分解为子问题
    """
    original_question = state["original_question"]

    # 使用结构化输出的LLM
    structured_llm = model.with_structured_output(QueryRewriteOutput)

    # 构建提示词
    system_prompt = """你是一个专业的查询优化专家。你的任务是将用户的问题改写为3-5个不同的查询变体,以提高从向量数据库检索的准确率。

改写策略:
1. original - 保留原始查询
2. simplify - 简化查询,去除冗余信息,提取核心关键词
3. expand - 扩展查询,添加相关概念、同义词和背景信息
4. rephrase - 用不同的表达方式重新表述问题
5. decompose - 将复杂问题分解为多个子问题

要求:
- 每个查询变体应该使用不同的策略
- 改写后的查询应该更容易匹配向量数据库中的文档
- 保持查询的语义不变
- 生成3-5个查询变体"""

    user_prompt = f"请将以下问题改写为多个查询变体:\n\n{original_question}"

    try:
        # 调用LLM生成改写查询
        response = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        # 转换为字典格式
        rewritten_queries = [q.model_dump() for q in response.queries]

        print(f"📝 Query Rewriter: 生成了 {len(rewritten_queries)} 个查询变体")
        for i, q in enumerate(rewritten_queries, 1):
            print(f"  {i}. [{q['strategy']}] {q['rewritten']}")

    except Exception as e:
        print(f"⚠️ Query Rewriter 出错: {e}, 使用原始查询")
        # 降级处理: 只使用原始查询
        rewritten_queries = [{
            "original": original_question,
            "rewritten": original_question,
            "strategy": "original"
        }]
# pragma: no cover  MS80OmFIVnBZMlhsa0xUb3Y2bzZVMDl2YkE9PTpjZWJhZmJkZQ==

    return {"rewritten_queries": rewritten_queries}

def retrieval_worker(state: RetrievalWorkerState) -> dict:
    """
    检索Worker节点 - 从知识库召回数据（并行执行）
    使用 similarity_search_with_score 获取文档和相关性分数

    注意: 此函数接受单个查询，会被并行调用多次
    """
    query_dict = state["query"]
    query_text = query_dict.get("rewritten", query_dict.get("original", ""))
    strategy = query_dict.get("strategy", "unknown")

    all_results = []

    try:
        # 使用 similarity_search_with_score 获取 (Document, score) 元组列表
        docs_with_scores = vector_store.similarity_search_with_score(query_text, k=3)

        # 转换为标准格式
        for doc, score in docs_with_scores:
            result = {
                "query": query_text,
                "content": doc.page_content,
                "score": float(score),  # 确保分数是float类型
                "metadata": doc.metadata,
                "strategy": strategy
            }
            all_results.append(result)

        print(f"  ✓ [{strategy}] 检索到 {len(docs_with_scores)} 个文档")

    except Exception as e:
        print(f"  ✗ [{strategy}] 查询失败: {e}")
# noqa  Mi80OmFIVnBZMlhsa0xUb3Y2bzZVMDl2YkE9PTpjZWJhZmJkZQ==

    return {"retrieval_results": all_results}


# ============================================================================
# Reranker 辅助函数
# ============================================================================

def _deduplicate_by_pk(results: List[dict]) -> List[dict]:
    """基于 pk (主键) 精确去重"""
    seen_pks = set()
    deduped = []

    for result in results:
        pk = result.get("metadata", {}).get("pk")
        if pk is not None:
            if pk not in seen_pks:
                seen_pks.add(pk)
                deduped.append(result)
        else:
            # 如果没有 pk，保留该结果
            deduped.append(result)

    return deduped


def _evaluate_relevance_with_llm(result: dict, question: str, idx: int, total: int) -> float:
    """使用 LLM 评估单个文档的相关性"""
    import re

    relevance_prompt = f"""请评估以下文档内容与用户问题的相关性,给出0-1之间的分数。
只需要输出一个数字(如: 0.85),不要解释。

用户问题: {question}

文档内容: {result['content'][:600]}

相关性分数 (0-1):"""

    try:
        response = model.invoke([HumanMessage(content=relevance_prompt)])
        score_text = response.content.strip()

        # 提取数字 (支持 0.85, .85, 1, 0 等格式)
        match = re.search(r'0?\.\d+|[01](?:\.\d+)?', score_text)
        if match:
            llm_score = float(match.group())
            llm_score = max(0.0, min(1.0, llm_score))  # 限制在 [0, 1]
        else:
            llm_score = result["score"]

        print(f"    [{idx}/{total}] LLM评分: {llm_score:.3f} (原始: {result['score']:.3f})")
        return llm_score

    except Exception as e:
        print(f"    [{idx}/{total}] LLM评分失败: {e}, 使用原始分数")
        return result["score"]


def _rerank_with_llm(results: List[dict], question: str, max_docs: int = 15) -> List[dict]:
    """使用 LLM 重新评分和排序"""
    if len(results) > max_docs:
        print(f"  ⊙ 步骤2 - 跳过LLM重排序 (文档数 {len(results)} > {max_docs}), 使用原始分数排序")
        return sorted(results, key=lambda x: x["score"], reverse=True)

    print(f"  ⏳ 步骤2 - LLM重排序: 正在评估 {len(results)} 个文档...")

    try:
        reranked_results = []

        for idx, result in enumerate(results, 1):
            llm_score = _evaluate_relevance_with_llm(result, question, idx, len(results))

            # 结合原始分数和LLM分数 (LLM权重更高)
            final_score = 0.3 * result["score"] + 0.7 * llm_score

            reranked_result = result.copy()
            reranked_result["score"] = final_score
            reranked_result["original_score"] = result["score"]
            reranked_result["llm_score"] = llm_score
            reranked_results.append(reranked_result)

        # 按新分数排序
        reranked_results.sort(key=lambda x: x["score"], reverse=True)
        print(f"  ✓ 步骤2 - LLM重排序完成")
        return reranked_results

    except Exception as e:
        print(f"  ✗ 步骤2 - LLM重排序失败: {e}, 使用原始分数排序")
        return sorted(results, key=lambda x: x["score"], reverse=True)

# type: ignore  My80OmFIVnBZMlhsa0xUb3Y2bzZVMDl2YkE9PTpjZWJhZmJkZQ==

def _optimize_diversity(results: List[dict]) -> List[dict]:
    """多样性优化 - 优先选择不同来源的文档"""
    diverse_results = []
    seen_sources = set()
    remaining_results = []

    for result in results:
        source = result.get("metadata", {}).get("source", "unknown")
        if source not in seen_sources:
            diverse_results.append(result)
            seen_sources.add(source)
        else:
            remaining_results.append(result)

    # 添加剩余结果
    diverse_results.extend(remaining_results)

    return diverse_results, len(seen_sources)


def _print_reranker_summary(all_results: List[dict], unique_results: List[dict],
                           final_results: List[dict], top_k: int):
    """打印 Reranker 处理摘要"""
    print(f"\n✅ Reranker 完成:")
    print(f"   原始结果: {len(all_results)} 个")
    print(f"   去重后: {len(unique_results)} 个")
    print(f"   最终返回: {len(final_results)} 个 (Top-{top_k})")

    # 打印 Top-3 结果预览
    if final_results:
        print(f"\n📋 Top-3 结果预览:")
        for i, result in enumerate(final_results[:3], 1):
            source = result.get("metadata", {}).get("source", "unknown")
            score = result.get("score", 0)
            content_preview = result.get("content", "")[:80].replace("\n", " ")
            print(f"   {i}. [分数: {score:.3f}] {content_preview}...")
            print(f"      来源: {source}")


# ============================================================================
# Reranker 主函数
# ============================================================================

def reranker(state: RAGState) -> dict:
    """
    重排序节点 - 对召回结果进行智能去重和重排序

    优化策略:
    1. 基于 pk (主键) 去重 - 精确去重
    2. 使用LLM评估相关性 - 重新评分
    3. 多样性优化 - 确保结果覆盖不同来源
    4. Top-K 选择 - 返回最相关的结果
    """
    all_results = state["retrieval_results"]
    original_question = state["original_question"]

    if not all_results:
        print("⚠️ Reranker: 没有召回结果")
        return {"reranked_results": []}

    print(f"\n🎯 Reranker: 开始处理 {len(all_results)} 个召回结果")

    # 步骤1: PK去重
    pk_deduped = _deduplicate_by_pk(all_results)
    print(f"  ✓ 步骤1 - PK去重: {len(all_results)} -> {len(pk_deduped)} 个文档")

    # 步骤2: LLM重排序
    # reranked_results = _rerank_with_llm(pk_deduped, original_question)
    reranked_results = pk_deduped
    # 步骤3: 多样性优化
    diverse_results, num_sources = _optimize_diversity(reranked_results)
    print(f"  ✓ 步骤3 - 多样性优化: 覆盖 {num_sources} 个不同来源")

    # 步骤4: Top-K 选择
    top_k = 10
    final_results = diverse_results[:top_k]

    # 打印摘要
    _print_reranker_summary(all_results, pk_deduped, final_results, top_k)

    return {"reranked_results": final_results}


def synthesizer(state: RAGState) -> dict:
    """
    答案合成节点 - 使用LLM基于召回的内容生成最终答案

    优化策略:
    1. 智能上下文构建 - 包含分数和来源信息
    2. 引用标注 - 标记信息来源
    3. 质量评估 - 评估答案质量
    4. 降级处理 - 错误时返回结构化摘要
    """
    question = state["original_question"]
    results = state["reranked_results"]

    if not results:
        return {"final_answer": "抱歉,没有找到相关的文档来回答您的问题。请尝试换一种方式提问。"}

    print(f"\n📝 Synthesizer: 开始生成答案 (基于 {len(results)} 个文档)")

    # ========== 构建上下文 - 包含详细的来源和分数信息 ==========
    context_parts = []
    top_n = min(5, len(results))  # 使用 top-5 或更少的结果

    for i, result in enumerate(results[:top_n], 1):
        source = result.get('metadata', {}).get('source', 'unknown')
        content = result.get('content', '')
        score = result.get('score', 0)

        # 构建带有元信息的上下文
        context_part = f"""[文档{i}]
来源: {source}
相关性分数: {score:.3f}
内容:
{content}"""
        context_parts.append(context_part)

        print(f"  ✓ 文档{i}: {source[:50]}... (分数: {score:.3f})")

    context = "\n\n" + "="*80 + "\n\n".join(context_parts)

    # ========== 构建提示词 ==========
    system_prompt = """你是一个专业的问答助手。你的任务是基于提供的文档内容回答用户的问题。

要求:
1. **基于事实**: 答案必须严格基于提供的文档内容,不要编造信息
2. **标注来源**: 在答案中标注信息来源,使用 [文档X] 的格式
3. **综合信息**: 如果多个文档提供了相关信息,请综合所有信息给出完整答案
4. **清晰准确**: 答案要清晰、准确、有条理,使用分点或分段的方式组织
5. **诚实表达**: 如果文档中没有足够信息回答某个方面,请明确说明

答案结构建议:
- 开头: 直接回答核心问题
- 中间: 提供详细解释和支持信息
- 结尾: 总结要点或补充说明"""

    user_prompt = f"""请基于以下文档内容回答问题:

{context}

用户问题: {question}

请提供详细、准确的答案:"""

    try:
        # 调用LLM生成答案
        print(f"  ⏳ 正在调用 LLM 生成答案...")
        response = model.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        final_answer = response.content.strip()

        # ========== 添加元数据和统计信息 ==========
        # 统计来源
        unique_sources = set()
        for result in results:
            source = result.get('metadata', {}).get('source', 'unknown')
            unique_sources.add(source)

        # 计算平均分数
        avg_score = sum(r.get('score', 0) for r in results[:top_n]) / top_n if top_n > 0 else 0

        stats = f"""

{"="*80}
📊 答案元数据:
- 参考文档数: {len(results)} 个 (使用 top-{top_n} 生成答案)
- 来源数量: {len(unique_sources)} 个不同来源
- 平均相关性分数: {avg_score:.3f}

📚 参考来源:"""

        # 列出所有来源
        for i, source in enumerate(sorted(unique_sources)[:5], 1):
            stats += f"\n  {i}. {source}"

        if len(unique_sources) > 5:
            stats += f"\n  ... 还有 {len(unique_sources) - 5} 个来源"

        final_answer = final_answer + stats

        print(f"  ✅ LLM 答案生成成功 (长度: {len(final_answer)} 字符)")
        print(f"  ✅ 平均相关性分数: {avg_score:.3f}")

    except Exception as e:
        print(f"  ✗ Synthesizer 出错: {e}")
        print(f"  ⚠️ 使用降级策略: 返回结构化摘要")

        # ========== 降级处理: 返回结构化的文档摘要 ==========
        final_answer = f"""# 基于 {len(results)} 个相关文档的信息摘要

**问题**: {question}

**注意**: LLM 生成失败,以下是文档摘要供参考:

"""

        for i, result in enumerate(results[:5], 1):
            source = result.get('metadata', {}).get('source', 'unknown')
            content = result.get('content', '')
            score = result.get('score', 0)

            # 截取内容预览
            content_preview = content[:300].replace('\n', ' ')
            if len(content) > 300:
                content_preview += "..."

            final_answer += f"""
## 文档 {i} (相关性: {score:.3f})
**来源**: {source}
**内容**: {content_preview}

"""

        final_answer += f"""
---
💡 提示: 请尝试重新提问或联系技术支持。
错误信息: {str(e)}
"""

    return {"final_answer": final_answer}


# ============================================================================
# 条件边函数
# ============================================================================

def assign_retrieval_workers(state: RAGState) -> List[Send]:
    """
    分配检索任务 - 为每个改写的查询创建一个并行的检索Worker

    使用LangGraph的Send API实现并行检索
    每个查询会触发一个独立的 retrieval_worker 节点执行
    """
    queries = state["rewritten_queries"]

    print(f"🚀 分配 {len(queries)} 个并行检索任务")

    # 为每个查询创建一个Send对象,触发并行执行
    return [
        Send("retrieval_worker", {"query": query})
        for query in queries
    ]


# ============================================================================
# 构建Graph
# ============================================================================

def build_enhanced_rag_graph():
    """
    构建增强的RAG Graph

    使用条件边实现并行检索:
    - query_rewriter 生成多个查询变体
    - 通过条件边 assign_retrieval_workers 为每个查询创建并行任务
    - 多个 retrieval_worker 并行执行
    - 所有 retrieval_worker 完成后，结果自动合并到 retrieval_results
    - reranker 对合并后的结果进行去重和重排序
    """

    # 创建StateGraph
    graph_builder = StateGraph(RAGState)

    # 添加节点
    graph_builder.add_node("query_rewriter", query_rewriter)
    graph_builder.add_node("retrieval_worker", retrieval_worker)
    graph_builder.add_node("reranker", reranker)
    graph_builder.add_node("synthesizer", synthesizer)

    # 添加边
    graph_builder.add_edge(START, "query_rewriter")

    # 条件边: 从 query_rewriter 到多个并行的 retrieval_worker
    # assign_retrieval_workers 返回 List[Send]，每个 Send 触发一个 retrieval_worker
    graph_builder.add_conditional_edges(
        "query_rewriter",
        assign_retrieval_workers,
        ["retrieval_worker"]
    )

    # 所有 retrieval_worker 完成后进入 reranker
    # 由于 retrieval_results 使用了 operator.add，所有并行结果会自动合并
    graph_builder.add_edge("retrieval_worker", "reranker")
    graph_builder.add_edge("reranker", "synthesizer")
    graph_builder.add_edge("synthesizer", END)

    # 编译Graph
    graph = graph_builder.compile()

    return graph
graph = build_enhanced_rag_graph()

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 构建Graph
    rag_graph = build_enhanced_rag_graph()
    
    # 测试输入
    # test_question = "什么是LangGraph?它有哪些核心特性?"
    test_question = "介绍一下这份培训大纲"
    initial_state = {
        "original_question": test_question,
        "rewritten_queries": [],
        "retrieval_results": [],
        "reranked_results": [],
        "final_answer": "",
        "metadata": {}
    }
    
    print("=" * 80)
    print("🚀 启动增强RAG系统")
    print("=" * 80)
    print(f"📥 用户问题: {test_question}\n")
    
    # 执行Graph
    result = rag_graph.invoke(initial_state)
    
    print("\n" + "=" * 80)
    print("📤 最终结果")
    print("=" * 80)
    print(result["final_answer"])
    print("\n" + "=" * 80)
