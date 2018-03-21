## Read in the data
data <- read.csv(file="trials.csv", header=TRUE, sep=',')

sizegrep <- c("tiny", "small", "medium", "large", "huge", "colossal")

for (set in c("Floyd-Warshall", "Johnson-FibonacciHeap", "Johnson-Min-Heap")) {
    algodata = data[data$ALGO == set,]
    for (variety in c("sparse", "dense")) {
        varietydata = algodata[grep(variety, algodata$FILE),]
        times <- c()
        for (size in sizegrep){
            times <- c(times,varietydata[grep(size, varietydata$FILE), 3])
        }
        pdf(paste(set, variety, ".pdf", sep=""))
        barplot(times, names.arg=sizegrep, ylab="Time (seconds)", log="y")
        dev.off()
    }
}

