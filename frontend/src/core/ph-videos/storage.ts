/**
 * ph-videos 配置存储（仅前端，与 ph-videos-text 一致）
 * 使用 localStorage，可选 cookie。不落盘、不发送到后端。
 */

const STORAGE_KEY = "ph_videos_config";

export interface PhVideosConfig {
  volcano_api_key: string;
  dashscope_api_key: string;
  ph_videos_text_path: string;
  default_video_provider: string;
}

const DEFAULT: PhVideosConfig = {
  volcano_api_key: "",
  dashscope_api_key: "",
  ph_videos_text_path: "",
  default_video_provider: "volcano",
};

export function getPhVideosConfig(): PhVideosConfig {
  if (typeof window === "undefined") return DEFAULT;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT;
    const parsed = JSON.parse(raw) as Partial<PhVideosConfig>;
    return { ...DEFAULT, ...parsed };
  } catch {
    return DEFAULT;
  }
}

export function setPhVideosConfig(config: PhVideosConfig): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
  } catch {
    // ignore
  }
}
