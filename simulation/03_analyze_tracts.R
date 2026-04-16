# Manon Le Goff - Novembre 2024
# Script to create summary statistic

rm(list=ls())
library(ggplot2)
library(tidyr)
library(dplyr)
library(metap)

setwd("/Volumes/MANON/Data_cione/simulation/pipeline")

analyze_tracts <- function(simu_dir) {
  
  # Function to extract tracts carrying the mutation
  tracts_pop <- function(at_data) {
    tracts <- data.frame(sample_id = character(),
                         left = numeric(),
                         right = numeric(),
                         population = character(),
                         stringsAsFactors = FALSE)
    at_data$sample_id <- as.character(at_data$sample)
    samples <- unique(at_data$sample_id)
    
    for (s in samples) {
      sample_data <- at_data %>% filter(sample_id == s)
      sample_data_sorted <- sample_data[order(sample_data$left), ]
      sample_data_filtered <- sample_data_sorted[c(TRUE, diff(sample_data_sorted$population) != 0), ]
      sample_data_filtered$right <- c(sample_data_filtered$left[-1], 7499939)
      
      tracts <- rbind(
        tracts,
        sample_data_filtered[, c("sample_id", "left", "right", "population")]
      )
    }
    
    return(tracts)
  }
  
  # Tract lengths
  calculate_lengths <- function(data) {
    results <- list()
    samples <- unique(data$sample_id)
    
    for (s in samples) {
      tracts_sample <- subset(data, sample_id == s)
      lengths_1 <- numeric()
      
      for (i in 1:nrow(tracts_sample)) {
        # all tracts
        # if (tracts_sample$population[i] == 1) {
        #   tract_length <- tracts_sample$right[i] - tracts_sample$left[i]
        
        # only tracts carrying the mutation
        if (tracts_sample$population[i] == 1 &&
            tracts_sample$left[i] < 3749970 &&
            tracts_sample$right[i] > 3749970) {
          
          tract_length <- tracts_sample$right[i] - tracts_sample$left[i]
          
          lengths_1 <- c(lengths_1, tract_length)
        }
      }
      
      if (length(lengths_1) > 0) {
        results[[as.character(s)]] <- lengths_1
      }
    }
    
    result_table <- data.frame(
      sample_id = rep(names(results), times = lengths(results)),
      length = as.numeric(unlist(results, use.names = FALSE)),
      row.names = NULL,
      stringsAsFactors = FALSE
    )
    
    return(result_table)
  }
  
  # Frequency of tracts
  freq <- function(df, position = 3749970) {
    samples_fix <- df[df$population == 1 & df$left < position & df$right > position, ]
    
    freq <- length(samples_fix$sample) / length(unique(df$sample))
    
    return(freq)
  }
  
  mean_lengths <- c()
  labels_pop <- c()
  generations <- c()
  simulation_names <- c()
  frequencies <- c()
  
  csv_files <- list.files(simu_dir, pattern = "\\.csv$", full.names = TRUE)
  
  for (csv_file in csv_files) {
    # Extract pop and generation from filename
    fname <- basename(csv_file)
    
    pop_match <- regmatches(fname, regexec("at_pop(\\d+)_generation(\\d+)\\.csv", fname))[[1]]
    pop <- as.numeric(pop_match[2])
    gen <- as.numeric(pop_match[3])
    
    at_pop <- read.csv(csv_file)
    
    # Calculate tracts, lengths, frequency
    tracts_pop_rob <- tracts_pop(at_pop)
    length_pop <- calculate_lengths(tracts_pop_rob)
    mean_length <- mean(length_pop$length, na.rm = TRUE)
    freq_pop <- freq(at_pop)
    
    mean_lengths <- c(mean_lengths, mean_length)
    labels_pop <- c(labels_pop, pop)
    generations <- c(generations, gen)
    simulation_names <- c(simulation_names, basename(simu_dir))
    frequencies <- c(frequencies, freq_pop)
  }
  
  # Create final table
  data_all <- data.frame(
    Simulation = simulation_names,
    Population = labels_pop,
    Generation = generations,
    Mean_Length = mean_lengths,
    Frequency = frequencies
  )
  
  return(data_all)
}

