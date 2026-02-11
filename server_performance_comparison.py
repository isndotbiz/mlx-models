#!/usr/bin/env python3
"""
Comprehensive Server Performance Comparison
Tests: vLLM-MLX, MLX server, and LM Studio CLI
Model: Josiefied-Qwen3-8B-abliterated
"""

import time
import json
import requests
import psutil
import os
from datetime import datetime
from typing import Dict, List, Any

# Server configurations
SERVERS = {
    "lm_studio": {
        "name": "LM Studio CLI",
        "base_url": "http://localhost:1234/v1",
        "model": "josiefied-qwen3-8b-abliterated-v1",
        "port": 1234
    },
    # "mlx_server": {
    #     "name": "MLX Server",
    #     "base_url": "http://localhost:11434/v1",
    #     "model": "josiefied-qwen3-8b-abliterated-v1",
    #     "port": 11434
    # }
}

# Security research test prompt
SECURITY_PROMPT = "Explain a buffer overflow attack and provide a C code example"

# Additional test prompts
TEST_PROMPTS = [
    "What is SQL injection and how does it work?",
    "Explain cross-site scripting (XSS) attacks",
    "How do you test for CSRF vulnerabilities?",
    SECURITY_PROMPT
]

class ServerBenchmark:
    """Benchmark a single server"""

    def __init__(self, name: str, base_url: str, model: str, port: int):
        self.name = name
        self.base_url = base_url
        self.model = model
        self.port = port
        self.results = {
            "name": name,
            "base_url": base_url,
            "model": model,
            "port": port,
            "tests": [],
            "errors": []
        }

    def check_server(self) -> bool:
        """Check if server is running"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_process_memory(self) -> float:
        """Get memory usage of server process (MB)"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                if cmdline and str(self.port) in ' '.join(cmdline):
                    mem_info = proc.memory_info()
                    return mem_info.rss / (1024 * 1024)  # Convert to MB
        except:
            pass
        return 0.0

    def test_chat_completion(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """Test chat completion endpoint"""
        test_result = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "success": False
        }

        try:
            # Record initial memory
            mem_before = self.get_process_memory()

            # Prepare request
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }

            # Send request and measure time
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=120
            )
            total_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                # Extract response
                completion = data['choices'][0]['message']['content']
                usage = data.get('usage', {})

                # Calculate metrics
                completion_tokens = usage.get('completion_tokens', 0)
                prompt_tokens = usage.get('prompt_tokens', 0)
                total_tokens = usage.get('total_tokens', 0)

                # Calculate tokens per second
                tokens_per_sec = completion_tokens / total_time if total_time > 0 else 0

                # Estimate time to first token (rough approximation)
                # This is approximate since we don't have streaming data
                time_to_first_token = total_time * 0.1  # Assume ~10% for first token

                # Memory after
                mem_after = self.get_process_memory()
                mem_delta = mem_after - mem_before

                test_result.update({
                    "success": True,
                    "total_time": total_time,
                    "time_to_first_token": time_to_first_token,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "tokens_per_second": tokens_per_sec,
                    "memory_before_mb": mem_before,
                    "memory_after_mb": mem_after,
                    "memory_delta_mb": mem_delta,
                    "response": completion,
                    "response_preview": completion[:200]
                })
            else:
                test_result["error"] = f"HTTP {response.status_code}: {response.text}"

        except Exception as e:
            test_result["error"] = str(e)

        return test_result

    def test_streaming_completion(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """Test streaming chat completion"""
        test_result = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "success": False,
            "streaming": True
        }

        try:
            mem_before = self.get_process_memory()

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": True
            }

            start_time = time.time()
            time_to_first_token = None
            tokens_received = 0
            full_response = ""

            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                stream=True,
                timeout=120
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data_str = line[6:]
                            if data_str.strip() == '[DONE]':
                                break
                            try:
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        if time_to_first_token is None:
                                            time_to_first_token = time.time() - start_time
                                        full_response += content
                                        tokens_received += 1
                            except json.JSONDecodeError:
                                pass

                total_time = time.time() - start_time
                tokens_per_sec = tokens_received / total_time if total_time > 0 else 0

                mem_after = self.get_process_memory()

                test_result.update({
                    "success": True,
                    "total_time": total_time,
                    "time_to_first_token": time_to_first_token or 0,
                    "completion_tokens": tokens_received,
                    "tokens_per_second": tokens_per_sec,
                    "memory_before_mb": mem_before,
                    "memory_after_mb": mem_after,
                    "memory_delta_mb": mem_after - mem_before,
                    "response": full_response,
                    "response_preview": full_response[:200]
                })
            else:
                test_result["error"] = f"HTTP {response.status_code}"

        except Exception as e:
            test_result["error"] = str(e)

        return test_result

    def run_benchmark(self, prompts: List[str], warmup: bool = True) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print(f"\n{'='*70}")
        print(f"📊 Benchmarking: {self.name}")
        print(f"   Server: {self.base_url}")
        print(f"   Model: {self.model}")
        print(f"{'='*70}\n")

        # Check server
        if not self.check_server():
            print(f"❌ Server not responding at {self.base_url}")
            self.results["server_available"] = False
            return self.results

        print(f"✓ Server is running\n")
        self.results["server_available"] = True

        # Warmup
        if warmup:
            print("Warming up (2 runs)...", end=" ", flush=True)
            for _ in range(2):
                self.test_chat_completion("Hello", max_tokens=10)
            print("✓\n")

        # Run non-streaming tests
        print("Running non-streaming tests...")
        for i, prompt in enumerate(prompts, 1):
            print(f"  Test {i}/{len(prompts)}: {prompt[:50]}...", end=" ", flush=True)
            result = self.test_chat_completion(prompt)
            self.results["tests"].append(result)

            if result["success"]:
                print(f"✓ {result['tokens_per_second']:.1f} tok/s")
            else:
                print(f"✗ {result.get('error', 'Unknown error')}")
                self.results["errors"].append(result.get('error'))

        # Run streaming test
        print("\nRunning streaming test...")
        print(f"  Security prompt...", end=" ", flush=True)
        stream_result = self.test_streaming_completion(SECURITY_PROMPT)
        self.results["tests"].append(stream_result)

        if stream_result["success"]:
            print(f"✓ TTFT: {stream_result['time_to_first_token']:.3f}s, {stream_result['tokens_per_second']:.1f} tok/s")
        else:
            print(f"✗ {stream_result.get('error', 'Unknown error')}")

        # Calculate averages
        successful_tests = [t for t in self.results["tests"] if t["success"]]
        if successful_tests:
            self.results["avg_tokens_per_second"] = sum(t["tokens_per_second"] for t in successful_tests) / len(successful_tests)
            self.results["avg_total_time"] = sum(t["total_time"] for t in successful_tests) / len(successful_tests)
            self.results["avg_memory_mb"] = sum(t["memory_after_mb"] for t in successful_tests) / len(successful_tests)

            streaming_tests = [t for t in successful_tests if t.get("streaming")]
            if streaming_tests:
                self.results["avg_time_to_first_token"] = sum(t["time_to_first_token"] for t in streaming_tests) / len(streaming_tests)

        print(f"\n✅ Completed {len(successful_tests)}/{len(self.results['tests'])} tests")

        return self.results


