import os
import logging
import azure.cognitiveservices.speech as speechsdk
import gradio as gr
from pydub import AudioSegment
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

def split_text(text, max_length=5000):
    """
    将文本分割成较小的块，每块大约5000个字符（约3-4分钟的语音）
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_length:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def text_to_speech(text):
    try:
        if not text:
            logging.warning("输入文本为空，请输入有效文本")
            return None

        chunks = split_text(text)
        output_files = []

        for i, chunk in enumerate(chunks):
            output_file_path = f'output_{i+1}.wav'
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file_path)
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

            speech_synthesis_result = speech_synthesizer.speak_text_async(chunk).get()

            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logging.info(f"Speech synthesized for chunk {i+1} and saved to [{output_file_path}]")
                output_files.append(output_file_path)
            elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_synthesis_result.cancellation_details
                logging.error(f"Speech synthesis canceled for chunk {i+1}: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        logging.error(f"Error details: {cancellation_details.error_details}")
                return None

        # 合并音频文件
        if output_files:
            combined = AudioSegment.empty()
            for file in output_files:
                combined += AudioSegment.from_wav(file)
            
            final_output = "final_output.wav"
            combined.export(final_output, format="wav")
            
            # 删除临时文件
            for file in output_files:
                os.remove(file)
            
            logging.info(f"All chunks combined into [{final_output}]")
            return final_output
        else:
            return None

    except Exception as e:
        logging.error(f"发生异常: {e}")
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