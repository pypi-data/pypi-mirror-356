import argparse
from pamlqt.phyloio import process_folder
from pamlqt.ctlgen import generate_ctl_files
from pamlqt.codemlrunner import run_parallel_codlem
from pamlqt.paml_summary import summarize_paml_results

def main():
    parser = argparse.ArgumentParser(
        description="pamlqt → .phy/.tre + codeml ctl generator & runner"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 子命令：prepare
    p_prep = sub.add_parser("prepare", help="生成 .phy/.tre 及 codeml 控制文件")
    p_prep.add_argument("raw_dir", help="输入 raw FASTA 文件夹")
    p_prep.add_argument("tree", help="Newick 树文件")
    p_prep.add_argument(
        "-w", "--workdir", default=".", help="工作目录，默认当前"
    )

    # 子命令：run-codeml
    p_run = sub.add_parser("run-codeml", help="并行执行 codeml .ctl 文件")
    p_run.add_argument("ctl_dir", help="存放 .ctl 文件的文件夹")
    p_run.add_argument(
        "max_jobs", type=int, help="最大并行任务数 (正整数)"
    )
    # 子命令：summarize
    p_sum = sub.add_parser("summarize", help="整合 codeml 结果，输出 CSV")
    p_sum.add_argument("res_dir", help="codeml 输出的 res 目录 (txt 文件所在)")
    p_sum.add_argument(
        "-o", "--out", default="summary.csv",
        help="输出 CSV 文件路径，默认 summary.csv"
    )

    args = parser.parse_args()

    if args.cmd == "prepare":
        phy_dir = f"{args.workdir}/fasta"
        nh_dir  = f"{args.workdir}/nh"
        res_dir = f"{args.workdir}/res"
        ctl_dir = f"{args.workdir}/codeml"
        process_folder(args.raw_dir, phy_dir, args.tree, nh_dir)
        generate_ctl_files(phy_dir, nh_dir, res_dir, ctl_dir)

    elif args.cmd == "run-codeml":
        run_parallel_codlem(args.ctl_dir, args.max_jobs)
    elif args.cmd == "summarize":
        summarize_paml_results(args.res_dir, args.out)

if __name__ == "__main__":
    main()