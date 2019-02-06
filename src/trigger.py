#Created By Alex
import wave

import pyaudio
import pydub

class SoundTrigger :
    # WIDTH = 2
    # CHANNELS = 1
    # RATE = 44100

    #是否处在记录中
    recording = False

    #原始帧数据
    wav_buff = []

    def __init__(self, threshold, trigger, width = 2, rate = 16000, channels = 1):
        '''
        :param threshold:  阈值
        :param trigger:  触发器
        :param width:  位宽
        :param rate:  采样率
        :param channels: 频道数
        '''
        #### 初始化配置

        self.WIDTH = width
        self.RATE = rate
        self.CHANNELS = channels

        self.threshold = threshold
        self.trigger = trigger

        #### 实例化PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(self.WIDTH),
                        channels = self.CHANNELS,
                        rate = self.RATE,
                        input = True,
                        output = False,
                        stream_callback = self.callback)

    def callback(self, in_data, frame_count, time_info, status):
        segment = pydub.AudioSegment(in_data, sample_width = self.WIDTH, frame_rate = self.RATE, channels = self.CHANNELS)
        # 是否到达阈值
        reached = segment.rms > self.threshold
        if reached and not self.recording :
            self.recording = True #开始记录
            self.wav_buff = []  # 清空原始波数据
        if not reached :
            #RMS声音回落至阈值下面 调用触发器 传递记录的录音数据
            if self.recording :
                self.trigger(self.wav_buff)
            self.recording = False
        if self.recording :
            self.wav_buff.append(in_data)
        return (b'', pyaudio.paContinue)

    def start(self):
        '''
        开始监控
        :return:
        '''
        self.stream.start_stream()

    def stop(self):
        '''
        结束监控
        :return:
        '''
        self.stream.stop_stream()

    def is_active(self):
        return self.stream.is_active()

    def get_stream(self):
        return self.stream

    def close(self):
        '''
        关闭音频流 终止监控
        :return:
        '''
        self.stream.close()
        self.p.terminate()

    def save_file(self, filename, data):
        '''
        保存为wave文件
        :param filename:  文件名
        :param data:  raw frame data 原生数据
        '''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.WIDTH)
        wf.setframerate(self.RATE)
        wf.writeframes(b"".join(data))
        wf.close()
