head(appRating_data_clean)





#Gpol - rPol
X_bar_G <- mean(appRating_data_clean$SentiGPol)
X_bar_R <- mean(appRating_data_clean$SentiRPol)
sd_g <- sd(appRating_data_clean$SentiGPol)
sd_r <- sd(appRating_data_clean$SentiRPol)
n_g <- 1014
n_r <- 1014
D_bar <- X_bar_G - X_bar_R
D <- (c(appRating_data_clean$SentiGPol) - c(appRating_data_clean$SentiRPol))

sd_dd <- sd(D)

sddalpha <- 0.05
C <- 1-alpha

mu_0 <- 0
df <- 1014 -1
SE <- sqrt((sd_g^2/n_g) + (sd_r^2/n_r))


t.test(appRating_data_clean$SentiGPol, appRating_data_clean$SentiRPol,
       mu_0,
       0.95,
       paired = TRUE,
       alternative = "two.sided")

t_critical <- qt(1 - alpha/2, df)
t_critical

