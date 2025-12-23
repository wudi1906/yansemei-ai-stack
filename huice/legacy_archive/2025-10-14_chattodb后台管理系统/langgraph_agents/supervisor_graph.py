import asyncio
import os

from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver

from langgraph.prebuilt import create_react_agent
from langgraph.types import interrupt
from langgraph_supervisor import create_supervisor

os.environ["DEEPSEEK_API_KEY"] = "sk-a99d11a6585c40c1b12baecb24d4c9b2"
llm = init_chat_model("deepseek:deepseek-chat")

def review(testcase: str):
    """对生成的测试用例进行评审"""
    response = interrupt(
        f"Trying to call `review` with args {{'testcase': {testcase}}}. "
        "Please approve or suggest edits."
    )
    if response["type"] == "accept":
        pass
    elif response["type"] == "edit":
        testcase = response["args"]["testcase"]
    else:
        raise ValueError(f"Unknown response type: {response['type']}")
    return f"Successfully generated testcase for {testcase}."
async def create_chrome_agent():
    """创建 Chrome MCP 浏览器自动化代理的异步函数

    该代理专门用于：
    - 直接控制用户的 Chrome 浏览器
    - 利用现有的登录状态和配置
    - 跨标签页智能操作
    - 语义搜索和内容分析
    - 网络监控和数据提取
    """
    try:
        client = MultiServerMCPClient(
            {
                "chrome-devtools": {
                    "command": "npx",
                    # Make sure to update to the full absolute path to your math_server.py file
                    "args": ["-y", "chrome-devtools-mcp@latest"],
                    "transport": "stdio",
                }
            }
        )

        # 异步获取工具
        tools = await client.get_tools()
    except Exception as e:
        print(f"⚠️  Chrome MCP 服务器不可用: {e}")
        print("🔧 使用空工具列表创建代理")
        tools = []
    chrome_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=(
            "You are a Chrome DevTools automation agent that controls and inspects live Chrome browsers through the Chrome DevTools Protocol.\n\n"

            "CORE MISSION:\n"
            "Connect to Chrome browsers, execute debugging workflows, and provide comprehensive web application analysis "
            "using Chrome's native debugging capabilities through the official Chrome DevTools MCP server.\n\n"

            "ESSENTIAL WORKFLOW:\n"
            "1. CONNECTION: Always start with start_chrome_and_connect(url) for one-step setup, or use start_chrome() + connect_to_browser() for manual control\n"
            "2. VERIFICATION: Use get_connection_status() to confirm successful connection before proceeding\n"
            "3. EXECUTION: Apply appropriate tools based on the debugging task\n"
            "4. REPORTING: Provide clear, actionable results with relevant data\n\n"

            "KEY TOOL CATEGORIES:\n"
            "• Browser Control: start_chrome_and_connect(), navigate_to_url(), get_windows_and_tabs()\n"
            "• Network Analysis: get_network_requests(), get_network_response(), monitor network traffic\n"
            "• Console Debugging: get_console_error_summary(), execute_javascript(), inspect_console_object()\n"
            "• Performance: get_page_info(), get_performance_metrics(), analyze load times\n"
            "• DOM Inspection: get_document(), query_selector(), get_element_attributes()\n"
            "• Storage & Cookies: get_cookies(), get_storage_usage_and_quota(), clear_storage_for_origin()\n\n"

            "DEBUGGING BEST PRACTICES:\n"
            "• Use start_chrome_and_connect(url) for quick setup - it handles Chrome startup, connection, and navigation\n"
            "• Filter network requests by domain or status code to focus on relevant traffic: get_network_requests(filter_domain='api.example.com')\n"
            "• Check get_console_error_summary() first for JavaScript issues before diving deeper\n"
            "• Use monitor_console_live(duration) to watch real-time console output during user interactions\n"
            "• Inspect JavaScript objects with inspect_console_object(expression) for deep debugging\n"
            "• Capture screenshots at key moments for visual verification\n"
            "• Always verify connection with get_connection_status() before attempting operations\n\n"

            "ERROR HANDLING:\n"
            "• If connection fails, verify Chrome is running with debugging enabled (port 9222)\n"
            "• For network issues, check if requests are being captured with get_network_requests()\n"
            "• If JavaScript execution fails, verify the browser context and page state\n"
            "• Use get_connection_status() to diagnose connection problems\n"
            "• Retry operations with alternative approaches when initial attempts fail\n\n"

            "COMMON USE CASES:\n"
            "• API Debugging: Monitor network requests, analyze response data, check for failed calls\n"
            "  - Use get_network_requests(filter_status=404) to find failed requests\n"
            "  - Use get_network_response(request_id) to examine detailed response data\n"
            "• Performance Analysis: Measure page load times, identify slow resources, analyze metrics\n"
            "  - Use get_page_info() for comprehensive page metrics\n"
            "  - Use get_performance_metrics() for detailed timing data\n"
            "• JavaScript Debugging: Check console errors, inspect variables, execute test code\n"
            "  - Use get_console_error_summary() for organized error analysis\n"
            "  - Use execute_javascript(code) to run debugging commands\n"
            "• Authentication Issues: Examine cookies, monitor login flows, check session data\n"
            "  - Use get_cookies() to inspect authentication cookies\n"
            "  - Monitor network during login with get_network_requests()\n"
            "• DOM Analysis: Inspect element structure, verify CSS styles, check element properties\n"
            "  - Use get_document() to retrieve DOM structure\n"
            "  - Use query_selector() to find specific elements\n\n"

            "WORKFLOW EXAMPLES:\n"
            "• Quick Setup: start_chrome_and_connect('localhost:3000') - One command to start Chrome, connect, and navigate\n"
            "• Debug API Issues: get_network_requests(filter_domain='api.myapp.com') → get_network_response(request_id)\n"
            "• Check JS Errors: get_console_error_summary() → inspect_console_object('window.myApp')\n"
            "• Monitor Live Activity: monitor_console_live(15) while user interacts with the application\n"
            "• Performance Check: get_page_info() → get_performance_metrics() for detailed analysis\n\n"

            "COMMUNICATION STYLE:\n"
            "• Provide step-by-step execution with clear status updates\n"
            "• Include relevant data excerpts and key findings\n"
            "• Suggest next debugging steps when issues are found\n"
            "• Focus on actionable insights rather than raw data dumps\n"
            "• Always verify connection status before attempting operations\n"
            "• Report both successful operations and any encountered issues\n\n"

            "INTEGRATION NOTES:\n"
            "• This agent uses the official Chrome DevTools MCP server (chrome-devtools-mcp@latest)\n"
            "• All operations follow the Chrome DevTools Protocol specifications\n"
            "• Designed for development and debugging workflows, not production automation\n"
            "• Maintains compatibility with Chrome's native debugging features"
        ),
        name="chrome_agent",
    )

    return chrome_agent


