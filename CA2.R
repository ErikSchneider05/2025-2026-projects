appRating_data_clean <- read.csv("appRating_data_clean.csv") 
head(appRating_data_clean)
unique_apps_data <- appRating_data_clean[!duplicated(appRating_data_clean$App), ] 
unique_apps_data.subset <- subset(unique_apps_data, 
                                  ContRating == 'Everyone' | 
                                    ContRating == 'Everyone 10+')
hist(unique_apps_data.subset$AppRating, breaks = 8)
hist(unique_apps_data.subset$AppRating, breaks = 9, 
     freq = FALSE)   # freq=FALSE is required for density curve
lines(density(unique_apps_data.subset$AppRating), 
      col = "red", 
      lwd = 2)
#historgram

boxplot(unique_apps_data.subset$AppRating)
#box plot


qqnorm(unique_apps_data.subset$AppRating,
       main = "Q-Q Plot of App Ratings",
       xlab = "Theoretical Quantiles",
       ylab = "Sample Quantiles",
       col  = "steelblue",
       pch  = 19)        # pch = point shape (19 = filled circle)
qqline(unique_apps_data.subset$AppRating, 
       col = "red", 
       lwd = 2)          # lwd = line width
#qq line

# Setup
n         <- nrow(unique_apps_data.subset)
mean_rating <- mean(unique_apps_data.subset$AppRating, na.rm = TRUE)
sd_rating   <- sd(unique_apps_data.subset$AppRating, na.rm = TRUE)
se_rating   <- sd_rating / sqrt(n)
df          <- n - 1
mu_0        <- 4.5

# Critical value
t_critical <- qt(0.975, df)  # 2-sided 95%

# Confidence interval
lower_bound <- mean_rating - t_critical * se_rating
upper_bound <- mean_rating + t_critical * se_rating
cat("Lower bound:", lower_bound, "\n")
cat("Upper bound:", upper_bound, "\n")

# t.test
t.test(unique_apps_data.subset$AppRating,
       alternative = "greater",
       conf.level  = 0.95)

# Test statistic
test_stat <- (mean_rating - mu_0) / (sd_rating / sqrt(n))
test_stat

# P-value
pt(test_stat, df, lower.tail = FALSE)

