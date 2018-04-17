## Read in the data
data <- read.csv(file="runs.csv", header=TRUE, sep=',')
library("calibrate")

for (set in c("BruteForce", "BranchAndBound", "DynamicProgramming", "MSTApproximation")) {
    algodata = data[data$ALGO == set,]
    pdf(paste(set, ".pdf", sep=""))
    plot(algodata$N, algodata$TIME, ylab="Time (seconds)", xlab="Number of Nodes", xlim=c(2,11), log="y")
    textxy(algodata$N, algodata$TIME, algodata$TIME)
    dev.off()
}
