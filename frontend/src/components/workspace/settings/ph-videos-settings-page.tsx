"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useI18n } from "@/core/i18n/hooks";
import {
  getTaskDownloadURL,
  usePhVideosConfig,
  usePhVideosTask,
} from "@/core/ph-videos";

import { SettingsSection } from "./settings-section";

export function PhVideosSettingsPage() {
  const { t } = useI18n();
  const { config, save } = usePhVideosConfig();
  const [volcanoApiKey, setVolcanoApiKey] = useState("");
  const [dashscopeApiKey, setDashscopeApiKey] = useState("");
  const [openaiApiKey, setOpenaiApiKey] = useState("");
  const [phVideosTextPath, setPhVideosTextPath] = useState("");
  const [defaultProvider, setDefaultProvider] = useState("volcano");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setVolcanoApiKey(config.volcano_api_key ?? "");
    setDashscopeApiKey(config.dashscope_api_key ?? "");
    setOpenaiApiKey(config.openai_api_key ?? "");
    setPhVideosTextPath(config.ph_videos_text_path ?? "");
    setDefaultProvider(config.default_video_provider ?? "volcano");
  }, [config]);

  const handleSave = () => {
    save({
      volcano_api_key: volcanoApiKey,
      dashscope_api_key: dashscopeApiKey,
      openai_api_key: openaiApiKey,
      ph_videos_text_path: phVideosTextPath,
      default_video_provider: defaultProvider,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  return (
    <div className="space-y-8">
      <SettingsSection
        title={t.settings.phVideos.title}
        description={t.settings.phVideos.description}
      >
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="volcano-api-key">
              {t.settings.phVideos.volcanoApiKey}
            </Label>
            <Input
              id="volcano-api-key"
              type="password"
              placeholder={t.settings.phVideos.volcanoPlaceholder}
              value={volcanoApiKey}
              onChange={(e) => setVolcanoApiKey(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="dashscope-api-key">
              {t.settings.phVideos.dashscopeApiKey}
            </Label>
            <Input
              id="dashscope-api-key"
              type="password"
              placeholder={t.settings.phVideos.dashscopePlaceholder}
              value={dashscopeApiKey}
              onChange={(e) => setDashscopeApiKey(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="openai-api-key">OpenAI API Key（脚本生成）</Label>
            <Input
              id="openai-api-key"
              type="password"
              placeholder="sk-..."
              value={openaiApiKey}
              onChange={(e) => setOpenaiApiKey(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="ph-videos-text-path">
              {t.settings.phVideos.phVideosTextPath}
            </Label>
            <Input
              id="ph-videos-text-path"
              type="text"
              placeholder={t.settings.phVideos.phVideosTextPathPlaceholder}
              value={phVideosTextPath}
              onChange={(e) => setPhVideosTextPath(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label>{t.settings.phVideos.defaultProvider}</Label>
            <Select value={defaultProvider} onValueChange={setDefaultProvider}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="volcano">火山 Seedance</SelectItem>
                <SelectItem value="wanxiang">通义万相</SelectItem>
                <SelectItem value="comfyui">ComfyUI</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <p className="text-muted-foreground text-xs">
            {t.settings.phVideos.storageHint}
          </p>
          <Button onClick={handleSave} disabled={saved}>
            {saved ? t.settings.phVideos.saved : t.settings.phVideos.save}
          </Button>
        </div>
      </SettingsSection>

      <PhVideosGenerateSection />
    </div>
  );
}

function PhVideosGenerateSection() {
  const { t } = useI18n();
  const { config } = usePhVideosConfig();
  const {
    taskId,
    task,
    error,
    isPolling,
    startTask,
    reset,
  } = usePhVideosTask();
  const [topic, setTopic] = useState("");
  const [budget, setBudget] = useState(10);

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    try {
      await startTask({
        topic: topic.trim(),
        api_keys: {
          llm: config.openai_api_key || "",
          volcano: config.volcano_api_key || "",
          dashscope: config.dashscope_api_key || "",
        },
        budget,
      });
    } catch {
      // error set in hook
    }
  };

  return (
    <SettingsSection
      title="视频生成"
      description="通过 API 生成视频，API keys 仅随请求传入，不持久化到后端。"
    >
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="ph-videos-topic">主题</Label>
          <Input
            id="ph-videos-topic"
            placeholder="例如：一只猫在阳光下打盹"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={isPolling}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="ph-videos-budget">预算</Label>
          <Input
            id="ph-videos-budget"
            type="number"
            min={0.1}
            step={1}
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value) || 10)}
            disabled={isPolling}
          />
        </div>
        {error && (
          <p className="text-destructive text-sm">{error}</p>
        )}
        {task && (
          <div className="space-y-2 rounded-lg border p-3">
            <p className="text-sm">
              <span className="text-muted-foreground">状态：</span>
              {task.status}
            </p>
            {task.status === "completed" && task.result_path && (
              <a
                href={taskId ? getTaskDownloadURL(taskId) : "#"}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline text-sm"
              >
                下载视频
              </a>
            )}
            {task.status === "failed" && task.error && (
              <p className="text-destructive text-sm">{task.error}</p>
            )}
          </div>
        )}
        <div className="flex gap-2">
          <Button
            onClick={handleGenerate}
            disabled={isPolling || !topic.trim()}
          >
            {isPolling ? "生成中..." : "生成视频"}
          </Button>
          {task && (
            <Button variant="outline" onClick={reset}>
              重置
            </Button>
          )}
        </div>
      </div>
    </SettingsSection>
  );
}
