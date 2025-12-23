/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// NOTE  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaek5vU0E9PTplZjUwYWI4Yw==

import { useEffect, useState } from "react";

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZaek5vU0E9PTplZjUwYWI4Yw==