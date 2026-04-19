
  n <- 65
  p <- 0.45
  mu <- (n * p)
  sigma <- sqrt(n * p * (1-p))
  D2 <- dbinom(47, 65, 0.45)
  D4a <- (1 - pbinom(47, 65, 0.45))
  D4b <- pbinom(47.5, 65, 0.45, lower.tail = FALSE)
  cat("mu = ", mu, "\n")
  cat("sd = ", sigma, "\n")
  cat("P(x = 47", format(D2, scientific = FALSE), "\n")
  cat("P_a(x > 47)", format(D4a, scientific = FALSE), "\n")
  cat("P_b(x > 47.5) = ", format(round(D4b, 5), scientific = FALSE), "\n")
  D4b <- pnorm(47.5, mu, sigma, lower.tail = FALSE)
  cat("P_b(x > 47.5) = ", format(round(D4b, 5), scientific = FALSE), "\n")  
  
  
  