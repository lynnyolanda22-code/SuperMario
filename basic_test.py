#!/usr/bin/env python3
"""
Super Mario Bros - 基础测试版本
纯Python实现，不依赖任何外部库
"""

import time
import random

def create_ascii_game_frame(step_count, mario_x=10):
    """创建ASCII游戏画面"""
    frame = []
    height = 15
    width = 40
    
    # 创建空画面
    for y in range(height):
        frame.append([' '] * width)
    
    # 添加地面
    for x in range(width):
        frame[height-1][x] = '='
        frame[height-2][x] = '='
    
    # 添加马里奥 (M)
    mario_y = height - 3
    if 0 <= mario_x < width:
        frame[mario_y][mario_x] = 'M'
    
    # 添加障碍物 (X)
    if step_count > 10:
        obstacle_x = 25
        obstacle_y = height - 3
        if 0 <= obstacle_x < width:
            frame[obstacle_y][obstacle_x] = 'X'
    
    # 添加金币 ($)
    if step_count % 20 < 10:
        coin_x = 15
        coin_y = height - 5
        if 0 <= coin_x < width:
            frame[coin_y][coin_x] = '$'
    
    # 添加云朵 (.)
    cloud_x = 5
    cloud_y = 3
    if 0 <= cloud_x < width:
        frame[cloud_y][cloud_x] = '.'
        frame[cloud_y][cloud_x+1] = '.'
        frame[cloud_y][cloud_x+2] = '.'
    
    return frame

def display_frame(frame):
    """显示游戏画面"""
    print("\n" + "="*50)
    for row in frame:
        print("|" + "".join(row) + "|")
    print("="*50)

def main():
    """主函数"""
    print("🍄 Super Mario Bros - 基础测试版本")
    print("=" * 50)
    
    # 游戏状态
    score = 0
    lives = 3
    step_count = 0
    mario_x = 10
    done = False
    
    print("游戏说明:")
    print("- 马里奥用 'M' 表示")
    print("- 障碍物用 'X' 表示") 
    print("- 金币用 '$' 表示")
    print("- 云朵用 '.' 表示")
    print()
    print("游戏控制:")
    print("- 按 Enter 键执行一步")
    print("- 输入 'q' 退出游戏")
    print("- 输入 'r' 重置游戏")
    print("- 输入 'a' 自动游戏")
    print()
    
    while not done:
        # 显示游戏信息
        print(f"步数: {step_count:4d} | 分数: {score:4d} | 生命: {lives} | 马里奥位置: {mario_x}")
        
        # 创建并显示游戏画面
        frame = create_ascii_game_frame(step_count, mario_x)
        display_frame(frame)
        
        # 获取用户输入
        user_input = input("输入命令 (Enter=继续, q=退出, r=重置, a=自动): ").strip().lower()
        
        if user_input == 'q':
            print("游戏结束！")
            break
        elif user_input == 'r':
            score = 0
            lives = 3
            step_count = 0
            mario_x = 10
            print("游戏已重置！")
            continue
        elif user_input == 'a':
            # 自动游戏模式
            print("自动游戏模式启动！按 Ctrl+C 停止")
            try:
                while True:
                    step_count += 1
                    mario_x = (mario_x + random.randint(-1, 2)) % 40
                    score += random.randint(0, 10)
                    
                    # 随机减少生命
                    if random.random() < 0.1:
                        lives -= 1
                        if lives <= 0:
                            print("游戏结束！生命耗尽！")
                            done = True
                            break
                    
                    frame = create_ascii_game_frame(step_count, mario_x)
                    display_frame(frame)
                    
                    print(f"步数: {step_count:4d} | 分数: {score:4d} | 生命: {lives} | 马里奥位置: {mario_x}")
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                print("\n自动游戏已停止")
                continue
        else:
            # 正常游戏步进
            step_count += 1
            mario_x = (mario_x + random.randint(-1, 2)) % 40
            score += random.randint(0, 5)
            
            # 随机减少生命
            if random.random() < 0.05:
                lives -= 1
                if lives <= 0:
                    print("游戏结束！生命耗尽！")
                    done = True
    
    print(f"\n最终分数: {score}")
    print("感谢游玩！")

if __name__ == "__main__":
    main()

