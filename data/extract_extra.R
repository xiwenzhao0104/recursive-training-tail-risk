# Usage: Rscript extract_extra.R <evir data dir> <ReIns data dir> <output dir>
# Writes norwegian_fire.csv, soa_medical.csv and sp500_losses.csv.
args <- commandArgs(trailingOnly = TRUE)
e <- new.env()
load(file.path(args[2], "norwegianfire.RData"), envir = e)
write.csv(data.frame(loss = e$norwegianfire$size, year = e$norwegianfire$year),
          file.path(args[3], "norwegian_fire.csv"), row.names = FALSE)
load(file.path(args[2], "soa.RData"), envir = e)
write.csv(data.frame(loss = e$soa$size), file.path(args[3], "soa_medical.csv"), row.names = FALSE)
load(file.path(args[1], "sp.raw.rda"), envir = e)
p <- as.numeric(e$sp.raw)
r <- -100 * diff(log(p))                  # daily loss in percent
d <- as.character(attr(e$sp.raw, "times"))[-1]
keep <- r > 0
write.csv(data.frame(loss = r[keep], date = d[keep]), file.path(args[3], "sp500_losses.csv"),
          row.names = FALSE)
