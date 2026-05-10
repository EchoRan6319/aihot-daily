# AI HOT Daily Report

> 每日自动抓取 [AI HOT](https://aihot.virxact.com) 资讯，生成静态日报页面并部署到 GitHub Pages。

每天北京时间 09:00 自动更新，无需人工干预。

**[在线预览](https://echoran6319.github.io/aihot-daily/)**

---

## 工作原理

```
GitHub Actions (cron)
    ↓
Python 脚本请求 aihot.virxact.com API
    ↓
Jinja2 渲染为静态 HTML
    ↓
部署到 GitHub Pages
```

## 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮。

### 2. 开启 GitHub Pages

进入仓库 **Settings → Pages**，Source 选择 **GitHub Actions**。

### 3. 启用 Actions

进入 **Actions** 标签页，点击 **I understand my workflows, go ahead and enable them**。

完成。次日北京时间 09:00 即可看到第一份日报。

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/EchoRan6319/aihot-daily.git
cd aihot-daily

# 安装依赖
pip install -r requirements.txt

# 生成日报
python scripts/generate.py
```

生成的文件在 `output/` 目录下，直接用浏览器打开 `output/index.html` 即可预览。

## 项目结构

```
aihot-daily/
├── scripts/
│   └── generate.py          # 数据抓取与页面生成
├── templates/
│   └── daily.html            # Jinja2 模板
├── static/
│   └── style.css             # 样式
├── .github/workflows/
│   └── daily.yml             # GitHub Actions 定时任务
├── requirements.txt
└── output/                   # 生成的静态文件（git ignored）
```

## 日报分类

| 分类 | 内容 |
|------|------|
| 模型发布/更新 | 新模型发布、模型升级 |
| 产品发布/更新 | AI 产品上线、功能更新 |
| 行业动态 | 公司动态、融资、政策 |
| 论文研究 | 重要论文、研究成果 |
| 技巧与观点 | 使用技巧、行业观点 |
| 快讯 | 简短新闻速览 |

## 自定义

**修改更新时间：** 编辑 `.github/workflows/daily.yml` 中的 cron 表达式。

**修改样式：** 编辑 `static/style.css`。

**修改页面结构：** 编辑 `templates/daily.html`。

## 常见问题

**Q: Actions 没有自动运行？**
A: 确认已启用 Actions 并设置了 Pages source 为 GitHub Actions。首次需要手动触发一次 workflow_dispatch。

**Q: 能看历史日报吗？**
A: 可以。页面底部有历史日报链接，自动保留最近 90 天。

**Q: 数据从哪来？**
A: [aihot.virxact.com](https://aihot.virxact.com) 的公开 API，无需 API Key。

## License

MIT
