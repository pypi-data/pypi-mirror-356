import os

CTL_TEMPLATE = """seqfile = {seqfile}
treefile = {treefile}
outfile = {outfile}

noisy = 9
verbose = 1
runmode = 0

seqtype = 1
CodonFreq = 2
ndata = 1
clock = 0
aaDist = 0
aaRatefile = ../dat/jones.dat

model = 0
NSsites = 0

icode = 0
Mgene = 0

fix_kappa = 0
kappa = 2
fix_omega = 0
omega = 1

fix_alpha = 1
alpha = 0.
Malpha = 0
ncatG = 8

getSE = 0
RateAncestor = 1

Small_Diff = .5e-6
cleandata = 0
"""

def generate_ctl_files(phy_dir, tre_dir, res_dir, ctl_dir):
    os.makedirs(res_dir, exist_ok=True)
    os.makedirs(ctl_dir, exist_ok=True)
    for fn in os.listdir(phy_dir):
        if not fn.endswith(".phy"): continue
        base = os.path.splitext(fn)[0]
        seqf = os.path.join(phy_dir, fn)
        treef= os.path.join(tre_dir, f"{base}.tre")
        outf = os.path.join(res_dir, f"{base}.txt")
        ctlf = os.path.join(ctl_dir, f"{base}.ctl")
        content = CTL_TEMPLATE.format(seqfile=seqf, treefile=treef, outfile=outf)
        with open(ctlf, "w") as w:
            w.write(content)
        print(f"Created {ctlf}")