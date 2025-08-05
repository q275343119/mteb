from mteb import Benchmark
from mteb.leaderboard.rteb.constant import LEADERBOARD_ICON_MAP
from mteb.leaderboard.rteb.data_engine import DataEngine


def get_dynamic_domain_specific_benchmarks():
    """
    Mock function for dynamically loading domain-specific benchmarks.
    This function can be replaced with actual logic to fetch benchmarks
    from database, API, or other sources.

    Returns:
        list: List of Benchmark objects for domain-specific category
    """
    data_engine = DataEngine()

    benchmark_list = [d.get("name").capitalize() for d in data_engine.datasets if d.get("name") != "text"]

    # 创建自定义Benchmark对象
    custom_benchmarks = []
    for benchmark_info in benchmark_list:
        try:

            # 创建Benchmark对象
            custom_benchmark = Benchmark(
                name=benchmark_info,
                display_name=LEADERBOARD_ICON_MAP.get(benchmark_info,"")+benchmark_info,
                tasks=[],
            )
            custom_benchmarks.append(custom_benchmark)
        except Exception as e:
            print(f"Failed to create benchmark {benchmark_info['name']}: {e}")
            continue

    return custom_benchmarks

if __name__ == '__main__':
    get_dynamic_domain_specific_benchmarks()