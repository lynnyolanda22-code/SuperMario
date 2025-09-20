# 🚀 快速部署到Streamlit Cloud

## 方法1：通过GitHub网站（推荐）

### 步骤1：创建GitHub仓库
1. 访问 https://github.com
2. 点击右上角的 "+" 号
3. 选择 "New repository"
4. 仓库名称：`super-mario-streamlit`
5. 选择 "Public"
6. 点击 "Create repository"

### 步骤2：上传文件
1. 在仓库页面点击 "uploading an existing file"
2. 将以下文件拖拽到页面：
   - `streamlit_app.py` (主应用文件)
   - `requirements.txt` (依赖文件)
   - `README.md` (说明文档)
   - `basic_test.py` (测试文件)
3. 在底部输入提交信息："Add Super Mario Bros Streamlit app"
4. 点击 "Commit changes"

### 步骤3：部署到Streamlit Cloud
1. 访问 https://share.streamlit.io/
2. 点击 "New app"
3. 选择你的GitHub仓库
4. 设置配置：
   - **Repository**: 选择 `super-mario-streamlit`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **Requirements file**: `requirements.txt`
5. 点击 "Deploy"

## 方法2：使用GitHub Desktop

1. 下载安装 GitHub Desktop
2. 创建新仓库并选择当前文件夹
3. 提交并推送到GitHub
4. 在Streamlit Cloud中部署

## 部署完成后

部署成功后，您将获得一个类似这样的链接：
```
https://super-mario-streamlit.streamlit.app
```

## 应用功能

- 🎮 多种Super Mario Bros版本选择
- 🕹️ 简单和复杂动作控制
- 🎲 自动游戏模式（AI随机动作）
- ⚡ 可调节游戏速度
- 📊 实时游戏统计（分数、生命、步数）
- 🌐 完全基于Web的界面

## 注意事项

- 确保GitHub仓库是公开的
- 首次部署可能需要5-10分钟
- 所有依赖都已正确配置
- 使用模拟画面展示游戏功能

## 故障排除

如果部署失败：
1. 检查文件路径是否正确
2. 确保requirements.txt格式正确
3. 查看Streamlit Cloud日志
4. 确保仓库是公开的

---

**部署完成后，您就可以分享链接给朋友一起游玩了！** 🎉

