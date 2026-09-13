# WeChat AI Sticker Pack

一个用于制作或修订微信表情专辑的 Codex Agent Skill。它面向真人照片、既有角色和品牌形象，强调角色一致性、分阶段人工确认、动态表情质量检查，以及微信投稿素材的确定性验证。

## 核心能力

- 从照片或既有角色建立可复用的角色母版
- 根据人物语言习惯规划表情文案、动作与节奏
- 在批量生成前设置母版、完整静态套图、动画样片和最终套图四个审批节点
- 支持静态表情和 A/M/B 等完整动画状态
- 对文字、透明背景、手部、道具连续性和角色漂移进行视觉检查
- 将最终 GIF 解码到明暗背景上进行逐帧审核
- 校验数量、尺寸、格式、透明度、循环、帧时长及文件大小
- 为单张缺陷执行局部返修，避免破坏已经批准的素材

## 安装

将整个 `wechat-ai-sticker-pack` 文件夹放入 Codex skills 目录，例如：

```text
~/.codex/skills/wechat-ai-sticker-pack/
```

两个辅助脚本需要 Python 3.10+ 和 Pillow：

```bash
python -m pip install -r requirements.txt
```

## 使用

在 Codex 中调用：

```text
请用 $wechat-ai-sticker-pack 根据这些参考照片制作一套微信动态表情包，先和我确认制作方式与角色母版。
```

Skill 会按照以下流程推进：

1. 确认静态或动态专辑，以及绘制/生成方式。
2. 建立角色母版并等待明确批准。
3. 规划文案、语义动作、构图、道具与动画节奏。
4. 完成整套静态关键姿势并等待批准。
5. 制作有代表性的动画样片并等待批准。
6. 批量制作、添加确定性文字层并导出。
7. 在明暗聊天背景中检查解码帧并运行文件验证。
8. 展示最终套图，获得批准后才将其视为完成。

## 辅助脚本

渲染动画逐帧审核图：

```bash
python scripts/render_animation_review.py path/to/sticker-pack
```

验证动态表情包：

```bash
python scripts/validate_sticker_pack.py path/to/sticker-pack \
  --mode animated \
  --expected-count 16 \
  --main-size 240x240 \
  --thumb-size 120x120
```

微信表情开放平台的字段和限制可能变化。最终导出前，应以当时提交界面显示的要求为准，并将实际参数传给验证脚本。

## 目录结构

```text
wechat-ai-sticker-pack/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── method.md
│   ├── prompt-templates.md
│   └── submission-checklist.md
├── scripts/
│   ├── render_animation_review.py
│   └── validate_sticker_pack.py
├── requirements.txt
└── LICENSE
```

## 安全与权利

上传或发布真人照片、角色、字体、商标和生成素材前，请确认拥有必要授权。产品化部署时，还应提供肖像授权、隐私与数据删除机制，并单独核验所使用图像模型及其权重的商业许可。

## License

[MIT](LICENSE)
