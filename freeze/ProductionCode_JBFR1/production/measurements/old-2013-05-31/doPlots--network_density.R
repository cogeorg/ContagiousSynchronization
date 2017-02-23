args <- commandArgs(trailingOnly = TRUE)
identifier <- gsub(" *$", "", args[1])
variable_parameter <- as.double(args[2])

histo_network_density = scan(paste(identifier,"-histo-network_density.dat", sep=''))
res_average_density = c()
res_average_density[1] = variable_parameter
res_average_density[2] = mean(histo_network_density)
res_average_density[3] = sd(histo_network_density)
res_average_density = matrix(res_average_density,1,3)
write.table(	res_average_density, 
				paste(identifier,"-res-average_density.dat",sep=''), 
				quote=FALSE, sep=" ", 
				row.names = FALSE, col.names = FALSE
			)