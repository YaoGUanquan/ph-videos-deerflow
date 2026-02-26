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
import { usePhVideosConfig } from "@/core/ph-videos";

import { SettingsSection } from "./settings-section";

export function PhVideosSettingsPage() {
  const { t } = useI18n();
  const { config, save } = usePhVideosConfig();
  const [volcanoApiKey, setVolcanoApiKey] = useState("");
  const [dashscopeApiKey, setDashscopeApiKey] = useState("");
  const [phVideosTextPath, setPhVideosTextPath] = useState("");
  const [defaultProvider, setDefaultProvider] = useState("volcano");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setVolcanoApiKey(config.volcano_api_key ?? "");
    setDashscopeApiKey(config.dashscope_api_key ?? "");
    setPhVideosTextPath(config.ph_videos_text_path ?? "");
    setDefaultProvider(config.default_video_provider ?? "volcano");
  }, [config]);

  const handleSave = () => {
    save({
      volcano_api_key: volcanoApiKey,
      dashscope_api_key: dashscopeApiKey,
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
    </div>
  );
}
