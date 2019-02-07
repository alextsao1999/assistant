# HyperMind语音助手

接入百度语音识别API

如果声音RMS大于特定阈值就开始录制

录制完成后将buff进行上传到百度云进行语音识别

不完善的整合了百度的UNIT, 使其初步支持了语义/命令词识别

并调用CommandTrigger添加的触发器

通过如下方式添加触发器

```python
def callback(name, value):
    
    pass

ct = CommandTrigger()
ct.add_intent("意图名称", callback)
```

默认触发器有些不同 callback多了一个参数 intent (意图)

在添加的意图触发器如果没找到 就会调用默认意图触发器 intent 名称必须为default( 主要是因为我懒(●'◡'●)  )

```python
def default_callback(intent, name, value):
    
    pass

ct = CommandTrigger()
ct.add_intent("default", callback)
```

运行assistant.py 对着麦克风进行简单的机器人对话吧~

