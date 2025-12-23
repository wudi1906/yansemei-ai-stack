/**
 * Copyright (c) 2025 Dean Wu. All rights reserved.
 * AuroraAI Project.
 */
// FIXME  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTVXh4VHc9PTo5OWRjMjcxNQ==

const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};
// @ts-expect-error  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTVXh4VHc9PTo5OWRjMjcxNQ==

export default reportWebVitals;