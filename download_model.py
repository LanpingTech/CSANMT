from modelscope.hub.snapshot_download import snapshot_download

model_dir = snapshot_download('damo/nlp_csanmt_translation_en2zh_base', cache_dir='.', revision='v1.0.1')