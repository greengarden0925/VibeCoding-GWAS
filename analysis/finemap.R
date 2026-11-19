# 用 SuSiE-RSS 對最顯著位點做精細定位（L12）
# 用法：Rscript finemap.R RESULTS_DIR
args <- commandArgs(trailingOnly = TRUE)
fm <- file.path(args[1], "finemap")
library(susieR)
loc <- read.table(file.path(fm, "locus.tsv"), header = TRUE, sep = "\t", check.names = FALSE)
R <- as.matrix(read.table(file.path(fm, "locus.ld"), header = FALSE))
stopifnot(nrow(R) == nrow(loc))
R[is.na(R)] <- 0
n <- median(loc$N, na.rm = TRUE)
keep <- !is.na(loc$Z)
fit <- susie_rss(z = loc$Z[keep], R = R[keep, keep], n = n, L = 10)
pip <- rep(NA_real_, nrow(loc)); pip[keep] <- fit$pip
cs <- rep(NA_integer_, nrow(loc))
idx <- which(keep)
if (!is.null(fit$sets$cs)) {
  for (k in seq_along(fit$sets$cs)) cs[idx[fit$sets$cs[[k]]]] <- k
}
write.table(data.frame(ID = loc$ID, PIP = pip, CS = cs), file.path(fm, "susie_pip.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
sink(file.path(fm, "susie_summary.txt")); print(summary(fit)); print(fit$sets); sink()
cat("susieR version:", as.character(packageVersion("susieR")), "\n",
    file = file.path(args[1], "versions.txt"), append = TRUE)
print(fit$sets)
