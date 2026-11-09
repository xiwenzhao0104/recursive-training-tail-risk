# Usage: Rscript extract_danish.R danish.rda danish.csv
args <- commandArgs(trailingOnly = TRUE)
e <- new.env()
load(args[1], envir = e)
x <- get("danish", envir = e)
write.csv(data.frame(loss = as.numeric(x), date = as.character(attr(x, "times"))),
          args[2], row.names = FALSE)
