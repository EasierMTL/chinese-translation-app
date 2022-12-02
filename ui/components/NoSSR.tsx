import React, { FC, useEffect, useState } from "react";

export const NoSSR = ({ children }: { children: React.ReactNode }) => {
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);
  return <>{mounted ? children : null}</>;
};
