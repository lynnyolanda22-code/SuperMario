import streamlit as st
import numpy as np
import time
import random

# 尝试导入OpenCV，如果失败则使用替代方案
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    st.warning("OpenCV不可用，将使用简化版本")

# 设置页面配置
st.set_page_config(
    page_title="Super Mario Bros Game",
    page_icon="🍄",
    layout="wide"
)

# 标题
st.title("🍄 Super Mario Bros Game")
st.markdown("---")

# 侧边栏控制
st.sidebar.header("游戏控制")

# 环境选择
env_options = {
    "SuperMarioBros-v0": "标准版本",
    "SuperMarioBros-v1": "降采样版本", 
    "SuperMarioBros-v2": "像素版本",
    "SuperMarioBros-v3": "矩形版本"
}

selected_env = st.sidebar.selectbox(
    "选择游戏版本",
    options=list(env_options.keys()),
    format_func=lambda x: env_options[x]
)

# 动作空间选择
action_space_options = {
    "simple": "简单动作 (6个动作)",
    "complex": "复杂动作 (12个动作)"
}

selected_action_space = st.sidebar.selectbox(
    "选择动作空间",
    options=list(action_space_options.keys()),
    format_func=lambda x: action_space_options[x]
)

# 游戏速度控制
game_speed = st.sidebar.slider("游戏速度", 0.01, 0.1, 0.05, 0.01)

# 初始化游戏状态
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'running': False,
        'score': 0,
        'lives': 3,
        'step_count': 0,
        'done': True,
        'mario_x': 10
    }

def create_game_frame(step_count, mario_x=10):
    """创建游戏画面"""
    # 创建基础画面
    frame = np.zeros((240, 256, 3), dtype=np.uint8)
    
    # 添加背景颜色（模拟天空）
    frame[:, :, 2] = 135  # 蓝色天空
    frame[:, :, 1] = 135
    frame[:, :, 0] = 135
    
    # 添加地面
    frame[200:, :, 1] = 100  # 绿色地面
    frame[200:, :, 0] = 50
    frame[200:, :, 2] = 0
    
    if HAS_CV2:
        # 使用OpenCV绘制图形
        # 马里奥（红色方块）
        if 0 <= mario_x < 240:
            cv2.rectangle(frame, (mario_x, 180), (mario_x + 20, 200), (0, 0, 255), -1)
        
        # 障碍物（棕色方块）
        if step_count > 50:
            cv2.rectangle(frame, (150, 190), (170, 200), (0, 100, 200), -1)
        
        # 金币（黄色圆圈）
        if step_count % 30 < 15:
            cv2.circle(frame, (100, 120), 8, (0, 255, 255), -1)
        
        # 云朵（白色圆圈）
        cv2.circle(frame, (50, 50), 15, (255, 255, 255), -1)
        cv2.circle(frame, (60, 50), 15, (255, 255, 255), -1)
    else:
        # 不使用OpenCV的简化版本 - 使用更明显的颜色
        # 马里奥（红色方块）
        if 0 <= mario_x < 240:
            frame[180:200, mario_x:mario_x+20, 0] = 255  # 红色
            frame[180:200, mario_x:mario_x+20, 1] = 0
            frame[180:200, mario_x:mario_x+20, 2] = 0
        
        # 障碍物（棕色方块）
        if step_count > 50:
            frame[190:200, 150:170, 0] = 200  # 棕色
            frame[190:200, 150:170, 1] = 100
            frame[190:200, 150:170, 2] = 0
        
        # 金币（黄色区域）
        if step_count % 30 < 15:
            frame[112:128, 92:108, 0] = 255  # 黄色
            frame[112:128, 92:108, 1] = 255
            frame[112:128, 92:108, 2] = 0
        
        # 云朵（白色区域）
        frame[35:65, 35:85, :] = 255  # 白色
    
    return frame

