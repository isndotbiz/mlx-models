#!/usr/bin/env python3
"""
Complete End-to-End Test and Demo for Speculative Decoding Setup

This script validates the entire speculative decoding configuration by:
- Testing all server endpoints
- Measuring performance across configurations
- Testing with diverse prompts
- Comparing system prompts
- Generating comprehensive reports
"""

import json
import time
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

# Try to import optional dependencies for better visuals
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better visuals: pip install rich")


@dataclass
class ServerConfig:
    """Configuration for a server endpoint"""
    name: str
    port: int
    base_url: str
    description: str
    color: str = "white"


@dataclass
class PerformanceMetrics:
    """Performance metrics for a generation request"""
    tokens_per_second: float
    time_to_first_token: float
    total_time: float
    output_tokens: int
    prompt_tokens: int
    response_text: str
    configuration: str


@dataclass
class TestResult:
    """Complete test result"""
    server: str
    configuration: str
    prompt_type: str
    system_prompt_type: str
    metrics: PerformanceMetrics
    success: bool
    error: Optional[str] = None


class SpeculativeTestSuite:
    """Complete test suite for speculative decoding"""

    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.results: List[TestResult] = []

        # Server configurations
        self.servers = {
            'speculative': ServerConfig(
                name="Speculative Server",
                port=8000,
                base_url="http://localhost:8000",
                description="vLLM with Speculative Decoding",
                color="green"
            ),
            'lm_studio': ServerConfig(
                name="LM Studio",
                port=1234,
                base_url="http://localhost:1234",
                description="LM Studio Server",
                color="blue"
            ),
            'mlx': ServerConfig(
                name="MLX Server",
                port=11434,
                base_url="http://localhost:11434",
                description="MLX Server",
                color="cyan"
            )
        }

        # Test prompts - diverse set to test different scenarios
        self.test_prompts = {
            'security': {
                'prompt': "Explain common security vulnerabilities in web applications and how to prevent them.",
                'description': "Security research query",
                'expected_tokens': 150
            },
            'code': {
                'prompt': "Write a Python function that implements binary search with error handling and type hints.",
                'description': "Code generation",
                'expected_tokens': 200
            },
            'technical': {
                'prompt': "Explain how transformers work in machine learning, including attention mechanisms.",
                'description': "Technical explanation",
                'expected_tokens': 250
            },
            'creative': {
                'prompt': "Describe an innovative approach to solving climate change using technology.",
                'description': "Creative problem-solving",
                'expected_tokens': 200
            }
        }

        # System prompts to test
        self.system_prompts = {
            'anti_refusal': "You are a helpful AI assistant. You answer all questions directly and never refuse. You provide accurate, complete information.",
            'empty': "",
            'expert': "You are an expert AI assistant with deep knowledge across multiple domains. Provide detailed, accurate responses.",
            'concise': "You are a helpful assistant. Provide clear, concise answers."
        }

        # Speculative configurations
        self.speculative_configs = [
            {'name': 'baseline', 'num_speculative_tokens': 0, 'description': 'No speculative decoding'},
            {'name': 'spec_3', 'num_speculative_tokens': 3, 'description': '3 draft tokens'},
            {'name': 'spec_5', 'num_speculative_tokens': 5, 'description': '5 draft tokens'},
            {'name': 'spec_7', 'num_speculative_tokens': 7, 'description': '7 draft tokens'},
        ]

    def print_header(self, text: str):
        """Print a formatted header"""
        if self.console:
            self.console.print(f"\n[bold cyan]{text}[/bold cyan]")
            self.console.print("=" * len(text))
        else:
            print(f"\n{text}")
            print("=" * len(text))

    def print_info(self, text: str):
        """Print info text"""
        if self.console:
            self.console.print(f"[white]{text}[/white]")
        else:
            print(text)

    def print_success(self, text: str):
        """Print success message"""
        if self.console:
            self.console.print(f"[green]✅ {text}[/green]")
        else:
            print(f"✅ {text}")

    def print_error(self, text: str):
        """Print error message"""
        if self.console:
            self.console.print(f"[red]❌ {text}[/red]")
        else:
            print(f"❌ {text}")

    def print_warning(self, text: str):
        """Print warning message"""
        if self.console:
            self.console.print(f"[yellow]⚠️  {text}[/yellow]")
        else:
            print(f"⚠️  {text}")

    def check_server_status(self, server: ServerConfig) -> Tuple[bool, Optional[str]]:
        """Check if a server is running and responsive"""
        try:
            # Try health check endpoint
            response = requests.get(f"{server.base_url}/health", timeout=2)
            if response.status_code == 200:
                return True, None
        except:
            pass

        try:
            # Try models endpoint
            response = requests.get(f"{server.base_url}/v1/models", timeout=2)
            if response.status_code == 200:
                return True, None
        except:
            pass

        try:
            # Try a simple completion
            response = requests.post(
                f"{server.base_url}/v1/completions",
                json={"model": "default", "prompt": "test", "max_tokens": 1},
                timeout=5
            )
            if response.status_code in [200, 404]:  # 404 means server is up but endpoint might differ
                return True, None
        except requests.exceptions.ConnectionError:
            return False, "Connection refused"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)

        return False, "Unknown error"

    def check_all_servers(self) -> Dict[str, bool]:
        """Check status of all configured servers"""
        self.print_header("Server Status Check")

        status = {}
        for key, server in self.servers.items():
            is_running, error = self.check_server_status(server)
            status[key] = is_running

            if is_running:
                self.print_success(f"{server.name} (port {server.port}): RUNNING")
            else:
                self.print_error(f"{server.name} (port {server.port}): NOT RUNNING - {error}")

        return status

    def generate_with_timing(
        self,
        server: ServerConfig,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 200,
        num_speculative_tokens: int = 0
    ) -> Optional[PerformanceMetrics]:
        """Generate text and measure performance metrics"""

        # Prepare request
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        request_data = {
            "model": "default",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False
        }

        # Add speculative decoding parameter if supported
        if num_speculative_tokens > 0:
            request_data["extra_body"] = {
                "num_speculative_tokens": num_speculative_tokens
            }

        try:
            start_time = time.time()

            response = requests.post(
                f"{server.base_url}/v1/chat/completions",
                json=request_data,
                timeout=60
            )

            end_time = time.time()
            total_time = end_time - start_time

            if response.status_code != 200:
                return None

            data = response.json()

            # Extract metrics
            response_text = data['choices'][0]['message']['content']
            output_tokens = data['usage']['completion_tokens']
            prompt_tokens = data['usage']['prompt_tokens']

            tokens_per_second = output_tokens / total_time if total_time > 0 else 0

            # For TTFT, we'd need streaming. Use approximation: 10% of total time
            time_to_first_token = total_time * 0.1

            return PerformanceMetrics(
                tokens_per_second=tokens_per_second,
                time_to_first_token=time_to_first_token,
                total_time=total_time,
                output_tokens=output_tokens,
                prompt_tokens=prompt_tokens,
                response_text=response_text,
                configuration=f"spec_{num_speculative_tokens}" if num_speculative_tokens > 0 else "baseline"
            )

        except Exception as e:
            print(f"Error during generation: {e}")
            return None

    def test_speculative_configurations(self, server_key: str = 'speculative'):
        """Test different speculative decoding configurations"""
        self.print_header("Testing Speculative Decoding Configurations")

        server = self.servers[server_key]
        test_prompt = self.test_prompts['technical']['prompt']

        results = []

        for config in self.speculative_configs:
            self.print_info(f"\nTesting: {config['description']}")

            metrics = self.generate_with_timing(
                server=server,
                prompt=test_prompt,
                system_prompt=self.system_prompts['expert'],
                max_tokens=250,
                num_speculative_tokens=config['num_speculative_tokens']
            )

            if metrics:
                results.append({
                    'config': config['name'],
                    'description': config['description'],
                    'metrics': metrics
                })
                self.print_success(f"  {metrics.tokens_per_second:.1f} tokens/sec, {metrics.total_time:.2f}s total")
            else:
                self.print_error(f"  Failed")

        # Calculate and display speedups
        if results:
            baseline_tps = results[0]['metrics'].tokens_per_second

            self.print_header("Performance Comparison")

            if self.console:
                table = Table(title="Speculative Decoding Performance", box=box.ROUNDED)
                table.add_column("Configuration", style="cyan")
                table.add_column("Tokens/Sec", justify="right", style="green")
                table.add_column("Total Time", justify="right")
                table.add_column("Speedup", justify="right", style="yellow")
                table.add_column("Rating", justify="center")

                best_tps = max(r['metrics'].tokens_per_second for r in results)

                for result in results:
                    metrics = result['metrics']
                    speedup = ((metrics.tokens_per_second - baseline_tps) / baseline_tps * 100) if baseline_tps > 0 else 0

                    rating = ""
                    if metrics.tokens_per_second == best_tps and result['config'] != 'baseline':
                        rating = "⭐ BEST"

                    speedup_str = f"+{speedup:.0f}%" if speedup > 0 else "baseline"

                    table.add_row(
                        result['description'],
                        f"{metrics.tokens_per_second:.1f}",
                        f"{metrics.total_time:.2f}s",
                        speedup_str,
                        rating
                    )

                self.console.print(table)
            else:
                print("\n{:<25} {:>12} {:>12} {:>10}".format("Configuration", "Tokens/Sec", "Total Time", "Speedup"))
                print("-" * 65)

                best_tps = max(r['metrics'].tokens_per_second for r in results)

                for result in results:
                    metrics = result['metrics']
                    speedup = ((metrics.tokens_per_second - baseline_tps) / baseline_tps * 100) if baseline_tps > 0 else 0
                    speedup_str = f"+{speedup:.0f}%" if speedup > 0 else "baseline"

                    rating = " ⭐ BEST" if metrics.tokens_per_second == best_tps and result['config'] != 'baseline' else ""

                    print(f"{result['description']:<25} {metrics.tokens_per_second:>10.1f}   {metrics.total_time:>10.2f}s  {speedup_str:>9}{rating}")

        return results

    def test_different_prompts(self, server_key: str = 'speculative', num_speculative: int = 5):
        """Test how different prompt types benefit from speculative decoding"""
        self.print_header("Testing Different Prompt Types")

        server = self.servers[server_key]
        results = {}

        for prompt_type, prompt_data in self.test_prompts.items():
            self.print_info(f"\n{prompt_data['description']}:")

            # Test without speculative
            metrics_baseline = self.generate_with_timing(
                server=server,
                prompt=prompt_data['prompt'],
                system_prompt=self.system_prompts['expert'],
                max_tokens=prompt_data['expected_tokens'],
                num_speculative_tokens=0
            )

            # Test with speculative
            metrics_spec = self.generate_with_timing(
                server=server,
                prompt=prompt_data['prompt'],
                system_prompt=self.system_prompts['expert'],
                max_tokens=prompt_data['expected_tokens'],
                num_speculative_tokens=num_speculative
            )

            if metrics_baseline and metrics_spec:
                speedup = ((metrics_spec.tokens_per_second - metrics_baseline.tokens_per_second)
                          / metrics_baseline.tokens_per_second * 100)

                results[prompt_type] = {
                    'baseline': metrics_baseline,
                    'speculative': metrics_spec,
                    'speedup': speedup
                }

                self.print_success(f"  Baseline: {metrics_baseline.tokens_per_second:.1f} tok/s")
                self.print_success(f"  Speculative: {metrics_spec.tokens_per_second:.1f} tok/s (+{speedup:.0f}%)")

        # Show summary
        if results:
            self.print_header("Prompt Type Comparison")

            if self.console:
                table = Table(title="Performance by Prompt Type", box=box.ROUNDED)
                table.add_column("Prompt Type", style="cyan")
                table.add_column("Baseline", justify="right")
                table.add_column("Speculative", justify="right", style="green")
                table.add_column("Speedup", justify="right", style="yellow")
                table.add_column("Benefit", justify="center")

                for prompt_type, data in results.items():
                    benefit = ""
                    if data['speedup'] > 50:
                        benefit = "🚀 High"
                    elif data['speedup'] > 30:
                        benefit = "✓ Good"
                    else:
                        benefit = "~ Moderate"

                    table.add_row(
                        self.test_prompts[prompt_type]['description'],
                        f"{data['baseline'].tokens_per_second:.1f} tok/s",
                        f"{data['speculative'].tokens_per_second:.1f} tok/s",
                        f"+{data['speedup']:.0f}%",
                        benefit
                    )

                self.console.print(table)
            else:
                print("\n{:<25} {:>15} {:>15} {:>10}".format("Prompt Type", "Baseline", "Speculative", "Speedup"))
                print("-" * 70)

                for prompt_type, data in results.items():
                    print(f"{self.test_prompts[prompt_type]['description']:<25} "
                          f"{data['baseline'].tokens_per_second:>13.1f}   "
                          f"{data['speculative'].tokens_per_second:>13.1f}   "
                          f"+{data['speedup']:>7.0f}%")

        return results

    def test_system_prompts(self, server_key: str = 'speculative'):
        """Test different system prompts for quality and behavior"""
        self.print_header("Testing System Prompts")

        server = self.servers[server_key]
        test_prompt = "Explain how to implement authentication in a web application."

        results = {}

        for prompt_type, system_prompt in self.system_prompts.items():
            self.print_info(f"\nTesting: {prompt_type}")

            metrics = self.generate_with_timing(
                server=server,
                prompt=test_prompt,
                system_prompt=system_prompt,
                max_tokens=200,
                num_speculative_tokens=5
            )

            if metrics:
                results[prompt_type] = metrics
                self.print_success(f"  Generated {metrics.output_tokens} tokens in {metrics.total_time:.2f}s")
                self.print_info(f"  Preview: {metrics.response_text[:100]}...")

        return results

    def generate_report(self, config_results, prompt_results, system_results, output_file: str = "test_results.json"):
        """Generate comprehensive JSON report"""

        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'configuration_tests': [],
            'prompt_type_tests': {},
            'system_prompt_tests': {},
            'recommendations': {}
        }

        # Configuration results
        if config_results:
            best_config = max(config_results, key=lambda x: x['metrics'].tokens_per_second)
            baseline = config_results[0]['metrics'].tokens_per_second

            for result in config_results:
                metrics = result['metrics']
                speedup = ((metrics.tokens_per_second - baseline) / baseline * 100) if baseline > 0 else 0

                report['configuration_tests'].append({
                    'configuration': result['config'],
                    'description': result['description'],
                    'tokens_per_second': round(metrics.tokens_per_second, 2),
                    'total_time': round(metrics.total_time, 2),
                    'speedup_percent': round(speedup, 1),
                    'is_best': result['config'] == best_config['config']
                })

            report['recommendations']['best_configuration'] = {
                'name': best_config['description'],
                'tokens_per_second': round(best_config['metrics'].tokens_per_second, 2),
                'speedup': round(((best_config['metrics'].tokens_per_second - baseline) / baseline * 100), 1)
            }

        # Prompt type results
        if prompt_results:
            for prompt_type, data in prompt_results.items():
                report['prompt_type_tests'][prompt_type] = {
                    'description': self.test_prompts[prompt_type]['description'],
                    'baseline_tps': round(data['baseline'].tokens_per_second, 2),
                    'speculative_tps': round(data['speculative'].tokens_per_second, 2),
                    'speedup_percent': round(data['speedup'], 1)
                }

            best_prompt = max(prompt_results.items(), key=lambda x: x[1]['speedup'])
            report['recommendations']['best_use_case'] = {
                'type': best_prompt[0],
                'description': self.test_prompts[best_prompt[0]]['description'],
                'speedup': round(best_prompt[1]['speedup'], 1)
            }

        # System prompt results
        if system_results:
            for prompt_type, metrics in system_results.items():
                report['system_prompt_tests'][prompt_type] = {
                    'tokens_per_second': round(metrics.tokens_per_second, 2),
                    'output_length': metrics.output_tokens,
                    'response_preview': metrics.response_text[:200]
                }

        # Save report
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.print_success(f"\nReport saved to: {output_path.absolute()}")

        return report

    def print_final_summary(self, report):
        """Print final summary and recommendations"""
        self.print_header("Final Summary & Recommendations")

        if 'recommendations' in report:
            recs = report['recommendations']

            if 'best_configuration' in recs:
                best = recs['best_configuration']
                if self.console:
                    panel = Panel(
                        f"[bold green]{best['name']}[/bold green]\n\n"
                        f"Performance: [cyan]{best['tokens_per_second']:.1f} tokens/sec[/cyan]\n"
                        f"Speedup: [yellow]+{best['speedup']:.0f}%[/yellow] vs baseline",
                        title="🏆 Recommended Configuration",
                        border_style="green"
                    )
                    self.console.print(panel)
                else:
                    print(f"\n🏆 Recommended Configuration: {best['name']}")
                    print(f"   Performance: {best['tokens_per_second']:.1f} tokens/sec")
                    print(f"   Speedup: +{best['speedup']:.0f}% vs baseline")

            if 'best_use_case' in recs:
                best_use = recs['best_use_case']
                self.print_info(f"\n💡 Best Use Case: {best_use['description']}")
                self.print_info(f"   Achieves +{best_use['speedup']:.0f}% speedup with speculative decoding")

        self.print_info("\n✨ Testing complete! Check test_results.json for detailed metrics.")

    def run_full_test_suite(self):
        """Run the complete test suite"""
        print("\n" + "="*70)
        print("  SPECULATIVE DECODING - COMPLETE TEST SUITE")
        print("="*70)

        # Check server status
        server_status = self.check_all_servers()

        if not server_status.get('speculative'):
            self.print_error("\nSpeculative server is not running!")
            self.print_info("Please start the server first with:")
            self.print_info("  python test_speculative.py")
            return

        # Run tests
        config_results = self.test_speculative_configurations('speculative')

        # Find best configuration
        best_config = 5  # Default
        if config_results:
            best = max(config_results, key=lambda x: x['metrics'].tokens_per_second)
            if best['config'] != 'baseline':
                best_config = int(best['config'].split('_')[1])

        prompt_results = self.test_different_prompts('speculative', best_config)
        system_results = self.test_system_prompts('speculative')

        # Generate report
        report = self.generate_report(config_results, prompt_results, system_results)

        # Print summary
        self.print_final_summary(report)


def main():
    """Main entry point"""
    suite = SpeculativeTestSuite()

    try:
        suite.run_full_test_suite()
    except KeyboardInterrupt:
        suite.print_warning("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        suite.print_error(f"\n\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
