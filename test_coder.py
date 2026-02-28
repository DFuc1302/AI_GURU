from orchestrator_level3 import run_pipeline

problem = "Tính đạo hàm của f(x)=3*x^3 - 4*x^2 + 2*x - 7"
result = run_pipeline(problem, language="python")

for k, v in result.items():
    print(k, ":\n", v)