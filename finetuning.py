import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"

from modelscope.trainers.nlp import CsanmtTranslationTrainer

trainer = CsanmtTranslationTrainer(model="damo/nlp_csanmt_translation_en2zh_base/", cfg_file='finetuning_cfg.json')
trainer.train()

