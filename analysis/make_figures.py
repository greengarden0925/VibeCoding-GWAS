"""把 run_gwas.sh 的輸出整理成講義用的圖與表。

用法：
    python make_figures.py RESULTS_DIR main      # QC、PCA、GWAS、clumping 的圖表，並準備精細定位輸入
    python make_figures.py RESULTS_DIR finemap   # 讀 SuSiE 結果，畫精細定位圖
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

R = Path(sys.argv[1])
MODE = sys.argv[2] if len(sys.argv) > 2 else "main"
FIG = R / "figures"
TAB = R / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

PALETTE = ["#0f766e", "#7c3aed", "#ea580c", "#2563eb", "#db2777", "#65a30d"]
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "font.size": 10,
})


def ws(path):
    return pd.read_csv(path, sep=r"\s+")


def md_table(df, path, floatfmt="{:.4g}"):
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        cells = []
        for v in row:
            if isinstance(v, float):
                cells.append(floatfmt.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    Path(path).write_text("\n".join(lines) + "\n")


def load_glm():
    g = pd.read_csv(R / "gwas/1kgeas.B1.glm.firth", sep="\t")
    g = g.rename(columns={"#CHROM": "CHROM"})
    return g


summary = json.loads((R / "summary.json").read_text()) if (R / "summary.json").exists() else {}


def main():
    counts = dict(l.split() for l in (R / "counts.txt").read_text().splitlines() if l.strip())
    summary["counts"] = counts

    # ---------- QC ----------
    imiss = ws(R / "qc/plink_results.imiss")
    lmiss = ws(R / "qc/plink_results.lmiss")
    het = ws(R / "qc/plink_results.het")
    afreq = pd.read_csv(R / "qc/plink_results.afreq", sep="\t")
    hwe = ws(R / "qc/plink_results.hwe")

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    ax[0].hist(imiss["F_MISS"], bins=40, color=PALETTE[0])
    ax[0].axvline(0.02, color="#dc2626", ls="--", lw=1.2, label="--mind 0.02")
    ax[0].set(title="Sample missingness (.imiss)", xlabel="F_MISS", ylabel="Number of samples")
    ax[0].legend(frameon=False)
    ax[1].hist(lmiss["F_MISS"], bins=60, color=PALETTE[1])
    ax[1].axvline(0.02, color="#dc2626", ls="--", lw=1.2, label="--geno 0.02")
    ax[1].set(title="Variant missingness (.lmiss)", xlabel="F_MISS", ylabel="Number of variants", yscale="log")
    ax[1].legend(frameon=False)
    fig.savefig(FIG / "qc_missingness.png")
    plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    maf = afreq["ALT_FREQS"].clip(upper=1)
    maf = np.minimum(maf, 1 - maf)
    ax[0].hist(maf, bins=50, color=PALETTE[2])
    ax[0].axvline(0.01, color="#dc2626", ls="--", lw=1.2, label="--maf 0.01")
    ax[0].set(title="Minor allele frequency (.afreq)", xlabel="MAF", ylabel="Number of variants")
    ax[0].legend(frameon=False)
    ax[1].hist(het["F"], bins=40, color=PALETTE[3])
    for x in (-0.1, 0.1):
        ax[1].axvline(x, color="#dc2626", ls="--", lw=1.2)
    ax[1].set(title="Inbreeding coefficient F (.het)", xlabel="F", ylabel="Number of samples")
    fig.savefig(FIG / "qc_maf_het.png")
    plt.close(fig)

    qc = pd.DataFrame([
        ["原始資料", counts["raw_samples"], counts["raw_variants"]],
        ["F 絕對值 > 0.1 的樣本（移除）", counts["high_het_samples"], "—"],
        ["LD 修剪後保留的 SNP（供 het／PCA 用）", "—", counts["prune_in_variants"]],
        ["QC 後（sample_data.clean）", counts["clean_samples"], counts["clean_variants"]],
    ], columns=["步驟", "樣本數", "變異數"])
    md_table(qc, TAB / "qc_summary.md")
    summary["qc"] = {
        "imiss_max": float(imiss["F_MISS"].max()),
        "n_samples_mind_fail": int((imiss["F_MISS"] > 0.02).sum()),
        "n_variants_geno_fail": int((lmiss["F_MISS"] > 0.02).sum()),
        "n_variants_maf_lt_001": int((maf < 0.01).sum()),
        "n_variants_hwe_lt_1e6": int((hwe["P"] < 1e-6).sum()),
        "het_F_min": float(het["F"].min()), "het_F_max": float(het["F"].max()),
    }

    # ---------- PCA ----------
    sc = pd.read_csv(R / "pca/plink_results_projected.sscore", sep="\t")
    sc = sc.rename(columns={"#FID": "FID", "#IID": "IID"})
    panel = pd.read_csv(R / "pca/integrated_call_samples_v3.20130502.ALL.panel", sep="\t")
    sc = sc.merge(panel[["sample", "pop", "super_pop"]], left_on="IID", right_on="sample", how="left")
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
    pops = sorted(sc["pop"].dropna().unique())
    for i, p in enumerate(pops):
        d = sc[sc["pop"] == p]
        ax[0].scatter(d["PC1_AVG"], d["PC2_AVG"], s=12, alpha=0.8, color=PALETTE[i % len(PALETTE)], label=f"{p} (n={len(d)})")
        ax[1].scatter(d["PC1_AVG"], d["PC3_AVG"], s=12, alpha=0.8, color=PALETTE[i % len(PALETTE)])
    ax[0].set(title="PC1 vs PC2", xlabel="PC1", ylabel="PC2")
    ax[1].set(title="PC1 vs PC3", xlabel="PC1", ylabel="PC3")
    ax[0].legend(frameon=False, fontsize=8, markerscale=1.5)
    fig.savefig(FIG / "pca.png")
    plt.close(fig)
    ev = pd.read_csv(R / "pca/plink_results.eigenval", header=None)[0]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range(1, len(ev) + 1), ev, marker="o", color=PALETTE[0])
    ax.set(title="Scree plot (.eigenval)", xlabel="PC", ylabel="Eigenvalue", xticks=range(1, len(ev) + 1))
    fig.savefig(FIG / "pca_scree.png")
    plt.close(fig)
    summary["pca"] = {"pop_counts": sc["pop"].value_counts().to_dict(), "eigenval": ev.round(3).tolist()}

    # ---------- GWAS ----------
    g = load_glm()
    summary["gwas"] = {"n_rows": int(len(g)), "errcode_counts": g["ERRCODE"].value_counts().to_dict()}
    ok = g[(g["ERRCODE"] == ".") & g["P"].notna()].copy()
    ok = ok[ok["P"] > 0]
    ok["CHROM"] = ok["CHROM"].astype(int)
    ok = ok.sort_values(["CHROM", "POS"])
    chisq = stats.chi2.isf(ok["P"], 1)
    lam = float(np.median(chisq) / stats.chi2.ppf(0.5, 1))
    summary["gwas"].update({"n_tested": int(len(ok)), "lambda_gc": round(lam, 4),
                            "n_gws": int((ok["P"] < 5e-8).sum())})

    # Manhattan
    ok["logp"] = -np.log10(ok["P"])
    offs, ticks, x = {}, [], np.zeros(len(ok))
    start = 0
    for c in range(1, 23):
        m = ok["CHROM"] == c
        if not m.any():
            continue
        pos = ok.loc[m, "POS"]
        x[m.values] = pos - pos.min() + start
        ticks.append((start + (pos.max() - pos.min()) / 2, c))
        start += pos.max() - pos.min() + 2e7
    ok["x"] = x
    fig, ax = plt.subplots(figsize=(11, 4))
    colors = np.where(ok["CHROM"] % 2 == 0, "#94a3b8", PALETTE[0])
    ax.scatter(ok["x"], ok["logp"], s=3, c=colors, linewidths=0, rasterized=True)
    ax.axhline(-np.log10(5e-8), color="#dc2626", ls="--", lw=1)
    causal = [l.split()[0] for l in (R / "gwas/causal.snplist").read_text().splitlines() if l.strip()]
    cz = ok[ok["ID"].isin(causal)]
    ax.scatter(cz["x"], cz["logp"], s=40, facecolors="none", edgecolors=PALETTE[2], linewidths=1.5, label="Simulated causal SNP")
    ax.set_xticks([t[0] for t in ticks], [str(t[1]) for t in ticks], fontsize=8)
    ax.set(xlabel="Chromosome", ylabel="-log10(P)", title=f"Manhattan plot (n tested = {len(ok):,}; red line P = 5e-8)")
    ax.legend(frameon=False, loc="upper right")
    fig.savefig(FIG / "manhattan.png")
    plt.close(fig)

    # QQ
    n = len(ok)
    exp = -np.log10((np.arange(1, n + 1) - 0.5) / n)
    obs = np.sort(ok["logp"].values)[::-1]
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.scatter(exp, obs, s=4, color=PALETTE[1], rasterized=True)
    mx = max(exp.max(), 1)
    ax.plot([0, mx], [0, mx], color="#dc2626", lw=1)
    ax.set(xlabel="Expected -log10(P)", ylabel="Observed -log10(P)", title=f"QQ plot (lambda GC = {lam:.3f})")
    fig.savefig(FIG / "qq.png")
    plt.close(fig)

    top = ok.nsmallest(10, "P")[["CHROM", "POS", "ID", "REF", "ALT", "A1", "A1_FREQ", "OR", "LOG(OR)_SE", "P"]]
    md_table(top, TAB / "top10.md")
    cz_all = g[g["ID"].isin(causal)][["CHROM", "POS", "ID", "A1", "A1_FREQ", "OR", "P", "ERRCODE"]].rename(columns={"CHROM": "CHR"})
    md_table(cz_all, TAB / "causal_lookup.md")

    # ---------- Clumping ----------
    cl = ws(R / "clump/1kg_eas.clumped")
    summary["clump"] = {"n_clumps": int(len(cl)), "n_gws_clumps": int((cl["P"] < 5e-8).sum())}
    md_table(cl[cl["P"] < 5e-8][["CHR", "SNP", "BP", "P", "TOTAL"]], TAB / "clumps_gws.md")

    # ---------- 精細定位輸入 ----------
    lead = cl.sort_values("P").iloc[0]
    chrom, bp = int(lead["CHR"]), int(lead["BP"])
    loc = ok[(ok["CHROM"] == chrom) & (ok["POS"].between(bp - 500_000, bp + 500_000))].copy()
    bim = pd.read_csv(R / "qc/sample_data.clean.bim", sep="\t", header=None,
                      names=["CHR", "ID", "CM", "BP", "B1", "B2"])
    bim = bim[bim["ID"].isin(loc["ID"])].reset_index(drop=True)
    loc = bim[["ID", "B1"]].merge(loc, on="ID", how="left")
    beta = np.log(loc["OR"])
    sign = np.where(loc["A1"] == loc["B1"], 1, -1)
    loc["Z"] = sign * beta / loc["LOG(OR)_SE"]
    loc["N"] = loc["OBS_CT"]
    fm = R / "finemap"
    fm.mkdir(exist_ok=True)
    loc[["ID", "CHROM", "POS", "B1", "A1", "OR", "LOG(OR)_SE", "Z", "P", "N"]].to_csv(fm / "locus.tsv", sep="\t", index=False)
    loc["ID"].to_csv(fm / "locus.snplist", index=False, header=False)
    summary["finemap"] = {"lead": lead["SNP"], "chrom": chrom, "bp": bp, "n_snps": int(len(loc))}
    (R / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


def finemap():
    fm = R / "finemap"
    loc = pd.read_csv(fm / "locus.tsv", sep="\t")
    pip = pd.read_csv(fm / "susie_pip.tsv", sep="\t")
    loc = loc.merge(pip, on="ID")
    ld = np.loadtxt(fm / "locus.ld")
    lead_id = summary["finemap"]["lead"]
    li = loc.index[loc["ID"] == lead_id][0]
    loc["r2"] = ld[li, :] ** 2
    fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    pos = loc["POS"] / 1e6
    sca = ax[0].scatter(pos, -np.log10(loc["P"]), c=loc["r2"], cmap="viridis", s=14, vmin=0, vmax=1)
    ax[0].scatter(pos[li], -np.log10(loc["P"][li]), marker="D", s=50, color=PALETTE[2], label=f"lead {lead_id}")
    ax[0].set(ylabel="-log10(P)", title=f"Regional association, chr{summary['finemap']['chrom']}")
    ax[0].legend(frameon=False)
    fig.colorbar(sca, ax=ax[0], label="r² with lead")
    cs = loc["CS"].fillna(0).astype(int)
    ax[1].scatter(pos[cs == 0], loc["PIP"][cs == 0], s=12, color="#94a3b8")
    for k in sorted(set(cs) - {0}):
        m = cs == k
        ax[1].scatter(pos[m], loc["PIP"][m], s=30, color=PALETTE[k % len(PALETTE)], label=f"95% credible set L{k}")
    ax[1].set(ylabel="PIP", xlabel="Position (Mb, hg19)", title="SuSiE posterior inclusion probability")
    ax[1].legend(frameon=False)
    fig.savefig(FIG / "finemap.png")
    plt.close(fig)
    cst = loc[cs > 0].sort_values(["CS", "PIP"], ascending=[True, False])[["CS", "ID", "POS", "P", "PIP", "r2"]]
    md_table(cst, TAB / "credible_sets.md")
    causal = [l.split()[0] for l in (R / "gwas/causal.snplist").read_text().splitlines() if l.strip()]
    summary["finemap"].update({
        "n_cs": int(len(set(cs) - {0})),
        "cs_sizes": cs[cs > 0].value_counts().sort_index().to_dict(),
        "causal_in_locus": [c for c in causal if c in set(loc["ID"])],
        "causal_pip": {c: float(loc.loc[loc["ID"] == c, "PIP"].iloc[0]) for c in causal if c in set(loc["ID"])},
        "top_pip": loc.nlargest(3, "PIP")[["ID", "PIP"]].to_dict("records"),
    })
    (R / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    print(json.dumps(summary["finemap"], indent=2, ensure_ascii=False, default=str))


main() if MODE == "main" else finemap()