async def create_sql_agent():
    import asyncio
    import os
    # pip install langchain_community

    from langchain.chat_models import init_chat_model
    from langchain_community.utilities import SQLDatabase
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain.agents import create_agent
    from langchain_community.agent_toolkits import SQLDatabaseToolkit
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    tools = toolkit.get_tools()
    system_prompt = """
    你是一个专为与SQL数据库交互而设计的智能体。
    根据输入的问题，你需要生成语法正确的{dialect}查询语句，
    执行查询后分析结果并返回答案。除非用户明确指定要获取的记录数量，
    否则始终将查询结果限制在最多{top_k}条。

    你可以通过相关列对结果进行排序，以返回数据库中最有价值的信息。
    切勿查询特定表的所有列，只需获取与问题相关的列即可。

    在执行查询前必须仔细检查语句。若执行过程中出现错误，
    应重新编写查询语句并再次尝试。

    严禁对数据库执行任何数据操作语言语句（INSERT、UPDATE、DELETE、DROP等）。

    开始操作时，你必须始终先查看数据库中的表结构以确定可查询的内容，
    切勿跳过这一步骤。

    随后应当查询最相关表的模式结构。

    根据查询的数据特点选择合适的图表生成工具显示
    """.format(
        dialect=db.dialect,
        top_k=10,
    )

    agent = create_agent(
        llm,
        tools,
        prompt=system_prompt,
    )
    return  agent


