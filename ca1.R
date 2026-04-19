n <- 17
sigma <- 11.8
s <- sigma
mau <- 202
X_bar <- mau
C <- 0.955
alpha <- 1 - C
alpha_2 <- alpha / 2
df <- n - 1

z <- qnorm(alpha_2, 0, 1, lower.tail = FALSE)         # z score
t <- qt(alpha_2, df, lower.tail = FALSE)
BigZ <- qnorm(alpha_2, lower.tail = FALSE)
t_lower <- qt(alpha, df, lower.tail = TRUE)


lower_bound <- X_bar- (t * (sigma/ (sqrt(n))))
upper_bound <- X_bar + (t * (sigma/ (sqrt(n))))
lower_t_lail_fuck_you <- X_bar + (t_lower * (sigma / sqrt(n)))


cat( "Z alpha/2 ", round(z,4), "\n")
cat( "t alpha/2 ", round(t,4), "\n")

cat("lower", lower_bound, "\t", "upper", upper_bound, "\n")
0
t_c <- (lower_bound - X_bar) / (sigma / sqrt(n))
cat(round(t_c,4))
cat(round(t_lower,4))
cat(round(lower_t_lail_fuck_you,4))
