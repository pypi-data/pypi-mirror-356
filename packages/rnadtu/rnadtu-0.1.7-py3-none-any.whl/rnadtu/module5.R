library(cidr)
library(qs)
library(arrow)

args <- commandArgs(trailingOnly=TRUE)

func_name <- args[1]
obj_name <- args[2]
layer_name <- args[3]

file_name <- paste0(obj_name, "_", layer_name, ".qs")

export_cidr <- function(sData, slots) {
    for (slot_name in slots) {
        slot_value <- slot(sData, slot_name)

    if (is.matrix(slot_value)){
        df <- as.data.frame(slot_value)
        write_parquet(df, paste0(slot_name, ".parquet"))
    } else if (is.vector(slot_value)) {
        df <- data.frame(value = slot_value)
        write_parquet(df, paste0(slot_name, ".parquet"))
    } else {
        message(paste("Skipping parameter", slot_name, "-not suitable for parquet format"))
    }
    }
}

if (func_name == "scDataConstructor") {
    data_type <- ifelse(length(args) > 4, args[4], "raw")
    csv_data <- read.csv("stdin")
    data_object <- as.matrix(csv_data)
    cidr_obj <- scDataConstructor(t(data_object), tagType = data_type)

} else {
    cidr_obj <- qread(file_name)

    named_args <- list()
    if (length(args) > 3) {
        for (arg in args[4: length(args)]) {
            split <- strsplit(arg, "=")[[1]]
            key <- sub("^--", "", split[1])
            val <- split[2]
            if (!is.na(as.numeric(val))) {
                val <- as.numeric(val)
            } else if (val %in% c("TRUE", "FALSE")) {
                val <- as.logical(val)
            }
            named_args[[key]] <- val
        }
    }

    if (func_name == "determineDropoutCandidates") {
        cidr_obj <- determineDropoutCandidates(cidr_obj)
        export_cidr(cidr_obj, c("dThreshold", "dropoutCandidates"))

    } else if (func_name == "wThreshold") {
        cidr_obj <- wThreshold(cidr_obj)
        export_cidr(cidr_obj, c("wThreshold", "pDropoutCoefA", "pDropoutCoefB"))

    } else if (func_name == "scDissim") {
        cidr_obj <- scDissim(cidr_obj)
        export_cidr(cidr_obj, c("dissim", "correction"))

    } else if (func_name == "scPCA") {
        pdf("cidr_variation_plot.pdf")
        cidr_obj <- scPCA(cidr_obj)
        dev.off()
        export_cidr(cidr_obj, c("PC", "variation", "eigenvalues"))

    } else if (func_name == "nPC") {
        cidr_obj <- nPC(cidr_obj)
        export_cidr(cidr_obj, c("nPC"))

    } else if (func_name == "nCluster") {
        pdf("cidr_number_of_clusters_plot.pdf")
        nCluster(cidr_obj)
        dev.off()
        export_cidr(cidr_obj, c("nPC"))

    } else if (func_name == "scCluster") {
        pdf("cidr_cluster_plot.pdf")
        cidr_obj <- scCluster(cidr_obj)

        plot(cidr_obj@PC[, c(1, 2)],
        col = cidr_obj@clusters,
        pch = cidr_obj@clusters,
        main = "CIDR Clustering",
        xlab = "PC1", ylab = "PC2")
        dev.off()

        export_cidr(cidr_obj, c("nCluster", "clusters", "nPC", "cMethod"))

    } else {
        stop(paste("Unknown function: ", func_name))
    }
}

qsave(cidr_obj, file = file_name)
