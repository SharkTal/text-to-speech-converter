# Text-to-Speech Converter

这是一个使用Azure语音服务和Gradio构建的文本到语音转换器。

## 功能

- 上传文本文件并将其转换为MP3音频文件
- 支持长文本，自动分割并合并音频
- 简单的Web界面，易于使用

## 安装

1. 克隆仓库：

'''
git clone https://github.com/你的用户名/text-to-speech-converter.git cd text-to-speech-converter
'''

2. 安装依赖：

'''
pip install -r requirements.txt
'''

3. 设置Azure语音服务凭证：
在系统环境变量中设置 `SPEECH_KEY` 和 `SPEECH_REGION`。

## 使用

运行以下命令启动应用：

'''
python speech_synthesis_v3.py
'''


然后在浏览器中打开显示的URL，上传文本文件并下载生成的音频文件。

## 注意事项

确保你的系统中安装了ffmpeg，这是生成MP3文件所必需的。
