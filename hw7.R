n <- 31
sigma <- 3.08
x_bar <- 46.78
alpha <- 0.005
mua <- 45
c <- 1 - alpha

z_ts <- (x_bar - mua) / (sigma / sqrt(n))
z_critical <- qnorm(1 - alpha)
z_ts_round <- round(z_ts, 5)
z_critical_round <- round(z_critical, 5)

p_value <- pnorm(z_ts, lower.tail = FALSE)
p_value_round <- round(p_value, 5)

alpha_2 <- alpha / 2
z_alpha_2 <- qnorm(alpha_2, lower.tail = FALSE)

# Confidence Interval
C_lower <- x_bar - (z_alpha_2 * (sigma / sqrt(n)))
C_upper <- x_bar + (z_alpha_2 * (sigma / sqrt(n)))  # ← don't forget this!
# One-sided CI (matches right-tailed test at α = 0.005)
C_lower_one_sided <- x_bar - (z_critical * (sigma / sqrt(n)))
# Interval: (C_lower_one_sided, ∞)
