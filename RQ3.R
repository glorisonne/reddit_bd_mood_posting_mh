# ToDo check which libraries do need and for what
library(car) #vif function for collinearity checks
#library(ggplot2)
#library(gridExtra)
library(languageR) # collinearity checks
#library(Hmisc) # variable hierarchical clustering
#library(matrixStats) # SD for multiple columns
# install.packages("caret")
library(caret) #confusionMatrix function for accuracy evaluation
# library(mdscore) # log ratio test for glm https://rdrr.io/cran/mdscore/man/lr.test.html (lr.test yields almost same results as anova with Chisq)
#library(flexmix) # BIC function for glm
library(ROCR) # precision-recall curve for accuracy evaluation

# references
# Field: Field, A., Miles, J., & Field, Z. (2012). Discovering Statistics Using R. SAGE Publications Inc.

data_folder = "data/" # "C:/Users/glori/Documents/Persönliches/#PhD_local/data/"
dataset = "users_rq3-new.csv" # "users_rq3.csv", "users_rq3-new.csv" # "users_rq3-25wtotal.csv"

df = read.csv(paste(data_folder, dataset, sep=""), fileEncoding='UTF-8-BOM', sep=",")
# number of cases
print(nrow(df))
print(nrow(df[complete.cases(df), ]))
nrow(df[df$posted_MH == 0, ])
nrow(df[df$posted_MH == 1, ])

controls <- c("avg_posting_age", "gender", "active_days", "activity")
liwc <- c("posemo", "anx", "sad", "anger", "i")

# model with controls only
model.controls <- glm(posted_MH ~ avg_posting_age + gender + active_days + activity,
                      data = df, family = binomial(link="logit"))
summary(model.controls)

# model with controls + LIWC variables
model.liwc_w_controls <- glm(posted_MH ~ avg_posting_age + gender + active_days + activity
                             + posemo + anx + anger + sad + i,
                             data = df, family = binomial(link="logit"))
summary(model.liwc_w_controls)

## Evaluate model fit
# compare controls only to LIWC + controls model
BIC(model.controls)
BIC(model.liwc_w_controls)

# important to specify Chisq, otherwise do not get significance results
anova(model.controls, model.liwc_w_controls, test = "Chisq")

# function from Field (2012) p. 334
logisticPseudoR2s <- function(LogModel) {
  dev <- LogModel$deviance
  nullDev <- LogModel$null.deviance
  modelN <- length(LogModel$fitted.values)
  
  R.hl <- 1 - dev / nullDev
  R.cs <- 1 - exp(-(nullDev - dev) / modelN)
  R.n <- R.cs / (1 - (exp (-(nullDev / modelN))))
  
  cat("Pseudo R^2 for logistic regression\n")
  cat("Hosmer and Lemeshow R2 ", round(R.hl, 3), "\n")
  cat("Cox and Snell R2 ", round(R.cs, 3), "\n")
  cat("Nagelkerke R2 ", round(R.n, 3), "\n")
}
logisticPseudoR2s(model.liwc_w_controls)

## Confidence intervals for coefficients + odds ratios
# confidence intervals for the coefficients
# confint() prodcues profile confidence intervals (https://stats.stackexchange.com/questions/275416/computing-confidence-intervals-for-coefficients-in-logistic-regression)
# confint.default uses Wald method https://stats.stackexchange.com/questions/5304/why-is-there-a-difference-between-manually-calculating-a-logistic-regression-95/5320#5320
confint.default(model.liwc_w_controls)

# odds ratio of coefficients and their confidence intervals
# see Field (2012), p. 335
exp(model.liwc_w_controls$coefficients)
exp(confint(model.liwc_w_controls))

## Collinearity
# pairwise correlations
corrs <- cor(df[, c(liwc, controls)], df[, c(liwc, controls)], use = "pairwise.complete.obs", method = "spearman")
print(corrs)

# collinearity of controls + LIWC predictors
collin.fnc(df[, c(4:12)])$cnumber

# multicollinearity?
multicollinearity_checks <- function(model){
  # guidelines for interpreting: Field p. 298
  # largest VIF should be < 10
  # mean VIF should be <= 1
  # Tolerance should be >= 0.2 (0.1)
  variance_inflation_factor = vif(model)
  print("variance inflation factor (VIF) (max < 10)")
  print(variance_inflation_factor)
  print("mean VIF (should be <= 1)")
  print(mean(variance_inflation_factor))
  tolerance = 1 / variance_inflation_factor
  print("Tolerance (= 1/VIF, min should be > 0.1/0.2)")
  print(tolerance)
}

multicollinearity_checks(model.liwc_w_controls)

## test for linearity of the logit (Field p. 343 ff)
# include IVs that are the interaction of the IV and the log of the IV
for (iv in c(liwc, c("avg_posting_age", "active_days", "activity"))) {
  df[paste("log", iv, sep = "_")] <- log(df[, iv])*df[, iv]
}

# run controls + LIWC model with log interactions
model.liwc_w_controls_log_interactions <- glm(posted_MH ~ avg_posting_age + gender + active_days + activity
                                              + posemo + anx + anger + sad + i
                                              + log_avg_posting_age + log_active_days + log_activity
                                              + log_posemo + log_anx + log_anger + log_sad + log_i, 
                                              data = df, family = binomial(link="logit"))
summary(model.liwc_w_controls_log_interactions)
logisticPseudoR2s(model.liwc_w_controls_log_interactions)

## model accuracy
# confusion matrix
df$predict_p_posted_MH = predict(model.liwc_w_controls, type = "response")
df$predict_posted_MH = ifelse(df$predict_p_posted_MH >= 0.5, 1, 0)
confusionMatrix(as.factor(df$predict_posted_MH), as.factor(df$posted_MH))

# precision-recall curve
# ROC curve https://stats.stackexchange.com/questions/6067/does-an-unbalanced-sample-matter-when-doing-logistic-regression
pred <- prediction(df$predict_p_posted_MH, df$posted_MH)
perf <- performance(pred, "prec", "rec")
plot(perf, colorize=TRUE)

## gender-balanced dataset
dataset = "users_rq3-new_gender_balanced.csv"
df = read.csv(paste(data_folder, dataset, sep=""), fileEncoding='UTF-8-BOM', sep=",")

# number of cases
print(nrow(df))
nrow(df[df$posted_MH == 0, ])
nrow(df[df$posted_MH == 1, ])

# model with controls only
model.controls <- glm(posted_MH ~ avg_posting_age + gender + active_days + activity,
                      data = df, family = binomial(link="logit"))
summary(model.controls)

# model with controls + LIWC variables
model.liwc_w_controls <- glm(posted_MH ~ avg_posting_age + gender + active_days + activity
                             + posemo + anx + anger + sad + i,
                             data = df, family = binomial(link="logit"))
summary(model.liwc_w_controls)

## Model fit
BIC(model.controls)
BIC(model.liwc_w_controls)
anova(model.controls, model.liwc_w_controls, test = "Chisq")

logisticPseudoR2s(model.liwc_w_controls)

## Confidence intervals
confint.default(model.liwc_w_controls)
exp(model.liwc_w_controls$coefficients)
exp(confint(model.liwc_w_controls))

## Model accuracy
df$predict_p_posted_MH = predict(model.liwc_w_controls, type = "response")
df$predict_posted_MH = ifelse(df$predict_p_posted_MH >= 0.5, 1, 0)
confusionMatrix(as.factor(df$predict_posted_MH), as.factor(df$posted_MH))