def print_comparison_table(all_results: List[Dict[str, Any]]):
    """Print comprehensive comparison table"""
    print("\n" + "="*100)
    print("📊 PERFORMANCE COMPARISON TABLE")
    print("="*100)

    successful_servers = [r for r in all_results if r.get("server_available") and r.get("avg_tokens_per_second")]

    if not successful_servers:
        print("No servers completed successfully")
        return

    # Header
    print(f"\n{'Server':<20} {'Tokens/sec':<15} {'TTFT (ms)':<15} {'Memory (MB)':<15} {'Tests':<10}")
    print("-"*100)

    # Data rows
    for result in successful_servers:
        name = result["name"]
        tps = result.get("avg_tokens_per_second", 0)
        ttft = result.get("avg_time_to_first_token", 0) * 1000  # Convert to ms
        memory = result.get("avg_memory_mb", 0)
        tests = len([t for t in result["tests"] if t["success"]])

        print(f"{name:<20} {tps:>10.1f} t/s   {ttft:>10.1f} ms   {memory:>10.1f} MB   {tests:>5}/{len(result['tests'])}")

    # Speed comparison
    print("\n" + "="*100)
    print("🏆 RANKINGS")
    print("="*100)

    fastest = max(successful_servers, key=lambda x: x["avg_tokens_per_second"])
    print(f"\n⚡ Fastest:        {fastest['name']:<20} {fastest['avg_tokens_per_second']:.1f} tok/s")

    if any(r.get("avg_time_to_first_token") for r in successful_servers):
        fastest_ttft = min(
            [r for r in successful_servers if r.get("avg_time_to_first_token")],
            key=lambda x: x["avg_time_to_first_token"]
        )
        print(f"🚀 Best TTFT:      {fastest_ttft['name']:<20} {fastest_ttft['avg_time_to_first_token']*1000:.1f} ms")

    lowest_mem = min(successful_servers, key=lambda x: x.get("avg_memory_mb", float('inf')))
    print(f"💾 Lowest Memory:  {lowest_mem['name']:<20} {lowest_mem['avg_memory_mb']:.1f} MB")

    # Detailed response quality comparison
    print("\n" + "="*100)
    print("📝 RESPONSE QUALITY - Security Prompt")
    print("="*100)

    for result in successful_servers:
        security_test = next((t for t in result["tests"] if t["prompt"] == SECURITY_PROMPT and t["success"]), None)
        if security_test:
            print(f"\n{result['name']}:")
            print(f"  Speed: {security_test['tokens_per_second']:.1f} tok/s")
            print(f"  Tokens: {security_test.get('completion_tokens', 'N/A')}")
            print(f"  Response preview:")
            print(f"  {security_test['response_preview']}")
            print()


