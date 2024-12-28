import os
import logging
import azure.cognitiveservices.speech as speechsdk

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

# 读取本地文本文件
input_file_path = '/Users/tal/Desktop/text-to-speech/sample.txt'  # 假设输入文件名为 input.txt
output_file_path = '/Users/tal/Desktop/text-to-speech/sample.wav'  # 假设输出文件名为 output.wav

try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()
    
    if not text:
        logging.warning("输入文件为空，请输入有效文本")
        exit(1)

    # 配置音频输出到文件
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file_path)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # 合成语音
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        logging.info("Speech synthesized for text in file [{}] and saved to [{}]".format(input_file_path, output_file_path))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        logging.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                logging.error("Error details: {}".format(cancellation_details.error_details))
                logging.error("Did you set the speech resource key and region values?")
except Exception as e:
    logging.error("发生异常: {}".format(e))