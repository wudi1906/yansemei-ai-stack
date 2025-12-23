/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */

import { PrismAsyncLight as SyntaxHighlighterPrism } from "react-syntax-highlighter";
import tsx from "react-syntax-highlighter/dist/esm/languages/prism/tsx";
import python from "react-syntax-highlighter/dist/esm/languages/prism/python";
import { coldarkDark } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { FC } from "react";
// eslint-disable  MC8yOmFIVnBZMlhsa0xUb3Y2bzZiRzE2TlE9PTpmNzE5ZDA0YQ==

// Register languages you want to support
SyntaxHighlighterPrism.registerLanguage("js", tsx);
SyntaxHighlighterPrism.registerLanguage("jsx", tsx);
SyntaxHighlighterPrism.registerLanguage("ts", tsx);
SyntaxHighlighterPrism.registerLanguage("tsx", tsx);
SyntaxHighlighterPrism.registerLanguage("python", python);

interface SyntaxHighlighterProps {
  children: string;
  language: string;
  className?: string;
}
// eslint-disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZiRzE2TlE9PTpmNzE5ZDA0YQ==

export const SyntaxHighlighter: FC<SyntaxHighlighterProps> = ({
  children,
  language,
  className,
}) => {
  return (
    <SyntaxHighlighterPrism
      language={language}
      style={coldarkDark}
      customStyle={{
        margin: 0,
        width: "100%",
        background: "transparent",
        padding: "1.5rem 1rem",
      }}
      className={className}
    >
      {children}
    </SyntaxHighlighterPrism>
  );
};