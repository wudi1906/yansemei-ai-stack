import express from 'express';
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNodeHttpEndpoint,
  LangGraphAgent, ExperimentalEmptyAdapter
} from '@copilotkit/runtime';
// import OpenAI from "openai";

const app = express();
// const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
// const serviceAdapter = new OpenAIAdapter({ openai } as any);
const serviceAdapter = new ExperimentalEmptyAdapter();
app.use('/copilotkit', (req, res, next) => {
  const runtime = new CopilotRuntime({
    agents: {
      'agent': new LangGraphAgent({
        deploymentUrl: "http://localhost:2025", // make sure to replace with your real deployment url
        langsmithApiKey: process.env.LANGSMITH_API_KEY, // only used in LangGraph Platform deployments
        graphId: 'graph', // usually the same as agent name
      })
    },
  });

  const handler = copilotRuntimeNodeHttpEndpoint({
    endpoint: '/copilotkit',
    runtime,
    serviceAdapter,
  });

  return handler(req, res, next);
});

app.listen(4000, () => {
  console.log('Listening at http://localhost:4000/copilotkit');
});