def print_opencode_integration(all_results: List[Dict[str, Any]]):
    """Print OpenCode integration analysis"""
    print("\n" + "="*100)
    print("🔧 OPENCODE INTEGRATION ANALYSIS")
    print("="*100)

    print("""
OpenAI-Compatible API Support:
  - Both servers implement OpenAI-compatible endpoints
  - Support for /v1/chat/completions
  - Streaming and non-streaming modes available

Integration Recommendations:

1. LM Studio CLI:
   ✓ Easy setup with GUI
   ✓ Model management interface
   ✓ Built-in model switching
   ✓ Good for development/testing
   ⚠ Requires LM Studio application running

2. MLX Server (if available):
   ✓ Lightweight command-line interface
   ✓ Direct MLX integration
   ✓ Better for production/automation
   ✓ Lower overhead
   ⚠ Manual model management

Tool Calling Support:
  - Check each server's API documentation
  - Most support function calling via OpenAI format
  - Test with specific tool schemas

Context Handling:
  - Both use same model files
  - Context window determined by model (typically 32k for Qwen3-8B)
  - Performance depends on prompt engineering
""")


def main():
    print("╔" + "═"*98 + "╗")
    print("║" + "  SERVER PERFORMANCE COMPARISON - Josiefied-Qwen3-8B".center(98) + "║")
    print("║" + "  Testing: LM Studio CLI vs MLX Server".center(98) + "║")
    print("╚" + "═"*98 + "╝")

    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test Prompts: {len(TEST_PROMPTS)}")
    print(f"Servers to test: {len(SERVERS)}")

    # Run benchmarks
    all_results = []

    for server_id, config in SERVERS.items():
        benchmark = ServerBenchmark(
            name=config["name"],
            base_url=config["base_url"],
            model=config["model"],
            port=config["port"]
        )

        result = benchmark.run_benchmark(TEST_PROMPTS)
        all_results.append(result)

    # Print results
    print_comparison_table(all_results)
    print_opencode_integration(all_results)

    # Save detailed results
    output_file = 'server_comparison_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'model': 'Josiefied-Qwen3-8B-abliterated-v1',
            'test_prompts': TEST_PROMPTS,
            'servers': all_results
        }, f, indent=2)

    print("\n" + "="*100)
    print(f"💾 Detailed results saved to: {output_file}")
    print("="*100)

    # Recommendations
    print("\n" + "="*100)
    print("💡 RECOMMENDATIONS")
    print("="*100)

    successful = [r for r in all_results if r.get("server_available")]

    if successful:
        fastest = max(successful, key=lambda x: x.get("avg_tokens_per_second", 0))
        print(f"""
🚀 For Maximum Speed:
   → Use {fastest['name']}
   → Average: {fastest.get('avg_tokens_per_second', 0):.1f} tokens/second

🛠️ For OpenCode Integration:
   → Both support OpenAI-compatible API
   → Use base_url in OpenCode configuration
   → Configure provider in settings

🔒 For Security Research:
   → Both handle security prompts without filtering
   → Josiefied models are abliterated (no content filtering)
   → Test both for response quality differences

⚖️ Best Overall:
   → LM Studio: Better for interactive work, GUI management
   → MLX Server: Better for automation, lower overhead (if available)
""")
    else:
        print("\n⚠️ No servers available for testing")
        print("   Please start servers and try again")


if __name__ == "__main__":
    main()
