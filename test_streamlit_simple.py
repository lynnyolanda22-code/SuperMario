#!/usr/bin/env python3
"""
简单的Streamlit测试版本
"""

import streamlit as st
import numpy as np
import time
import random

# 设置页面配置
st.set_page_config(
    page_title="Super Mario Bros Game - Test",
    page_icon="🍄",
    layout="wide"
)

# 标题
st.title("🍄 Super Mario Bros Game - 测试版本")
st.markdown("---")

def create_simple_frame(step_count, mario_x=10):
    """创建简单的游戏画面"""
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

def resize_frame_simple(frame, target_width=400, target_height=300):
    """简单的图像缩放"""
    frame_resized = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    # 简单的缩放
    for i in range(target_height):
        for j in range(target_width):
            src_i = int(i * 240 / target_height)
            src_j = int(j * 256 / target_width)
            if src_i < 240 and src_j < 256:
                frame_resized[i, j] = frame[src_i, src_j]
    return frame_resized

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
                frame = create_simple_frame(
                    st.session_state.game_state['step_count'],
                    st.session_state.game_state['mario_x']
                )
                
                # 调整图像大小以适应显示
                frame_resized = resize_frame_simple(frame, 400, 300)
                game_placeholder.image(frame_resized, use_column_width=True)

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
    
    st.subheader("测试信息")
    st.text(f"NumPy版本: {np.__version__}")
    st.text("画面生成: 简化版本")
    
    # 显示原始画面（用于调试）
    if st.button("显示原始画面"):
        frame = create_simple_frame(0, 10)
        st.image(frame, caption="原始画面 (240x256)", use_column_width=True)

# 页脚
st.markdown("---")
st.markdown("**Super Mario Bros** - 简化测试版本")
st.markdown("用于验证画面显示功能")
