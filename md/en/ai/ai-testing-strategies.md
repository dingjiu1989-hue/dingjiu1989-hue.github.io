---
title: "Testing Strategies for AI Applications"
description: "Implement robust AI testing with evaluation datasets, regression testing, A/B evaluation, hallucination detection, prompt testing, and performance benchmarking."
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-testing-strategies.html
---

# Testing Strategies for AI Applications

##  Introduction

  


Testing AI applications differs fundamentally from testing deterministic software. Model outputs are probabilistic, edge cases are infinite, and a passing unit test does not guarantee correct behavior in production. A comprehensive AI testing strategy combines traditional software testing with AI-specific evaluation methodologies to catch regressions, hallucinations, and performance degradations before they reach users.

  


##  Evaluation Datasets

  


Curate high-quality evaluation datasets that reflect real-world usage:

  

    
    
    from dataclasses import dataclass
    
    from typing import List, Callable
    
    import json
    
    
    
    @dataclass
    
    class TestCase:
    
        id: str
    
        input: str
    
        expected_output: str
    
        domain: str
    
        difficulty: str  # "easy", "medium", "hard"
    
        tags: List[str]
    
        # For non-deterministic evaluation
    
        criteria: List[Callable[[str], bool]]
    
    
    
    class EvalDataset:
    
        def __init__(self, name: str):
    
            self.name = name
    
            self.test_cases: List[TestCase] = []
    
    
    
        def add_golden_set(self, path: str):
    
            """Load curated golden test cases."""
    
            with open(path) as f:
    
                data = json.load(f)
    
            for item in data:
    
                self.test_cases.append(TestCase(
    
                    id=item["id"],
    
                    input=item["input"],
    
                    expected_output=item["expected_output"],
    
                    domain=item.get("domain", "general"),
    
                    difficulty=item.get("difficulty", "medium"),
    
                    tags=item.get("tags", []),
    
                    criteria=[
    
                        lambda output, expected=item["expected_output"]:
    
                            expected.lower() in output.lower(),
    
                    ],
    
                ))
    
    
    
        def add_adversarial(self, path: str):
    
            """Load adversarial test cases (edge cases, jailbreaks)."""
    
            with open(path) as f:
    
                data = json.load(f)
    
            for item in data:
    
                self.test_cases.append(TestCase(
    
                    id=f"adv_{item['id']}",
    
                    input=item["input"],
    
                    expected_output="",
    
                    domain="adversarial",
    
                    difficulty="hard",
    
                    tags=["adversarial"],
    
                    criteria=[
    
                        lambda output:
    
                            "I cannot" in output or "I'm unable" in output,
    
                    ],
    
                ))
    
    

  


##  Regression Testing

  


Automated regression testing catches model behavior changes:

  

    
    
    class ModelRegressionTest:
    
        def __init__(self, eval_dataset: EvalDataset):
    
            self.dataset = eval_dataset
    
            self.results_history: List[dict] = []
    
    
    
        async def run_regression_suite(
    
            self,
    
            model_name: str,
    
            previous_results: dict = None,
    
        ) -> dict:
    
            results = {
    
                "model": model_name,
    
                "timestamp": datetime.utcnow().isoformat(),
    
                "total": len(self.dataset.test_cases),
    
                "passed": 0,
    
                "failed": 0,
    
                "failures": [],
    
                "score": 0.0,
    
            }
    
    
    
            for test_case in self.dataset.test_cases:
    
                try:
    
                    output = await self._invoke_model(model_name, test_case.input)
    
    
    
                    # Evaluate against all criteria
    
                    passed = all(
    
                        criterion(output) for criterion in test_case.criteria
    
                    )
    
    
    
                    if passed:
    
                        results["passed"] += 1
    
                    else:
    
                        results["failed"] += 1
    
                        results["failures"].append({
    
                            "id": test_case.id,
    
                            "input": test_case.input,
    
                            "expected": test_case.expected_output,
    
                            "actual": output,
    
                            "domain": test_case.domain,
    
                        })
    
                except Exception as e:
    
                    results["failed"] += 1
    
                    results["failures"].append({
    
                        "id": test_case.id,
    
                        "error": str(e),
    
                    })
    
    
    
            results["score"] = results["passed"] / results["total"]
    
    
    
            # Compare with previous run
    
            if previous_results:
    
                score_delta = results["score"] - previous_results["score"]
    
                results["regression"] = score_delta < -0.02
    
                results["score_delta"] = score_delta
    
    
    
            return results
    
    
    
        def fail_pipeline_if_regression(self, results: dict):
    
            """Fail CI if model regressed beyond threshold."""
    
            if results.get("regression", False):
    
                raise Exception(
    
                    f"Model regression detected! "
    
                    f"Score dropped from "
    
                    f"{results.get('previous_score', 1.0):.2%} to "
    
                    f"{results['score']:.2%}"
    
                )
    
    

  


