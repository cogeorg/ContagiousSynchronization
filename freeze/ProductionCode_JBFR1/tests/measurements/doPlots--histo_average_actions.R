args <- commandArgs(trailingOnly = TRUE)
identifier <- gsub(" *$", "", args[1])
variable_parameter <- as.double(args[2])

histo_average_actions = scan(paste(identifier,"-histo-average_actions.dat", sep=''))
res_average_actions = c()
res_average_actions[1] = variable_parameter
res_average_actions[2] = mean(histo_average_actions)
res_average_actions[3] = sd(histo_average_actions)
res_average_actions = matrix(res_average_actions,1,3)
write.table(	res_average_actions, 
				paste(identifier,"-res-average_actions.dat",sep=''), 
				quote=FALSE, sep=" ", 
				row.names = FALSE, col.names = FALSE
			)