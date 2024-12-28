import os
import logging
import azure.cognitiveservices.speech as speechsdk
import gradio as gr

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取环境变量并检查是否存在
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')

if not speech_key or not speech_region:
    logging.error("请设置环境变量 SPEECH_KEY 和 SPEECH_REGION")
    exit(1)

# 配置语音合成
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

# 设置语音名称为配置项，默认使用 en-US-BrianMultilingualNeural
voice_name = os.getenv('VOICE_NAME', 'en-US-BrianMultilingualNeural')
speech_config.speech_synthesis_voice_name = voice_name

def text_to_speech(text):
    try:
        if not text:
            logging.warning("输入文本为空，请输入有效文本")
            return None

        # 配置音频输出到文件
        output_file_path = 'output.wav'
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file_path)

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # 合成语音
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info("Speech synthesized for text and saved to [{}]".format(output_file_path))
            return output_file_path
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            logging.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    logging.error("Error details: {}".format(cancellation_details.error_details))
                    logging.error("Did you set the speech resource key and region values?")
            return None
    except Exception as e:
        logging.error("发生异常: {}".format(e))
        return None

def process_file(file):
    try:
        with open(file.name, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        audio_path = text_to_speech(text)
        if audio_path:
            return audio_path
        else:
            return None
    except Exception as e:
        logging.error("处理文件时发生异常: {}".format(e))
        return None

# 创建 Gradio 界面
iface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="上传文本文件 (.txt)"),
    outputs=gr.File(label="下载音频文件 (.wav)"),
    title="Text to Speech Converter",
    description="上传一个文本文件，将其转换为音频文件并下载。"
)

# 启动 Gradio 应用
if __name__ == '__main__':
    iface.launch()