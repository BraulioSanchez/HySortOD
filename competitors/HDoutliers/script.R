args<-commandArgs(TRUE)
dName <- args[1]
d <- args[2]
alpha <- as.double(args[3])

my_packages <- c("HDoutliers", "readr", "stringr")
not_installed <- my_packages[!(my_packages %in% installed.packages()[ , "Package"])]
if(length(not_installed)) install.packages(not_installed)

library(HDoutliers)
library(readr)
library(stringr)

# read data
f <- file(dName, open = 'r')
cNames <- readLines(f, 1)
cNames <- unlist(strsplit(cNames, split = ','))
cTypes <- readLines(f, 1)
cTypes <- str_replace_all(cTypes, 'con', 'numeric')
cTypes <- str_replace_all(cTypes, 'cat', 'factor')
cTypes <- unlist(strsplit(cTypes, split = ','))
cTypes[length(cTypes)] = 'NULL'
dataset <- read.csv(dName, skip = 2, header = FALSE, col.names = cNames, colClasses = cTypes)
close.connection(f)

# process data
sink(paste('competitors/HDoutliers/results/', paste(paste('output_', paste(d, sep = ''), sep = ''),'.txt', sep = ''), sep = ''))
cat('pred', '\n')
cat('cat', '\n')
result <- HDoutliers(dataset, alpha = alpha)
for (i in 1:nrow(dataset)) {
  if (is.na(match(i, result)))
    cat(0, '\n')
  else
    cat(1, '\n')
}
sink()