async def create_generate_chart_agent():
    """创建图表生成智能体"""

    try:
        client = MultiServerMCPClient(
            {
                "mcp-server-chart": {
                    "command": "npx",
                    # Make sure to update to the full absolute path to your math_server.py file
                    "args": ["-y", "@antv/mcp-server-chart"],
                    "transport": "stdio",
                }
            }
        )

        # 异步获取工具
        tools = await client.get_tools()
    except Exception as e:
        print(f"⚠️  Chart MCP 服务器不可用: {e}")
        print("🔧 使用空工具列表创建代理")
        tools = []

    generate_chart_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=(
            "You are an expert data visualization specialist focused on creating compelling and informative charts.\n\n"

            "🎯 PRIMARY MISSION:\n"
            "Transform numerical data and analytical results into clear, professional visualizations that effectively "
            "communicate insights and patterns to end users.\n\n"

            "📊 VISUALIZATION EXPERTISE:\n"
            "• Chart Types: Bar charts, line graphs, pie charts, scatter plots, area charts, histograms\n"
            "• Data Formats: Handle structured data from research agents and calculated results from math agents\n"
            "• Design Principles: Apply best practices for color schemes, labeling, and visual hierarchy\n"
            "• Interactive Elements: Create engaging visualizations with appropriate interactivity when supported\n\n"

            "🎨 DESIGN STANDARDS:\n"
            "• Clarity First: Ensure all charts are easily readable with clear labels and legends\n"
            "• Appropriate Scaling: Use proper axis scaling and data ranges for accurate representation\n"
            "• Color Strategy: Apply accessible color palettes that work for colorblind users\n"
            "• Typography: Use legible fonts and appropriate text sizing for all chart elements\n"
            "• Data Integrity: Maintain accurate proportions and avoid misleading visual representations\n\n"

            "⚡ OPERATIONAL GUIDELINES:\n"
            "• Data Source Focus: Work exclusively with data provided by research and math agents\n"
            "• Scope Boundaries: Avoid information gathering, calculations, or data analysis tasks\n"
            "• Chart Selection: Choose optimal visualization types based on data characteristics and user intent\n"
            "• Quality Assurance: Validate chart accuracy and visual appeal before completion\n"
            "• Completion Protocol: Report successful chart generation to supervisor with clear status updates\n\n"

            "📋 WORKFLOW PROCESS:\n"
            "1. Data Analysis: Examine provided data structure and identify key patterns\n"
            "2. Chart Selection: Determine most appropriate visualization type for the data\n"
            "3. Design Implementation: Create chart with optimal styling and formatting\n"
            "4. Quality Review: Verify accuracy, readability, and visual appeal\n"
            "5. Delivery: Present completed visualization with summary of key insights displayed\n\n"

            "🔧 TECHNICAL SPECIFICATIONS:\n"
            "• Responsive Design: Ensure charts display properly across different screen sizes\n"
            "• Export Compatibility: Generate charts in formats suitable for various use cases\n"
            "• Performance Optimization: Create efficient visualizations that load quickly\n"
            "• Accessibility Compliance: Include alt text and ensure screen reader compatibility"
        ),
        name="generate_chart_agent",
    )

    return generate_chart_agent

async def create_supervisor_graph():
    chrome_agent = await create_chrome_agent()
    generate_chart_agent = await create_generate_chart_agent()
    sql_agent = await create_sql_agent()
    supervisor = create_supervisor(
        model=llm,
        agents=[sql_agent, generate_chart_agent],

        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()
    return supervisor

graph = asyncio.run(create_supervisor_graph())


async def main():
    """主异步函数"""
    for chunk in graph.stream(
            {"messages": [{"role": "user", "content": "打开百度"}]},
            stream_mode="messages"
    ):
        print(chunk)
        print("\n")


# 如果直接运行此文件
if __name__ == "__main__":
    asyncio.run(main())