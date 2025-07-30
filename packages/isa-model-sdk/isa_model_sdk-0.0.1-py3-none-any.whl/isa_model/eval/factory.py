"""
Unified Evaluation Factory for ISA Model Framework

This factory provides a single interface for all evaluation operations:
- LLM evaluation (perplexity, BLEU, ROUGE, custom metrics)
- Image model evaluation (FID, IS, LPIPS)
- Benchmark testing (MMLU, HellaSwag, ARC, etc.)
- Custom evaluation pipelines
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import datetime

from .metrics import LLMMetrics, ImageMetrics, BenchmarkRunner
from .benchmarks import MMLU, HellaSwag, ARC, GSM8K

logger = logging.getLogger(__name__)


class EvaluationFactory:
    """
    Unified factory for all AI model evaluation operations.
    
    This class provides simplified interfaces for:
    - LLM evaluation with various metrics
    - Image model evaluation
    - Benchmark testing on standard datasets
    - Custom evaluation pipelines
    
    Example usage:
        ```python
        from isa_model.eval import EvaluationFactory
        
        evaluator = EvaluationFactory()
        
        # Evaluate LLM on custom dataset
        results = evaluator.evaluate_llm(
            model_path="path/to/model",
            dataset_path="test_data.json",
            metrics=["perplexity", "bleu", "rouge"],
            output_dir="eval_results"
        )
        
        # Run MMLU benchmark
        mmlu_results = evaluator.run_benchmark(
            model_path="path/to/model",
            benchmark="mmlu",
            subjects=["math", "physics", "chemistry"]
        )
        
        # Compare multiple models
        comparison = evaluator.compare_models([
            "model1/path",
            "model2/path"
        ], benchmark="hellaswag")
        ```
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the evaluation factory.
        
        Args:
            output_dir: Base directory for evaluation outputs
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), "evaluation_results")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize metrics calculators
        self.llm_metrics = LLMMetrics()
        self.image_metrics = ImageMetrics()
        self.benchmark_runner = BenchmarkRunner()
        
        logger.info(f"EvaluationFactory initialized with output dir: {self.output_dir}")
    
    def _get_output_path(self, model_name: str, eval_type: str) -> str:
        """Generate timestamped output path for evaluation results."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_model_name = os.path.basename(model_name).replace("/", "_").replace(":", "_")
        filename = f"{safe_model_name}_{eval_type}_{timestamp}.json"
        return os.path.join(self.output_dir, filename)
    
    # =================
    # LLM Evaluation Methods
    # =================
    
    def evaluate_llm(
        self,
        model_path: str,
        dataset_path: str,
        metrics: List[str] = None,
        output_path: Optional[str] = None,
        batch_size: int = 8,
        max_samples: Optional[int] = None,
        provider: str = "ollama",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate an LLM model on a dataset with specified metrics.
        
        Args:
            model_path: Path to the model or model identifier
            dataset_path: Path to evaluation dataset (JSON format)
            metrics: List of metrics to compute ["perplexity", "bleu", "rouge", "accuracy"]
            output_path: Path to save results
            batch_size: Batch size for evaluation
            max_samples: Maximum number of samples to evaluate
            provider: Model provider ("ollama", "openai", "hf")
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing evaluation results
            
        Example:
            ```python
            results = evaluator.evaluate_llm(
                model_path="google/gemma-2-4b-it",
                dataset_path="test_data.json",
                metrics=["perplexity", "bleu", "rouge"],
                max_samples=1000
            )
            ```
        """
        if metrics is None:
            metrics = ["perplexity", "bleu", "rouge"]
        
        if not output_path:
            output_path = self._get_output_path(model_path, "llm_eval")
        
        logger.info(f"Evaluating LLM {model_path} with metrics: {metrics}")
        
        # Load dataset
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)
        
        if max_samples:
            dataset = dataset[:max_samples]
        
        # Run evaluation
        results = self.llm_metrics.evaluate(
            model_path=model_path,
            dataset=dataset,
            metrics=metrics,
            batch_size=batch_size,
            provider=provider,
            **kwargs
        )
        
        # Add metadata
        results["metadata"] = {
            "model_path": model_path,
            "dataset_path": dataset_path,
            "metrics": metrics,
            "num_samples": len(dataset),
            "timestamp": datetime.datetime.now().isoformat(),
            "provider": provider
        }
        
        # Save results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evaluation results saved to: {output_path}")
        return results
    
    def evaluate_generation_quality(
        self,
        model_path: str,
        prompts: List[str],
        reference_texts: List[str] = None,
        metrics: List[str] = None,
        output_path: Optional[str] = None,
        provider: str = "ollama",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate text generation quality.
        
        Args:
            model_path: Path to the model
            prompts: List of input prompts
            reference_texts: Reference texts for comparison (optional)
            metrics: Metrics to compute
            output_path: Output path for results
            provider: Model provider
            **kwargs: Additional parameters
            
        Returns:
            Evaluation results dictionary
        """
        if metrics is None:
            metrics = ["diversity", "coherence", "fluency"]
        
        if not output_path:
            output_path = self._get_output_path(model_path, "generation_eval")
        
        results = self.llm_metrics.evaluate_generation(
            model_path=model_path,
            prompts=prompts,
            reference_texts=reference_texts,
            metrics=metrics,
            provider=provider,
            **kwargs
        )
        
        # Save results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    # =================
    # Benchmark Testing Methods
    # =================
    
    def run_benchmark(
        self,
        model_path: str,
        benchmark: str,
        output_path: Optional[str] = None,
        num_shots: int = 0,
        max_samples: Optional[int] = None,
        provider: str = "ollama",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a standard benchmark test.
        
        Args:
            model_path: Path to the model
            benchmark: Benchmark name ("mmlu", "hellaswag", "arc", "gsm8k")
            output_path: Output path for results
            num_shots: Number of few-shot examples
            max_samples: Maximum samples to evaluate
            provider: Model provider
            **kwargs: Additional parameters
            
        Returns:
            Benchmark results dictionary
            
        Example:
            ```python
            mmlu_results = evaluator.run_benchmark(
                model_path="google/gemma-2-4b-it",
                benchmark="mmlu",
                num_shots=5,
                max_samples=1000
            )
            ```
        """
        if not output_path:
            output_path = self._get_output_path(model_path, f"{benchmark}_benchmark")
        
        logger.info(f"Running {benchmark} benchmark on {model_path}")
        
        # Select benchmark
        benchmark_map = {
            "mmlu": MMLU(),
            "hellaswag": HellaSwag(),
            "arc": ARC(),
            "gsm8k": GSM8K()
        }
        
        if benchmark.lower() not in benchmark_map:
            raise ValueError(f"Unsupported benchmark: {benchmark}")
        
        benchmark_instance = benchmark_map[benchmark.lower()]
        
        # Run benchmark
        results = self.benchmark_runner.run(
            benchmark=benchmark_instance,
            model_path=model_path,
            num_shots=num_shots,
            max_samples=max_samples,
            provider=provider,
            **kwargs
        )
        
        # Add metadata
        results["metadata"] = {
            "model_path": model_path,
            "benchmark": benchmark,
            "num_shots": num_shots,
            "max_samples": max_samples,
            "timestamp": datetime.datetime.now().isoformat(),
            "provider": provider
        }
        
        # Save results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Benchmark results saved to: {output_path}")
        return results
    
    def run_multiple_benchmarks(
        self,
        model_path: str,
        benchmarks: List[str] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run multiple benchmarks on a model.
        
        Args:
            model_path: Path to the model
            benchmarks: List of benchmark names
            output_dir: Directory to save results
            **kwargs: Additional parameters
            
        Returns:
            Combined results dictionary
        """
        if benchmarks is None:
            benchmarks = ["mmlu", "hellaswag", "arc"]
        
        if not output_dir:
            output_dir = os.path.join(self.output_dir, "multi_benchmark")
            os.makedirs(output_dir, exist_ok=True)
        
        all_results = {}
        
        for benchmark in benchmarks:
            try:
                output_path = os.path.join(output_dir, f"{benchmark}_results.json")
                results = self.run_benchmark(
                    model_path=model_path,
                    benchmark=benchmark,
                    output_path=output_path,
                    **kwargs
                )
                all_results[benchmark] = results
            except Exception as e:
                logger.error(f"Failed to run benchmark {benchmark}: {e}")
                all_results[benchmark] = {"error": str(e)}
        
        # Save combined results
        combined_path = os.path.join(output_dir, "combined_results.json")
        with open(combined_path, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        return all_results
    
    # =================
    # Model Comparison Methods
    # =================
    
    def compare_models(
        self,
        model_paths: List[str],
        dataset_path: Optional[str] = None,
        benchmark: Optional[str] = None,
        metrics: List[str] = None,
        output_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compare multiple models on the same evaluation.
        
        Args:
            model_paths: List of model paths to compare
            dataset_path: Path to evaluation dataset
            benchmark: Benchmark name for comparison
            metrics: Metrics to compute
            output_path: Output path for comparison results
            **kwargs: Additional parameters
            
        Returns:
            Comparison results dictionary
        """
        if not output_path:
            output_path = self._get_output_path("model_comparison", "comparison")
        
        comparison_results = {
            "models": model_paths,
            "results": {},
            "summary": {}
        }
        
        # Run evaluation for each model
        for model_path in model_paths:
            model_name = os.path.basename(model_path)
            logger.info(f"Evaluating model: {model_name}")
            
            try:
                if dataset_path:
                    # Custom dataset evaluation
                    results = self.evaluate_llm(
                        model_path=model_path,
                        dataset_path=dataset_path,
                        metrics=metrics,
                        **kwargs
                    )
                elif benchmark:
                    # Benchmark evaluation
                    results = self.run_benchmark(
                        model_path=model_path,
                        benchmark=benchmark,
                        **kwargs
                    )
                else:
                    raise ValueError("Either dataset_path or benchmark must be provided")
                
                comparison_results["results"][model_name] = results
                
            except Exception as e:
                logger.error(f"Failed to evaluate {model_name}: {e}")
                comparison_results["results"][model_name] = {"error": str(e)}
        
        # Generate summary
        comparison_results["summary"] = self._generate_comparison_summary(
            comparison_results["results"]
        )
        
        # Save results
        with open(output_path, 'w') as f:
            json.dump(comparison_results, f, indent=2)
        
        return comparison_results
    
    def _generate_comparison_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for model comparison."""
        summary = {
            "best_performing": {},
            "rankings": {},
            "average_scores": {}
        }
        
        # Extract key metrics and find best performing models
        for model_name, model_results in results.items():
            if "error" in model_results:
                continue
                
            # Extract main scores (this is simplified - would need more sophisticated logic)
            if "accuracy" in model_results:
                summary["average_scores"][model_name] = model_results["accuracy"]
            elif "overall_score" in model_results:
                summary["average_scores"][model_name] = model_results["overall_score"]
        
        # Rank models by performance
        if summary["average_scores"]:
            ranked = sorted(
                summary["average_scores"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            summary["rankings"] = {i+1: model for i, (model, score) in enumerate(ranked)}
            summary["best_performing"]["model"] = ranked[0][0]
            summary["best_performing"]["score"] = ranked[0][1]
        
        return summary
    
    # =================
    # Image Model Evaluation Methods
    # =================
    
    def evaluate_image_model(
        self,
        model_path: str,
        test_images_dir: str,
        reference_images_dir: Optional[str] = None,
        metrics: List[str] = None,
        output_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate image generation model.
        
        Args:
            model_path: Path to the image model
            test_images_dir: Directory with test images
            reference_images_dir: Directory with reference images
            metrics: Metrics to compute ["fid", "is", "lpips"]
            output_path: Output path for results
            **kwargs: Additional parameters
            
        Returns:
            Image evaluation results
        """
        if metrics is None:
            metrics = ["fid", "is"]
        
        if not output_path:
            output_path = self._get_output_path(model_path, "image_eval")
        
        results = self.image_metrics.evaluate(
            model_path=model_path,
            test_images_dir=test_images_dir,
            reference_images_dir=reference_images_dir,
            metrics=metrics,
            **kwargs
        )
        
        # Save results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    # =================
    # Utility Methods
    # =================
    
    def load_results(self, results_path: str) -> Dict[str, Any]:
        """Load evaluation results from file."""
        with open(results_path, 'r') as f:
            return json.load(f)
    
    def list_evaluation_results(self) -> List[Dict[str, Any]]:
        """List all evaluation results in the output directory."""
        results = []
        
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.output_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            results.append({
                                "filename": filename,
                                "path": filepath,
                                "metadata": data.get("metadata", {}),
                                "created": datetime.datetime.fromtimestamp(
                                    os.path.getctime(filepath)
                                ).isoformat()
                            })
                    except Exception as e:
                        logger.warning(f"Failed to load {filename}: {e}")
        
        return sorted(results, key=lambda x: x["created"], reverse=True)
    
    def generate_report(
        self,
        results_paths: List[str],
        output_path: Optional[str] = None,
        format: str = "json"
    ) -> str:
        """
        Generate evaluation report from multiple results.
        
        Args:
            results_paths: List of result file paths
            output_path: Output path for report
            format: Report format ("json", "html", "markdown")
            
        Returns:
            Path to generated report
        """
        if not output_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"evaluation_report_{timestamp}.{format}")
        
        # Load all results
        all_results = []
        for path in results_paths:
            try:
                results = self.load_results(path)
                all_results.append(results)
            except Exception as e:
                logger.warning(f"Failed to load results from {path}: {e}")
        
        # Generate report based on format
        if format == "json":
            report_data = {
                "report_generated": datetime.datetime.now().isoformat(),
                "num_evaluations": len(all_results),
                "results": all_results
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
        
        # TODO: Implement HTML and Markdown report generation
        
        logger.info(f"Evaluation report generated: {output_path}")
        return output_path 