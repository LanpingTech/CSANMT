# CSANMT Translation EN2ZH 微调使用说明

## 准备中英文数据集(用于Finetuning)

1. 英文数据集，**train.en**

格式如下：
```
This paper provides some reflections on the field of mathematical software on the occasion of John Rice's 65th birthday.
I describe some of the common themes of research in this field and recall some significant events in its evolution.
Finally, I raise a number of issues that are of concern to future developments.
The field of mathematical software is concerned with the science and engineering of solving mathematical problems with computers.The primary focus is the development of general-purpose software tools applicable to problems in a variety of disciplines.
There are a large number of facets to this work, including the following.
......
```

2. 中文数据集，**train.zh**

格式如下：
```
在约翰·赖斯65岁生日之际，本文对数学软件领域进行了一些思考。 
我描述了该领域研究的一些共同主题，并回顾了其发展过程中的一些重大事件。 
最后，我提出了一些与未来发展有关的问题。 
数学软件领域涉及用计算机解决数学问题的科学和工程。主要重点是开发适用于各种学科问题的通用软件工具。 
这项工作有很多方面，包括以下方面。
......
```

## 安装数据集预处理以及微调所需依赖

1. 创建虚拟环境
```bash
conda create -n modelscope python=3.9 -y
```

2. 激活虚拟环境
```bash
conda activate modelscope
```

3. 安装Pytorch
```bash
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.6 -c pytorch -c conda-forge
```
这里，我们使用的是Pytorch 1.12.1版本，因为这个版本的Pytorch支持CUDA 11.6，而我们使用的服务器上的CUDA版本就是11.6。

4. 安装Tensorflow
```bash
pip install tensorflow-gpu==2.9
```
经过测试，最新版本Modelscope的Tensorflow版本可以支持2.9，且本项目在2.9版本下可以正常运行。

5. 安装其他依赖
```bash
pip install -r requirements.txt
```

## 下载预训练模型
```bash
python download_model.py
```
运行结束后，会在当前目录下生成一个damo/nlp_csanmt_translation_en2zh_base文件夹，里面包含了预训练模型。

## 微调数据集预处理

1. 英文数据集的预处理
```bash
bash tokenization_en.sh
subword-nmt apply-bpe -c damo/nlp_csanmt_translation_en2zh_base/bpe.en < train.en.tok > train.en.tok.bpe
```

2. 中文数据集的预处理
```bash
python tokenization_zh.py
subword-nmt apply-bpe -c damo/nlp_csanmt_translation_en2zh_base/bpe.zh < train.zh.tok > train.zh.tok.bpe
```

## 微调

1. 修改[finetuning_cfg.json](finetuning_cfg.json)的'trian'中参数
```json
    "train": {
        "num_gpus": 2, #这里的GPU数量可以根据实际情况进行调整
        "warmup_steps": 4000,
        "update_cycle": 1,
        "keep_checkpoint_max": 1,
        "confidence": 0.9,
        "optimizer": "adam",
        "adam_beta1": 0.9,
        "adam_beta2": 0.98,
        "adam_epsilon": 1e-9,
        "gradient_clip_norm": 0.0,
        "learning_rate_decay": "linear_warmup_rsqrt_decay",
        "initializer": "uniform_unit_scaling",
        "initializer_scale": 0.1,
        "learning_rate": 1e-1, #这里的学习率可以根据实际情况进行调整
        "train_batch_size_words": 1024,
        "scale_l1": 0.0,
        "scale_l2": 0.0,
        "train_max_len": 100, #这里的最大训练长度是指读取句子的长度。数值越大读取的句子越长，最好设置为512，太大显存会爆。
        "num_of_epochs": 200, #这里的训练轮数越大越好
        "save_checkpoints_steps": 500,
        "num_of_samples": 4,
        "eta": 0.6
    },
```

2. 运行[finetuning.py](finetuning.py)
```bash
python finetuning.py
```
这里需要注意的是，finetuning.py中第2行的`os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'`，这里的GPU数量需要与finetuning_cfg.json中的num_gpus参数一致。

**微调训练结束后，会在damo/nlp_csanmt_translation_en2zh_base文件夹下生成4个文件，分别是，'checkpoint'、'\*\*\*.data-00000-of-00001'、'\*\*\*.index'和'\*\*\*.meta'。将这4个文件复制替换到damo/nlp_csanmt_translation_en2zh_base/tf_ckpts文件夹内**

## 微调效果测试

修改[inference.py](inference.py)中待翻译的英文句子，然后运行
```bash
python inference.py
```
