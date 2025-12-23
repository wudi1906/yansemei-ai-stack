/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTek51Tmc9PTo3ZjEzYTU4MQ==

import { HumanInterrupt } from "@langchain/langgraph/prebuilt";
// TODO  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTek51Tmc9PTo3ZjEzYTU4MQ==

export function isAgentInboxInterruptSchema(
  value: unknown,
): value is HumanInterrupt | HumanInterrupt[] {
  const valueAsObject = Array.isArray(value) ? value[0] : value;
  return (
    valueAsObject &&
    typeof valueAsObject === "object" &&
    "action_request" in valueAsObject &&
    typeof valueAsObject.action_request === "object" &&
    "config" in valueAsObject &&
    typeof valueAsObject.config === "object" &&
    "allow_respond" in valueAsObject.config &&
    "allow_accept" in valueAsObject.config &&
    "allow_edit" in valueAsObject.config &&
    "allow_ignore" in valueAsObject.config
  );
}