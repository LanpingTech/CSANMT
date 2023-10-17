from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

input_sequence = "For applied mathematics, abstractions are based upon concepts of the calculus, not simple arithmetic operations encapsulated in programming languages like Fortran. John Rice's work in high-level components and languages [5], [2], intelligent interfaces [15], [11], [7], and problem-solving environments [5], [10] have served to push abstractions to higher and higher levels."

pipeline_ins = pipeline(task=Tasks.translation, model="nlp_csanmt_translation_en2zh_base")
outputs = pipeline_ins(input=input_sequence)

print(outputs['translation'])