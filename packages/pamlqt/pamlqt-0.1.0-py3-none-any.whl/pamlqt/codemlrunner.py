import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def run_single_ctl(ctl_path: Path) -> None:
    """
    对单个 .ctl 文件执行 codeml，并把 stdout/stderr 写到同名 .log 文件里，
    并在启动时自动发送一个回车确认。
    """
    log_path = ctl_path.with_suffix(ctl_path.suffix + ".log")
    with log_path.open("w") as logf:
        proc = subprocess.run(
            ["codeml", str(ctl_path)],
            stdout=logf,
            stderr=subprocess.STDOUT,
            input="\n",    # 把回车发送给 codeml
            text=True      # 使用文本模式
        )
        if proc.returncode != 0:
            raise RuntimeError(f"codeml 返回非零退出码: {proc.returncode}")

def run_parallel_codlem(ctl_dir: str, max_jobs: int):
    """
    在 ctl_dir 里找到所有 .ctl 文件，用线程池并行执行 codeml，
    同时打印进度条。
    """
    ctl_dir = Path(ctl_dir)
    if not ctl_dir.is_dir():
        raise ValueError(f"输入目录不存在: {ctl_dir}")
    ctl_files = sorted(ctl_dir.glob("*.ctl"))
    if not ctl_files:
        raise ValueError(f"目录里没有找到 .ctl 文件: {ctl_dir}")

    total = len(ctl_files)
    print(f"Found {total} .ctl files, running up to {max_jobs} in parallel.")

    errors = []
    # 用 ThreadPoolExecutor，因为调用外部命令 I/O 密集
    with ThreadPoolExecutor(max_workers=max_jobs) as pool:
        futures = {pool.submit(run_single_ctl, ctl): ctl for ctl in ctl_files}
        for future in tqdm(as_completed(futures), total=total, desc="codeml"):
            ctl = futures[future]
            try:
                future.result()
            except Exception as e:
                errors.append((ctl.name, str(e)))

    print("\nAll jobs done.")
    if errors:
        print(f"\n{len(errors)} 个任务失败：")
        for name, msg in errors:
            print(f" - {name}: {msg}")
        sys.exit(1)