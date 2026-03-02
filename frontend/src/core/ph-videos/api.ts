/**
 * ph-videos 视频生成 API 客户端
 *
 * 调用 Gateway 的 /api/ph-videos 接口，API keys 仅通过请求传入，不持久化。
 */

import { getBackendBaseURL } from "../config";

const getBaseURL = () => {
  const base = getBackendBaseURL();
  return base ? `${base}/api/ph-videos` : "/api/ph-videos";
};

export interface GenerateRequest {
  topic: string;
  api_keys: Record<string, string>;
  budget: number;
}

export interface GenerateResponse {
  task_id: string;
  status: string;
}

export interface TaskResponse {
  task_id: string;
  topic: string;
  status: string;
  result_path: string;
  error: string;
  progress: Record<string, unknown>;
}

export interface TasksListResponse {
  tasks: TaskResponse[];
}

export async function createGenerateTask(
  request: GenerateRequest,
): Promise<GenerateResponse> {
  const res = await fetch(`${getBaseURL()}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function getTask(taskId: string): Promise<TaskResponse> {
  const res = await fetch(`${getBaseURL()}/tasks/${taskId}`);
  if (!res.ok) {
    if (res.status === 404) throw new Error("任务不存在");
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function listTasks(): Promise<TasksListResponse> {
  const res = await fetch(`${getBaseURL()}/tasks`);
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json();
}

/** 获取任务视频下载 URL */
export function getTaskDownloadURL(taskId: string): string {
  const base = getBaseURL();
  return `${base}/tasks/${taskId}/download`;
}

export type { PhVideosConfig } from "./storage";
export { getPhVideosConfig, setPhVideosConfig } from "./storage";
