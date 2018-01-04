## Requirements

* Python 3
* OpenCV 3
* NumPy
* Android Debug Bridge

``` bash
pip3 install opencv-python
pip3 install numpy
```

Python与Android Debug Bridge可在官网下载.

## Usage

开始游戏并连接手机至电脑。

全自动版本：

``` bash
python3 auto_play.py
```

半自动版本：

``` bash
python3 semi_auto_play.py
```

## Comments

距离计算的具体实现与其它程序稍有不同，理论上可避免跳跃偏差在变换方向时带来的影响。

由于在跳跃的时候垂直于所跳跃方向的偏移对于跳跃的距离没有影响，所以在原先距离上稍作变换。

具体依据公式，定义```x```方向为图像中水平方向，```y```方向为图像中竖直方向。

```x```, ```y```为变换前（当前位置与目标位置）坐标之差，```x'```, ```y'```为变换后坐标之差。

<a href="https://www.codecogs.com/eqnedit.php?latex=2\sqrt{3}y'=2x'=x&plus;\sqrt{3}y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?2\sqrt{3}y'=2x'=x&plus;\sqrt{3}y" title="2\sqrt{3}y'=2x'=x+\sqrt{3}y" /></a>

由于角度固定，所以真实跳跃距离与```x'```, ```y'```均呈正比，便可以求得

<a href="https://www.codecogs.com/eqnedit.php?latex=x&plus;\sqrt{3}y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x&plus;\sqrt{3}y" title="x+\sqrt{3}y" /></a>

与长按时间的关系，以达到用坐标之差计算长按时间的效果。

使用Canny与HoughLinesP检测矩形，使用HoughCircles检测圆形。
