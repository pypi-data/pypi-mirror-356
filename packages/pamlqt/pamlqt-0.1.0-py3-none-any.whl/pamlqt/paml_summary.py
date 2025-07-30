import re
import os
import pandas as pd
from pathlib import Path

def summarize_paml_results(res_dir: str, out_csv: str) -> None:
    """
    扫描 res_dir 下所有 .txt 文件，提取 kappa 和 omega，
    最后写入 out_csv。
    """
    res_path = Path(res_dir)
    if not res_path.is_dir():
        raise ValueError(f"结果目录不存在: {res_dir}")

    records = []
    for txt in sorted(res_path.glob("*.txt")):
        text = txt.read_text(encoding='utf-8', errors='ignore')
        kapp = re.search(r"kappa.*?=\s*([\d\.]+)", text, re.IGNORECASE)
        omeg = re.search(r"omega.*?=\s*([\d\.]+)", text, re.IGNORECASE)
        records.append({
            "filename": txt.name,
            "kappa":    float(kapp.group(1)) if kapp else None,
            "omega":    float(omeg.group(1)) if omeg else None
        })

    df = pd.DataFrame(records, columns=["filename", "kappa", "omega"])
    df.to_csv(out_csv, index=False)
    print(f"Summary written to {out_csv}")