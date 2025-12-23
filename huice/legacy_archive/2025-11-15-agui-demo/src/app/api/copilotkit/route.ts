import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";
import {LangGraphAgent} from "@ag-ui/langgraph";

// 1. You can use any service adapter here for multi-agent support. We use
//    the empty adapter since we're only using one agent.
const serviceAdapter = new ExperimentalEmptyAdapter();

// 2. Create the CopilotRuntime instance and utilize the PydanticAI AG-UI
//    integration to setup the connection.
const runtime = new CopilotRuntime({
  agents: {
    'agent': new LangGraphAgent({
      deploymentUrl: "http://localhost:2025", // make sure to replace with your real deployment url
      langsmithApiKey: process.env.LANGSMITH_API_KEY, // only used in LangGraph Platform deployments
      graphId: 'graph', // usually the same as agent name
    })
    // Our AG-UI endpoint URL
    // "agent": new HttpAgent({ url: "http://localhost:8000/" }),
  }
});

// 3. Build a Next.js API route that handles the CopilotKit runtime requests.
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};