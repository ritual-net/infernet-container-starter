import { PropsWithChildren, useEffect, useState } from "react";

export const ClientRendered = ({ children }: PropsWithChildren) => {
  // look at here:https://nextjs.org/docs/messages/react-hydration-error#solution-1-using-useeffect-to-run-on-the-client-only
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return null;
  }
  return <>{children}</>;
};
