import { useCallback, useEffect, useState } from "react";

import {
  getPhVideosConfig,
  setPhVideosConfig,
} from "./storage";
import type { PhVideosConfig } from "./storage";

export function usePhVideosConfig() {
  const [config, setConfig] = useState<PhVideosConfig>(() =>
    typeof window !== "undefined" ? getPhVideosConfig() : {
      volcano_api_key: "",
      dashscope_api_key: "",
      ph_videos_text_path: "",
      default_video_provider: "volcano",
    },
  );

  useEffect(() => {
    setConfig(getPhVideosConfig());
  }, []);

  const save = useCallback((newConfig: PhVideosConfig) => {
    setPhVideosConfig(newConfig);
    setConfig(newConfig);
  }, []);

  return { config, save };
}
