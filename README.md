# CompactPuzzleGame
## 简介 Introduction
一个基于Pygame的数学拼图游戏，目标是创建若干骨牌拼图并拼成可以紧密移动而不散开的结构。

A Pygame-based math puzzle game where players create domino-like tiles and assemble them into compact structures that can move cohesively without collapsing.

## 游玩方法 How to Play
在Releases中下载压缩包，其中有构建好的Windows可执行程序。

macOS和Linux需要手动打包或在Python环境下运行.py脚本。

Download the compressed package from Releases, which contains pre-built Windows executables.

For macOS and Linux users: Either manually package the game or run the .py script directly in a Python environment.

## 玩法规则 Game Rules
### 基本操作 Basic Controls
- 左键点击或者按住拖动，选中格子；右键点击或者按住拖动，清空选中的格子。 
- 点击 create 或按下 Enter / 空格，根据选中的格子创建拼图块。
- 左键点击选择拼图块，按住拖动移动拼图块，点击 delete 或按下 del 键删除拼图块。
- 将拼图块拼成目标结构后，点击 complete 或按下 C 键，完成拼图，进入结算环节。
- Left click/hold & drag to select grid cells.
- Right click/hold & drag to deselect cells.
- Click 'Create' or press Enter/Space to generate jigsaw pieces from selected cells.
- Left click to select tiles, hold & drag to move tiles, click 'Delete' or press del to remove pieces.
- After assembling target structure, click 'Complete' or press C to finish.
### 其他操作 Additional Controls
- 点击 restart 或按下 R 键清空盘面。
- 点击 undo 或按下 Z 键撤销一步。
- 按住鼠标中键并拖动，移动盘面。
- 拖动滑动条、按下 +/- 按钮、按下 +/- 键，或滚动鼠标滚轮，缩放盘面。
- Click 'Restart' or press R to reset board.
- Click 'Undo' or press Z to undo last action.
- Middle-click & drag to pan the board.
- Use slider, +/- buttons, +/- keys, or mouse wheel to zoom.
### 游戏目标 Game Objectives
- 保证最终的拼图结构无论如何移动，都不会散开（每一块拼图块的相对位置都不改变）。
- 在此基础上，追求更高的分数：
1. 减小 最大拼图块的格子数、总格子数;
2. 在减小到一定的情况下，增大 拼图块数量、最大拼图块的格子数与总格子数的比例;
3. 避免过于简单的结构（如全包围）。
- Ensure final structure maintains cohesion during movement \(relative positions of all tiles remain unchanged).
- Optimize scoring by:
1. Minimizing largest tile size and total cells;
2. While reduced to some low extent, maximize number of tiles and the ratio between largest tile and total cells;
3. Avoid overly simple structures.

## 更新计划 Roadmap
- [x] 成功时计算分数 Score calculation upon success
- [x] 添加音效 Sound effects implementation
- [ ] 增加成功/失败的炫酷动画 Enhanced success/failure animations
- [ ] 支持窗口缩放与全屏模式（当前存在渲染bug） Window scaling & fullscreen support (current rendering issues)
- [ ] 分数算法优化 Score algorithm optimization
- [ ] 优化UI的美术表现 UI visual improvements
- [ ] 优化音效表现 Sound effect refinements

## 碎碎念 Developer Notes
为了智力题活动写的游戏，未来将移植到web前端。可惜目前后端程序暂时神隐了，只能说未来可期。

Created for an intellectual puzzle event, with plans for future web frontend migration.
