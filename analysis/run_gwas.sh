#!/usr/bin/env bash
# 依 GWASTutorial 的步驟，從下載資料到 clumping 完整跑一次，所有輸出放 $OUT
set -euo pipefail
WORK=${WORK:-$PWD/work}
OUT=${OUT:-$PWD/results}
TUT=$WORK/GWASTutorial
DATA=$TUT/01_Dataset
mkdir -p "$WORK" "$OUT"/{qc,pca,gwas,clump,logs}
cd "$WORK"
STEP=0
# 執行一個 PLINK 指令，並把該步的 .log 另存成編號檔，方便講義引用
run() { "$@"; STEP=$((STEP+1)); local o="${@: -1}"; cp "$o.log" "$OUT/logs/$(printf %02d $STEP)_$1_$(basename "$o").log"; }

# ---------- 0. 取得教學資料 ----------
[ -d "$TUT" ] || git clone --depth 1 https://github.com/Cloufield/GWASTutorial.git
# repo 內已附 63 MB 的 zip；沒有才照 download_sampledata.sh 從 Dropbox 下載
( cd "$DATA"
  if [ ! -f 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.bed ]; then
    if [ -f 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.zip ]; then
      unzip -o -j 1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing.zip
    else
      bash download_sampledata.sh
    fi
  fi )
G=$DATA/1KG.EAS.auto.snp.norm.nodup.split.rare002.common015.missing
HILD=$TUT/05_PCA/high-ld-hg19.txt
ls -l "$G".bed "$G".bim "$G".fam "$DATA/1kgeas_binary.txt" "$HILD"

{ echo "date: $(date -u)"; plink --version; plink2 --version; } > "$OUT/versions.txt"
echo "raw_samples $(wc -l < "$G".fam)" > "$OUT/counts.txt"
echo "raw_variants $(wc -l < "$G".bim)" >> "$OUT/counts.txt"

# ---------- 1. QC（L07） ----------
Q=$OUT/qc/plink_results
run plink  --bfile "$G" --missing --out "$Q"
run plink2 --bfile "$G" --freq    --out "$Q"
run plink  --bfile "$G" --hardy   --out "$Q"
run plink  --bfile "$G" --maf 0.01 --geno 0.02 --mind 0.02 --hwe 1e-6 \
       --indep-pairwise 50 5 0.2 --out "$Q"
run plink  --bfile "$G" --extract "$Q".prune.in --het --out "$Q"
awk 'NR>1 && ($6>0.1 || $6<-0.1) {print $1,$2}' "$Q".het > "$OUT/qc/high_het.sample"
C=$OUT/qc/sample_data.clean
run plink  --bfile "$G" --maf 0.01 --geno 0.02 --mind 0.02 --hwe 1e-6 \
       --remove "$OUT/qc/high_het.sample" --keep-allele-order --make-bed --out "$C"
echo "high_het_samples $(wc -l < "$OUT/qc/high_het.sample")" >> "$OUT/counts.txt"
echo "prune_in_variants $(wc -l < "$Q".prune.in)" >> "$OUT/counts.txt"
echo "clean_samples $(wc -l < "$C".fam)" >> "$OUT/counts.txt"
echo "clean_variants $(wc -l < "$C".bim)" >> "$OUT/counts.txt"

# ---------- 2. PCA（L08） ----------
P=$OUT/pca/plink_results
run plink  --bfile "$C" --make-set "$HILD" --write-set --out "$OUT/pca/hild"
run plink2 --bfile "$C" --maf 0.01 --exclude "$OUT/pca/hild.set" \
       --indep-pairwise 500 50 0.2 --out "$P"
run plink2 --bfile "$C" --extract "$P".prune.in --king-cutoff 0.0884 --out "$P"
run plink2 --bfile "$C" --keep "$P".king.cutoff.in.id --extract "$P".prune.in \
       --freq counts --pca approx allele-wts 10 --grm-maf 0.01 yes-really --out "$P"
# ↑ 2026 年版的 PLINK 2 在 MAF 低於 0.25/sqrt(樣本數) 時會拒絕算 PCA；
#   GWASTutorial 撰寫時沒有這個檢查。加上 --grm-maf 0.01 yes-really 才能重現原教學的設定。
run plink2 --bfile "$C" --read-freq "$P".acount \
       --score "$P".eigenvec.allele 2 6 header-read no-mean-imputation variance-standardize \
       --score-col-nums 7-16 --out "$OUT/pca/plink_results_projected"
echo "king_kept $(($(wc -l < "$P".king.cutoff.in.id)-1))" >> "$OUT/counts.txt"
echo "king_removed $(($(wc -l < "$P".king.cutoff.out.id)-1))" >> "$OUT/counts.txt"

# ---------- 3. 關聯分析（L09） ----------
run plink2 --bfile "$C" --pheno "$DATA/1kgeas_binary.txt" --pheno-name B1 --maf 0.01 \
       --covar "$OUT/pca/plink_results_projected.sscore" --covar-col-nums 6-10 \
       --glm hide-covar firth firth-residualize single-prec-cc \
       --out "$OUT/gwas/1kgeas"

# ---------- 4. Clumping（L10） ----------
run plink --bfile "$C" --clump-p1 0.0001 --clump-r2 0.1 --clump-kb 250 \
      --clump "$OUT/gwas/1kgeas.B1.glm.firth" --clump-snp-field ID --clump-field P \
      --out "$OUT/clump/1kg_eas"

cp "$DATA/causal.snplist" "$OUT/gwas/"
cp "$DATA/integrated_call_samples_v3.20130502.ALL.panel" "$OUT/pca/"
cat "$OUT/counts.txt"
