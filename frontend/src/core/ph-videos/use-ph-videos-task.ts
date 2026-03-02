"use client";

import { useCallback, useEffect, useState } from "react";

import {
  createGenerateTask,
  getTask,
  type GenerateRequest,
  type TaskResponse,
} from "./api";

export type TaskStatus =
  | "pending"
  | "scripting"
  | "generating_scenes"
  | "generating_audio"
  | "rendering"
  | "completed"
  | "failed";

export function usePhVideosTask() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [task, setTask] = useState<TaskResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  const startTask = useCallback(async (request: GenerateRequest) => {
    setError(null);
    setTask(null);
    try {
      const res = await createGenerateTask(request);
      setTaskId(res.task_id);
      setIsPolling(true);
      return res.task_id;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    }
  }, []);

  useEffect(() => {
    if (!taskId || !isPolling) return;

    const poll = async () => {
      try {
        const t = await getTask(taskId);
        setTask(t);
        if (t.status === "completed" || t.status === "failed") {
          setIsPolling(false);
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
        setIsPolling(false);
      }
    };

    poll();
    const id = setInterval(poll, 2000);
    return () => clearInterval(id);
  }, [taskId, isPolling]);

  const reset = useCallback(() => {
    setTaskId(null);
    setTask(null);
    setError(null);
    setIsPolling(false);
  }, []);

  return {
    taskId,
    task,
    error,
    isPolling,
    startTask,
    reset,
  };
}
