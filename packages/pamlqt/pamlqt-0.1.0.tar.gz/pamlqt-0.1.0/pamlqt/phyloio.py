from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from ete3 import Tree
import os

def clean_and_convert_to_phy(input_fasta, output_phy):
    cleaned = []
    for rec in SeqIO.parse(input_fasta, "fasta"):
        seq = str(rec.seq).replace("N", "-")
        if set(seq) != {"-"}:
            cleaned.append(SeqRecord(Seq(seq), id=rec.id, description=""))
    if not cleaned:
        raise ValueError(f"No valid sequences in {input_fasta}")
    lengths = {len(r.seq) for r in cleaned}
    if len(lengths) != 1:
        raise ValueError(f"Inconsistent seq lengths: {lengths}")
    n_taxa = len(cleaned)
    L = lengths.pop()
    with open(output_phy, "w") as f:
        f.write(f"{n_taxa} {L}\n")
        for r in cleaned:
            name = r.id[:50].ljust(30)
            f.write(f"{name}{str(r.seq)}\n")
    return [r.id for r in cleaned]

def process_tree(input_tree, output_tree, species_list):
    tree = Tree(input_tree, format=1)
    tree.prune(species_list)
    leaves = set(tree.get_leaf_names())
    wanted = set(species_list)
    if leaves != wanted:
        raise ValueError(f"Tree/PHY mismatch: in tree only {leaves-wanted}, in phy only {wanted-leaves}")
    with open(output_tree, "w") as f:
        f.write(f"{len(species_list)} 1\n")
        f.write(tree.write(format=1))

def process_folder(raw_dir, phy_dir, tree_file, nh_dir):
    os.makedirs(phy_dir, exist_ok=True)
    os.makedirs(nh_dir, exist_ok=True)
    failures = []
    for fn in os.listdir(raw_dir):
        if not fn.lower().endswith((".fa", ".fasta")): continue
        base = os.path.splitext(fn)[0]
        fasta = os.path.join(raw_dir, fn)
        phy   = os.path.join(phy_dir, f"{base}.phy")
        nh    = os.path.join(nh_dir, f"{base}.tre")
        try:
            spp = clean_and_convert_to_phy(fasta, phy)
            process_tree(tree_file, nh, spp)
            print(f"[OK] {base}")
        except Exception as e:
            failures.append((fn, str(e)))
    if failures:
        for fn, err in failures:
            print(f"[ERR] {fn}: {err}")