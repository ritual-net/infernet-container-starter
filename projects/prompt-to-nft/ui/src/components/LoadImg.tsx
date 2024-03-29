import { useEffect, useState } from "react";

export const LoadImg = ({ url, tokenId }: { url: string; tokenId: number }) => {
  const [loaded, setLoaded] = useState(false);
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    if (loaded) {
      return;
    }
    let img = new Image();
    const loadImg = () => {
      console.log(`trying: ${attempts}`);
      img = new Image();
      img.src = url;
      img.onload = () => {
        setLoaded(true);
      };
      img.onerror = () => {
        if (attempts < 100) {
          // Set a max number of attempts
          setTimeout(() => {
            setAttempts((prev) => prev + 1);
            loadImg(); // Retry loading the image
          }, 1000); // Retry after 1 seconds
        }
      };
    };

    if (!loaded) {
      loadImg();
    }

    // Cleanup function to avoid memory leaks
    return () => {
      img.onload = null;
      img.onerror = null;
    };
  }, [url, loaded, attempts]);

  return (
    <div
      className={
        "bg-teal-600 bg-opacity-20 rounded-lg flex flex-1 justify-center items-center"
      }
    >
      {loaded ? (
        <img className={"rounded-lg"} src={url} alt={`NFT ${tokenId}`} />
      ) : (
        <div className={""}>
          <button
            type="button"
            className="py-3 px-4 inline-flex items-center gap-x-2 text-sm rounded-lg
            border border-transparent bg-emerald-700 text-white hover:bg-blue-700 disabled:opacity-50
            disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
          >
            <span
              className="animate-spin inline-block size-4 border-[2px] border-current border-t-transparent text-white
              rounded-full"
              role="status"
              aria-label="loading"
            ></span>
            Fetching from Arweave
          </button>{" "}
        </div>
      )}
    </div>
  );
};