##  A/B Evaluation

  


Compare model versions side by side with structured evaluation:

  

    
    
    class ABEvaluation:
    
        def __init__(self, judge_model: str = "claude-opus-4-20260512"):
    
            self.judge = judge_model
    
    
    
        async def evaluate_pair(
    
            self,
    
            prompt: str,
    
            output_a: str,
    
            output_b: str,
    
            criteria: List[str],
    
        ) -> dict:
    
            """Use an independent judge model to compare outputs."""
    
            evaluation_prompt = f"""
    
    Compare these two AI responses to the same prompt.
    
    
    
    Prompt: "{prompt}"
    
    
    
    Response A: "{output_a}"
    
    Response B: "{output_b}"
    
    
    
    Evaluate on these criteria: {', '.join(criteria)}
    
    
    
    For each criterion, state which response is better (A, B, or tie)
    
    and provide a brief justification.
    
    """
    
    
    
            response = client.messages.create(
    
                model=self.judge,
    
                max_tokens=1024,
    
                messages=[{"role": "user", "content": evaluation_prompt}],
    
            )
    
    
    
            return self._parse_evaluation(response.content[0].text)
    
    
    
        async def batch_evaluate(
    
            self,
    
            prompts: List[str],
    
            model_a: str,
    
            model_b: str,
    
            criteria: List[str],
    
        ) -> dict:
    
            results = {"model_a_wins": 0, "model_b_wins": 0, "ties": 0}
    
    
    
            for prompt in prompts:
    
                output_a = await self._invoke(model_a, prompt)
    
                output_b = await self._invoke(model_b, prompt)
    
    
    
                evaluation = await self.evaluate_pair(
    
                    prompt, output_a, output_b, criteria
    
                )
    
    
    
                # Aggregate across criteria
    
                winner = evaluation["winner"]
    
                results[f"{winner}_wins"] += 1
    
    
    
            results["total"] = len(prompts)
    
            results["a_win_rate"] = results["model_a_wins"] / results["total"]
    
            results["b_win_rate"] = results["model_b_wins"] / results["total"]
    
    
    
            return results
    
    

  


##  Hallucination Detection

  


