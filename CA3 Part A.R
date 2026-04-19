# Sample statistics



tapply(appRating_data_clean$lRevLen, appRating_data_clean$SentiG2, mean)
tapply(appRating_data_clean$lRevLen, appRating_data_clean$SentiG2, sd)


n_neg <- 676
n_pos <- 338
X_bar_neg <- 4.511774
X_bar_pos <- 4.498749
sd_neg <- 0.8636239
sd_pos <- 0.7738515
mu_0 <- 0
alpha <- 0.05

# Welch's degrees of freedom (defined AFTER sd values)
df <- ((sd_neg^2/n_neg) + (sd_pos^2/n_pos))^2 / 
  (((sd_neg^2/n_neg)^2 / (n_neg - 1)) + 
     ((sd_pos^2/n_pos)^2 / (n_pos - 1)))

# Difference and Standard Error
D_bar <- X_bar_neg - X_bar_pos
SE <- sqrt((sd_neg^2/n_neg) + (sd_pos^2/n_pos))

# Test statistic
t_ts <- (D_bar - mu_0) / SE

# Critical value & p-value (two-tailed)
t_critical <- qt(1 - alpha, df)
pvalue <-  pt((t_ts), df = df, lower.tail = FALSE)

# Confidence interval
lower_bound <- D_bar - qt(1 - alpha, df) * SE
upper_bound <- D_bar + qt(1 - alpha, df) * SE

# Results
cat("t-statistic:", t_ts, "\n")
cat("df:", df, "\n")
cat("t-critical:", t_critical, "\n")
cat("p-value:", pvalue, "\n")
cat("95% CI: [", lower_bound, ",", upper_bound, "]\n")
t_critical

