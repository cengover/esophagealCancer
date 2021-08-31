setwd("~/Documents/cisnet/esophageal-cancer-abm/")
# Read datasets
biopsy40 = read.table("tumor.csv.0",sep=",",header = TRUE)
biopsy50 = read.table("tumor.csv.1",sep=",",header = TRUE)
biopsy60 = read.table("tumor.csv.2",sep=",",header = TRUE)
biopsy40$type[biopsy40$type == 2] <- "Dysplasia"
biopsy40$type[biopsy40$type == 3] <- "Cancer"
biopsy40$type[biopsy40$type == 1] <- "BE"
biopsy50$type[biopsy50$type == 2] <- "Dysplasia"
biopsy50$type[biopsy50$type == 3] <- "Cancer"
biopsy50$type[biopsy50$type == 1] <- "BE"
biopsy60$type[biopsy60$type == 2] <- "Dysplasia"
biopsy60$type[biopsy60$type == 3] <- "Cancer"
biopsy60$type[biopsy60$type == 1] <- "BE"

#install.packages("plotly")
library(plotly)
#packageVersion('plotly')
toplot = subset(biopsy50,type=="Dysplasia"|type=="Cancer")
plot_ly(data = toplot,x=~xcoord,y=~ycoord,z=~zcoord,type="scatter3d",color=~type,
        colors=c("Black","Pink"),marker = list(size = 5),mode="markers",symbol = ~type,symbols=c(1)) 