Automated hallucination checks verify factual accuracy:

  

    
    
    class HallucinationDetector:
    
        def __init__(self, knowledge_base: Callable):
    
            self.kb = knowledge_base
    
    
    
        async def check_factual_claims(self, output: str) -> List[dict]:
    
            """Extract factual claims and verify them against a knowledge base."""
    
            # 1. Extract atomic claims
    
            claims = await self._extract_claims(output)
    
    
    
            verified_claims = []
    
            for claim in claims:
    
                # 2. Search knowledge base
    
                evidence = await self.kb.search(claim["text"])
    
    
    
                # 3. Verify claim against evidence
    
                verification = await self._verify_claim(
    
                    claim["text"],
    
                    evidence,
    
                    claim["context"],
    
                )
    
    
    
                verified_claims.append({
    
                    "claim": claim["text"],
    
                    "confidence": verification["confidence"],
    
                    "supported": verification["supported"],
    
                    "evidence": evidence[:3],
    
                    "context": claim["context"],
    
                })
    
    
    
            return verified_claims
    
    
    
        async def _verify_claim(
    
            self,
    
            claim: str,
    
            evidence: List[str],
    
            context: str,
    
        ) -> dict:
    
            prompt = f"""
    
    Claim: "{claim}"
    
    Context: "{context}"
    
    Evidence: {' '.join(evidence[:3])}
    
    
    
    Is this claim supported by the evidence?
    
    Respond with JSON:
    
    {{"supported": bool, "confidence": 0.0-1.0, "reasoning": "..."}}
    
    """
    
            response = await self._llm_call(prompt)
    
            return json.loads(response)
    
    
    
        def compute_hallucination_rate(
    
            self, verified_claims: List[dict]
    
        ) -> float:
    
            unsupported = sum(
    
                1 for c in verified_claims if not c["supported"]
    
            )
    
            total = len(verified_claims)
    
            return unsupported / total if total > 0 else 0.0
    
    

  


##  Prompt Testing

  


Version-control prompts with structured testing:

  

    
    
    class PromptRegistry:
    
        def __init__(self):
    
            self.prompts = {}
    
    
    
        def register(
    
            self,
    
            name: str,
    
            template: str,
    
            version: str,
    
            tests: List[Callable] = None,
    
        ):
    
            self.prompts[name] = {
    
                "template": template,
    
                "version": version,
    
                "tests": tests or [],
    
                "performance": [],
    
            }
    
    
    
        async def test_prompt(
    
            self, name: str, test_cases: List[dict]
    
        ) -> dict:
    
            prompt = self.prompts[name]
    
            results = []
    
    
    
            for case in test_cases:
    
                # Render template with test inputs
    
                rendered = prompt["template"].format(**case["inputs"])
    
                output = await self._invoke(rendered)
    
    
    
                # Run tests
    
                test_results = [
    
                    test(output) for test in prompt["tests"]
    
                ]
    
    
    
                results.append({
    
                    "case": case["name"],
    
                    "output": output,
    
                    "tests_passed": all(test_results),
    
                    "test_details": test_results,
    
                })
    
    
    
            return {
    
                "prompt": name,
    
                "version": prompt["version"],
    
                "pass_rate": sum(r["tests_passed"] for r in results) / len(results),
    
                "results": results,
    
            }
    
    

  


##  Performance Testing

  


Benchmark latency, throughput, and cost across model versions:

  

    
    
    class AIPerformanceTest:
    
        async def benchmark(
    
            self,
    
            model: str,
    
            concurrency: int = 10,
    
            requests: int = 100,
    
        ) -> dict:
    
            import time
    
            import asyncio
    
    
    
            semaphore = asyncio.Semaphore(concurrency)
    
            latencies = []
    
    
    
            async def single_request():
    
                async with semaphore:
    
                    start = time.monotonic()
    
                    await self._invoke_model(model, "Test prompt")
    
                    latencies.append(time.monotonic() - start)
    
    
    
            tasks = [single_request() for _ in range(requests)]
    
            await asyncio.gather(*tasks)
    
    
    
            latencies.sort()
    
            return {
    
                "model": model,
    
                "p50": latencies[len(latencies) // 2],
    
                "p95": latencies[int(len(latencies) * 0.95)],
    
                "p99": latencies[int(len(latencies) * 0.99)],
    
                "avg": sum(latencies) / len(latencies),
    
                "throughput": requests / sum(latencies),
    
                "total_cost": self._calculate_cost(model, requests),
    
            }
    
    

  


A mature AI testing pipeline runs golden set regression on every PR, A/B evaluations before model upgrades, hallucination detection on every production response, and performance benchmarks weekly. No single metric captures model quality; combine automated tests with human evaluation for production releases.
