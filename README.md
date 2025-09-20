# Super Mario Bros - Streamlit Web版本

这是一个基于Streamlit的Super Mario Bros游戏Web应用，可以在浏览器中直接游玩经典的马里奥游戏。

## 功能特性

- 🎮 多种游戏版本选择（标准、降采样、像素、矩形）
- 🕹️ 简单和复杂动作控制
- 🎲 自动游戏模式（AI随机动作）
- ⚡ 可调节游戏速度
- 📊 实时游戏统计信息
- 🌐 基于Web的界面，无需安装

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run streamlit_app.py
```

3. 在浏览器中打开 `http://localhost:8501`

## 部署到Streamlit Cloud

1. 将代码推送到GitHub仓库
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 点击 "New app"
4. 选择你的GitHub仓库
5. 设置以下配置：
   - **Main file path**: `streamlit_app.py`
   - **Requirements file**: `requirements.txt`
6. 点击 "Deploy"

## 文件说明

- `streamlit_app.py` - 主要的Streamlit应用文件
- `requirements.txt` - 依赖文件
- `basic_test.py` - 基础测试版本
- `simple_test.py` - 简单测试版本

## 技术栈

- **Streamlit** - Web应用框架
- **OpenCV** - 图像处理
- **NumPy** - 数值计算

## 许可证

请参考原项目的许可证信息。