# 创建两列布局
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("游戏画面")
    
    # 游戏显示区域
    game_placeholder = st.empty()
    
    # 控制按钮
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("🎮 开始游戏", key="start"):
            st.session_state.game_state['running'] = True
            st.session_state.game_state['done'] = False
            st.session_state.game_state['score'] = 0
            st.session_state.game_state['lives'] = 3
            st.session_state.game_state['step_count'] = 0
            st.session_state.game_state['mario_x'] = 10
            st.success("游戏开始！")
    
    with col_btn2:
        if st.button("🔄 重置游戏", key="reset"):
            st.session_state.game_state['running'] = False
            st.session_state.game_state['done'] = True
            st.session_state.game_state['score'] = 0
            st.session_state.game_state['lives'] = 3
            st.session_state.game_state['step_count'] = 0
            st.session_state.game_state['mario_x'] = 10
            st.success("游戏已重置！")
    
    with col_btn3:
        if st.button("⏸️ 暂停", key="pause"):
            st.session_state.game_state['running'] = False
            st.info("游戏已暂停")
    
    with col_btn4:
        if st.button("🎲 随机动作", key="random"):
            if st.session_state.game_state['running'] and not st.session_state.game_state['done']:
                # 模拟游戏步进
                st.session_state.game_state['step_count'] += 1
                st.session_state.game_state['score'] += random.randint(0, 10)
                st.session_state.game_state['mario_x'] = (st.session_state.game_state['mario_x'] + random.randint(-2, 3)) % 240
                
                # 随机减少生命
                if random.random() < 0.1:
                    st.session_state.game_state['lives'] -= 1
                    if st.session_state.game_state['lives'] <= 0:
                        st.session_state.game_state['done'] = True
                        st.session_state.game_state['running'] = False
                
                # 生成游戏画面
                frame = create_game_frame(
                    st.session_state.game_state['step_count'],
                    st.session_state.game_state['mario_x']
                )
                
                # 调整图像大小以适应显示
                if HAS_CV2:
                    frame_resized = cv2.resize(frame, (400, 300))
                    game_placeholder.image(frame_resized, channels="BGR", use_column_width=True)
                else:
                    # 不使用OpenCV的简化版本
                    frame_resized = np.zeros((300, 400, 3), dtype=np.uint8)
                    # 简单的缩放
                    for i in range(300):
                        for j in range(400):
                            src_i = int(i * 240 / 300)
                            src_j = int(j * 256 / 400)
                            if src_i < 240 and src_j < 256:
                                frame_resized[i, j] = frame[src_i, src_j]
                    game_placeholder.image(frame_resized, use_column_width=True)
                
                time.sleep(game_speed)

with col2:
    st.subheader("游戏信息")
    
    # 显示游戏状态
    st.metric("分数", st.session_state.game_state['score'])
    st.metric("生命", st.session_state.game_state['lives'])
    st.metric("步数", st.session_state.game_state['step_count'])
    st.metric("马里奥位置", st.session_state.game_state['mario_x'])
    
    if st.session_state.game_state['done']:
        st.warning("游戏结束！")
    elif st.session_state.game_state['running']:
        st.success("游戏进行中...")
    else:
        st.info("游戏未开始")
    
    st.subheader("操作说明")
    st.markdown("""
    **控制说明：**
    - 点击"开始游戏"开始
    - 点击"随机动作"模拟游戏
    - 可以调整游戏速度
    
    **游戏元素：**
    - 红色方块：马里奥
    - 棕色方块：障碍物
    - 黄色圆圈：金币
    - 白色圆圈：云朵
    """)
    
    st.subheader("游戏版本说明")
    for env_key, env_desc in env_options.items():
        if env_key == selected_env:
            st.info(f"**当前版本：** {env_desc}")
        else:
            st.text(f"{env_key}: {env_desc}")

# 自动游戏模式
if st.sidebar.checkbox("自动游戏模式", value=False):
    if st.session_state.game_state['running'] and not st.session_state.game_state['done']:
        # 自动执行随机动作
        st.session_state.game_state['step_count'] += 1
        st.session_state.game_state['score'] += random.randint(0, 5)
        st.session_state.game_state['mario_x'] = (st.session_state.game_state['mario_x'] + random.randint(-1, 2)) % 240
        
        # 随机减少生命
        if random.random() < 0.05:
            st.session_state.game_state['lives'] -= 1
            if st.session_state.game_state['lives'] <= 0:
                st.session_state.game_state['done'] = True
                st.session_state.game_state['running'] = False
        
        # 生成游戏画面
        frame = create_game_frame(
            st.session_state.game_state['step_count'],
            st.session_state.game_state['mario_x']
        )
        
        if HAS_CV2:
            frame_resized = cv2.resize(frame, (400, 300))
            game_placeholder.image(frame_resized, channels="BGR", use_column_width=True)
        else:
            # 不使用OpenCV的简化版本
            frame_resized = np.zeros((300, 400, 3), dtype=np.uint8)
            # 简单的缩放
            for i in range(300):
                for j in range(400):
                    src_i = int(i * 240 / 300)
                    src_j = int(j * 256 / 400)
                    if src_i < 240 and src_j < 256:
                        frame_resized[i, j] = frame[src_i, src_j]
            game_placeholder.image(frame_resized, use_column_width=True)
        
        time.sleep(game_speed)
        st.rerun()

# 页脚
st.markdown("---")
st.markdown("**Super Mario Bros** - 基于Streamlit的Web版本")
st.markdown("使用模拟画面展示游戏功能")
st.info("💡 这是演示版本，展示了完整的游戏界面和交互功能。")

