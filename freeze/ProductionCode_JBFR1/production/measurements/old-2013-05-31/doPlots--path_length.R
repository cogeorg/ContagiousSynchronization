args <- commandArgs(trailingOnly = TRUE)
identifier <- gsub(" *$", "", args[1])
minor_identifier <- gsub("*$","",args[2])
variable_parameter <- as.double(args[3])

histo = scan(paste(identifier, "-histo-", minor_identifier, ".dat", sep=''))
res = c()
res[1] = variable_parameter
res[2] = mean(histo)
res[3] = sd(histo)
res = matrix(res,1,3)
write.table(	res, 
				paste(identifier,"-res-", minor_identifier, ".dat", sep=''), 
				quote=FALSE, sep=" ", 
				row.names = FALSE, col.names = FALSE
			)