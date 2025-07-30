


library(cidr)

args <- commandArgs(trailingOnly=TRUE)

data_type <- args[1]
n_cluster <- args[2]
pc <- args[3]
dropout <- args[4]
dissim <- args[5]
large_data <- args[6]
data_path <- gsub("\\\\", "/", args[7])
pc_path <- gsub("\\\\", "/", args[8])
var_path <- gsub("\\\\", "/", args[9])
eigen_path <- gsub("\\\\", "/", args[10])
dropout_path <- gsub("\\\\", "/", args[11])
dissim_path <- sub("\\\\", "/", args[12])

if (large_data == "False") {
  csv_data <- read.csv("stdin")
} else {
  csv_data <- read.csv(data_path)
}

data_object <- as.matrix(csv_data)

if (data_type == "cpm"){
  cidr_obj <- scDataConstructor(t(data_object), tagType = data_type)
} else {
  cidr_obj <- scDataConstructor(t(data_object))
}

cat("Object created (1/8)\n", file = stderr())

cidr_obj <- determineDropoutCandidates(cidr_obj)
cat("Determined dropout candidates (2/8)\n", file = stderr())
if (dropout == 'True') {
  if (large_data == 'True') {
    write.csv(cidr_obj@dropoutCandidates, dropout_path)
  } else {
    write.csv(cidr_obj@dropoutCandidates, stdout())
    cat("---END OF DROPOUT CANDIDATES---\n")
  }
}

cidr_obj <- wThreshold(cidr_obj)
cat("Determined threshold (3/8)\n", file = stderr())


cidr_obj <- scDissim(cidr_obj)
cat("Created dissimilarity matrix (4/8)\n", file = stderr())
if (dissim == 'True') {
  if (large_data == 'True') {
    write.csv(cidr_obj@dissim, dissim_path)
  } else {
    write.csv(cidr_obj@dissim, stdout())
    cat("---END OF DISSIMILARITY---\n")
  }
}

pdf("cidr_plots.pdf")

cidr_obj <- scPCA(cidr_obj)
cat("Finished principal component analysis (5/8)\n", file = stderr())
if (pc == 'True') {
  if (large_data == 'True') {
    write.csv(cidr_obj@PC, pc_path)
    write.csv(cidr_obj@variation, var_path)
    write.csv(cidr_obj@eigenvalues, eigen_path)
  } else {
    write.csv(cidr_obj@PC, stdout())
    cat("---END OF PC---\n")
    write.csv(cidr_obj@variation, stdout())
    cat("---END OF VARIATION---\n")
    write.csv(cidr_obj@eigenvalues, stdout())
  }
}

cidr_obj <- nPC(cidr_obj)

cat("Determined number of principal components (6/8)\n", file = stderr())

if (n_cluster != 'None') {
  #if there is an argument for the amount of clusters passed
  cidr_obj <- scCluster(cidr_obj, nCluster = as.integer(n_cluster))
} else {
  nCluster(cidr_obj)
  cidr_obj <- scCluster(cidr_obj)
}

cat("Finished clustering (7/8)\n", file = stderr())

plot(cidr_obj@PC[, c(1, 2)],
  col = cidr_obj@clusters,
  pch = cidr_obj@clusters,
  main = "CIDR Clustering",
  xlab = "PC1", ylab = "PC2"
)

cat("Plot done (8/8)\n", file = stderr())