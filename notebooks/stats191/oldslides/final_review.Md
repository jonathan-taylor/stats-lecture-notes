### Final review

Overview

-   Simple linear regression.

-   Diagnostics for simple linear regression.

-   Multiple linear regression.

-   Diagnostics.

-   Interactions and ANOVA.

-   Weighted Least Squares.

-   Autocorrelation.

-   Model selection.

-   Logistic regression.

-   Poisson regression.

### Simple linear regression

### Simple linear regression

Least squares

-   We will be using “least squares” regression. This measures the
    goodness of fit of a line by the sum of squared errors, $SSE$.

-   Least squares regression chooses the line that minimizes
    $$SSE(\beta_0, \beta_1) = \sum_{i=1}^n (Y_i - \beta_0 - \beta_1 \cdot X_i)^2.$$

### Geometry of Least Squares: Simple Linear Model

### Simple linear regression

What is a $t$-statistic?

-   Start with $Z \sim N(0,1)$ is standard normal and
    $S^2 \sim \chi^2_{\nu}$, independent of $Z$.

-   Compute $$T = \frac{Z}{\sqrt{\frac{S^2}{\nu}}}.$$

-   Then, $T \sim t_{\nu}$ has a $t$-distribution with $\nu$ degrees of
    freedom.

-   Generally, a $t$-statistic has the form $$ T = $$

### Simple linear regression

Interval for $\beta_1$

A $(1-\alpha) \cdot 100 \%$ confidence interval:
$$\widehat{\beta}_1 \pm SE(\widehat{\beta}_1) \cdot t_{n-2, 1-\alpha/2}.$$

Interval for regression line $\beta_0 + \beta_1 \cdot X$

-   $(1-\alpha) \cdot 100 \%$ confidence interval:
    $$\widehat{\beta}_0 + \widehat{\beta}_1 X \pm SE(\widehat{\beta}_0 + \widehat{\beta}_1 X) \cdot t_{n-2, 1-\alpha/2}$$
    where
    $$SE(a_0\widehat{\beta}_0 + a_1\widehat{\beta}_1) = \widehat{\sigma} \sqrt{\frac{a_0^2}{n} + \frac{(a_0\overline{X} - a_1)^2}{\sum_{i=1}^n \left(X_i-\overline{X}\right)^2}}$$

### Simple linear regression

Predicting a new observation

-   $$SE(\widehat{\beta}_0 + \widehat{\beta}_1 X_{\text{new}} + \varepsilon_{\text{new}}) = \widehat{\sigma} \sqrt{1 + \frac{1}{n} + \frac{(\overline{X} - X_{\text{new}})^2}{\sum_{i=1}^n \left(X_i-\overline{X}\right)^2}}.$$

-   Prediction interval is
    $$\widehat{\beta}_0 +  \widehat{\beta}_1 X_{\text{new}} \pm t_{n-2, 1-\alpha/2} \cdot SE(\widehat{\beta}_0 + \widehat{\beta}_1 X_{\text{new}} + \varepsilon_{\text{new}})$$

### Simple linear diagnostics

Sums of squares

$$\begin{aligned}
   SSE &= \sum_{i=1}^n(Y_i - \widehat{Y}_i)^2 = \sum_{i=1}^n (Y_i - \widehat{\beta}_0 - \widehat{\beta}_1 X_i)^2 \\
   SSR &= \sum_{i=1}^n(\overline{Y} - \widehat{Y}_i)^2 = \sum_{i=1}^n (\overline{Y} - \widehat{\beta}_0 - \widehat{\beta}_1 X_i)^2 \\
   SST &= \sum_{i=1}^n(Y_i - \overline{Y})^2 = SSE + SSR \\
   R^2 &= \frac{SSR}{SST} = 1 - \frac{SSE}{SST} = \widehat{Cor}(\pmb{X},\pmb{Y})^2.
   \end{aligned}$$

Basic idea: if $R^2$ is large: a lot of the variability in $\pmb{Y}$ is
explained by $\pmb{X}$.

### Simple linear diagnostics

$F$-test in simple linear regression

-   *Full (bigger) model :*

    $$FM: \qquad Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i$$

-   *Reduced (smaller) model:*

    $$RM: \qquad Y_i = \beta_0  + \varepsilon_i$$

-   The $F$-statistic has the form
    $$F=\frac{(SSE(RM) - SSE(FM)) / (df_{RM} - df_{FM})}{SSE(FM) / df_{FM}}.$$

-   Reject $H_0: RM$ is correct, if $F > F_{1-\alpha, 1, n-2}$.

### Simple linear diagnostics

What are the assumptions

-   $$Y_i = \beta_0 + \beta_1 X_{i} + \varepsilon_i$$

-   Errors $\varepsilon_i$ are assumed independent $N(0,\sigma^2)$.

### Residuals from linear model

[R
code](http://stats191.stanford.edu/simple_diagnostics.html#poorly-fitting-linear-model)

### Quadratic model

[R
code](http://stats191.stanford.edu/simple_diagnostics.html#poorly-fitting-linear-model)

### Residuals from quadratic model

[R
code](http://stats191.stanford.edu/simple_diagnostics.html#poorly-fitting-linear-model)

### QQplot of residuals from quadratic model

[R
code](http://stats191.stanford.edu/simple_diagnostics.html#poorly-fitting-linear-model)

### Simple linear diagnostics

[R
code](http://stats191.stanford.edu/simple_diagnostics.html#outlier-and-nonconstant-variance)

### Multiple linear regression model

Specifying the model

-   Rather than one predictor, we have $p=6$ predictors.

-   $$Y_i = \beta_0 + \beta_1 X_{i1} + \dots + \beta_p X_{ip} + \varepsilon_i$$

-   Errors $\varepsilon$ are assumed independent $N(0,\sigma^2)$, as in
    simple linear regression.

-   Coefficients are called (partial) regression coefficients because
    they “allow” for the effect of other variables.

### Geometry of Least Squares: Multiple Regression

### Multiple linear regression

$F$-test

-   *Full (bigger) model :*

    $$Y_i = \beta_0 + \beta_1 X_{i1} + \dots \beta_p X_{ip} + \varepsilon_i$$

-   *Reduced (smaller) model:*

    $$Y_i = \beta_0  + \varepsilon_i$$

-   The $F$-statistic has the form
    $$F=\frac{(SSE(R) - SSE(F)) / (df_R - df_F)}{SSE(F) / df_F}.$$

### Multiple linear regression

Matrix formulation

$${\pmb Y}_{n \times 1} = \pmb{X}_{n \times (p + 1)} \pmb{\beta}_{(p+1) \times 1} + \pmb{\varepsilon}_{n \times 1}$$

-   $\pmb{X}$ is called the *design matrix* of the model

-   $\pmb{\varepsilon} \sim N(0, \sigma^2 I_{n \times n})$ is
    multivariate normal

$SSE$ in matrix form

$$SSE(\beta) = (\pmb{Y} - \pmb{X} \pmb{\beta})'(\pmb{Y} - \pmb{X} \pmb{\beta})$$

### Multiple linear regression

Least squares solution

-   Normal equations
    $$\frac{\partial}{\partial \beta_j} SSE \biggl|_{\widehat{\beta}_{}} = -2 \left(\pmb{Y} - \pmb{X} \widehat{\beta}_{} \right)^t \pmb{X}_j = 0, \qquad 0 \leq j \leq p.$$

-   Equivalent to $$\begin{aligned}
       (\pmb{Y} - \pmb{X}\pmb{\widehat{\beta}_{}})^t\pmb{X} &= 0 \\
       \pmb{\widehat{\beta}_{}} &= (\pmb{X}^t\pmb{X})^{-1}\pmb{X}^t\pmb{Y}
       \end{aligned}$$

-   Properties: $$ \~N(, ^2^ (^t^ )^-1^ ), $$

-   [R code](http://stats191.stanford.edu/multiple.html)

### Multiple linear regression

Confidence interval for $\sum_{j=0}^p a_j \beta_j$

-   Suppose we want a $(1-\alpha)\cdot 100\%$ CI for
    $\sum_{j=0}^p a_j\beta_j$.

-   Just as in simple linear regression:

    $$\sum_{j=0}^p a_j \widehat{\beta}_j \pm t_{1-\alpha/2, n-p-1} \cdot SE\left(\sum_{j=0}^p a_j\widehat{\beta}_j\right).$$

### Multiple linear regression

General $F$-tests

-   Given two models $R \subset F$ (i.e. $R$ is a subspace of $F$), we
    can consider testing $$ H~0~: $$vs.$$ H~a~:
    .$$\item The test statistic is$$ F = $$

-   If $H_0$ is true, $F \sim F_{df_R-df_F, df_F}$ so we reject $H_0$ at
    level $\alpha$ if $F > F_{df_R-df_F, df_F, 1-\alpha}$.

### Diagnostics

What can go wrong?

-   Regression function can be wrong: maybe regression function should
    be quadratic (see ).

-   Model for the errors may be incorrect:

    -   may not be normally distributed.

    -   may not be independent.

    -   may not have the same variance.

-   Detecting problems is more *art* then *science*, i.e. we cannot
    *test* for all possible problems in a regression model.

-   Basic idea of diagnostic measures: if model is correct then
    residuals $e_i = Y_i -\widehat{Y}_i, 1 \leq i \leq n$ should look
    like a sample of (not quite independent) $N(0, \sigma^2)$ random
    variables.

### Diagnostics

### Diagnostics

$DFFITS$

-   $$DFFITS_i = \frac{\widehat{Y}_i - \widehat{Y}_{i(i)}}{\widehat{\sigma}_{(i)} \sqrt{H_{ii}}}$$

### Diagnostics

Cook’s distance

-   $$D_i = \frac{\sum_{j=1}^n(\widehat{Y}_j - \widehat{Y}_{j(i)})^2}{(p+1) \, \widehat{\sigma}^2}$$

### Influence of an observation

$DFBETAS$

-   $$DFBETAS_{j(i)} = \frac{\widehat{\beta}_j - \widehat{\beta}_{j(i)}}{\sqrt{\widehat{\sigma}^2_{(i)} (X^TX)^{-1}_{jj}}}.$$

### Diagnostics

Outliers

-   Observations $(Y, X_1, \dots, X_p)$ that do not follow the model,
    while most other observations seem to follow the model.

-   One solution: Bonferroni correction, threshold at
    $t_{1 - \alpha/(2*n), n-p-2}$.

-   Bonferroni: if we are doing many $t$ (or other) tests, say $m >>1$
    we can control overall false positive rate at $\alpha$ by testing
    each one at level $\alpha/m$.

### No difference

[R
code](http://stats191.stanford.edu/interactions.html#minority-employment-data)

### Different slopes, same intercept

[R
code](http://stats191.stanford.edu/interactions.html#minority-employment-data)

### Different intercepts, same slope

[R
code](http://stats191.stanford.edu/interactions.html#minority-employment-data)

### Different intercepts, different slopes

[R
code](http://stats191.stanford.edu/interactions.html#minority-employment-data)

### ANOVA models

ANOVA table: One-way

-   
      Source                                                   $SS$                                                       $df$                                  $E(MS)$
      ------------ -------------------------------------------------------------------------------------------- ------------------------ ------------------------------------------------------
      Treatments    $SSTR = \sum_{i=1}^r n_i \left(\overline{Y}_{i\cdot} - \overline{Y}_{\cdot\cdot}\right)^2$           $r-1$            $\sigma^2 + \frac{\sum_{i=1}^r n_i \alpha_i^2}{r-1}$
      Error                  $SSE = \sum_{i=1}^r \sum_{j=1}^{n_i}(Y_{ij} - \overline{Y}_{i\cdot})^2$             $\sum_{i=1}^r n_i - r$                        $\sigma^2$

### ANOVA models

ANOVA table: Two-way (assuming $n_{ij}=n$)

  Term                                                                                      $SS$
  ------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  $A$                                        $SSA = nm\sum_{i=1}^r  \left(\overline{Y}_{i\cdot\cdot} - \overline{Y}_{\cdot\cdot\cdot}\right)^2$
  $B$                                       $SSB = nr\sum_{j=1}^m  \left(\overline{Y}_{\cdot j\cdot} - \overline{Y}_{\cdot\cdot\cdot}\right)^2$
  $AB$     $SSAB = n\sum_{i=1}^r \sum_{j=1}^m  \left(\overline{Y}_{ij\cdot} - \overline{Y}_{i\cdot\cdot} - \overline{Y}_{\cdot j\cdot} + \overline{Y}_{\cdot\cdot\cdot}\right)^2$
  Error                                             $SSE = \sum_{i=1}^r \sum_{j=1}^m \sum_{k=1}^{n}(Y_{ijk} - \overline{Y}_{ij\cdot})^2$

### ANOVA models

ANOVA table: Two-way (assuming $n_{ij}=n$)

-   
      $SS$          $df$                                          $E(MS)$
      -------- -------------- --------------------------------------------------------------------------------
      $SSA$        $r-1$                     $\sigma^2 + nm\frac{\sum_{i=1}^r \alpha_i^2}{r-1}$
      $SSB$        $m-1$                     $\sigma^2 + nr\frac{\sum_{j=1}^m \beta_j^2}{m-1}$
      $SSAB$    $(m-1)(r-1)$   $\sigma^2 + n\frac{\sum_{i=1}^r\sum_{j=1}^m (\alpha\beta)_{ij}^2}{(r-1)(m-1)}$
      $SSE$      $(n-1)mr$                                       $\sigma^2$

-   Also talked briefly about random effects.

### Weighted least squares

Weighted Least Squares

-   Weighted Least Squares
    $$SSE(\beta, w) = \sum_{i=1}^n w_i \left(Y_i - \beta_0 - \beta_1 X_i\right)^2.$$

-   In general, weights should be like:
    $$w_i = \frac{1}{\text{Var}(\varepsilon_i)}.$$

-   Briefly talked about efficiency of estimators.

### NASDAQ daily close 2011

[R code](http://stats191.stanford.edu/correlated_errors.html#nasdaq)

### Correlated errors

AR(1) noise

-   Suppose that, instead of being independent, the errors in our model
    were
    $$\varepsilon_t = \rho \cdot \varepsilon_{t-1} + \omega_t, \qquad -1 < \rho < 1$$
    with $\omega_t \sim N(0,\sigma^2)$ independent.

-   If $\rho$ is close to 1, then errors are very correlated, $\rho=0$
    is independence.

-   This is “Auto-Regressive Order (1)” noise (AR(1)). Many other models
    of correlation exist: ARMA, ARIMA, ARCH, GARCH, etc.

### Correlated errors

Correcting for AR(1)

-   Suppose we know $\rho$, if we “whiten” the data and regressors
    $$\begin{aligned}
       \tilde{Y}_{t+1} &= Y_{t+1} - \rho Y_t, t > 1   \\
       \tilde{X}_{(t+1)j} &= X_{(t+1)j} - \rho X_{tj}, i > 1
       \end{aligned}$$ for $1 \leq t \leq n-1$. This model satisfies
    “usual” assumptions, i.e. the errors
    $$\tilde{\varepsilon}_t = \omega_{t+1} = \varepsilon_{t+1} - \rho \cdot \varepsilon_t$$
    are independent $N(0,\sigma^2)$.

-   For coefficients in new model $\tilde{\beta}$,
    $\beta_0 = \tilde{\beta}_0 / (1 - \rho)$,
    $\beta_j = \tilde{\beta}_j.$

-   Problem: in general, we don’t know $\rho$.

### Model selection

Criteria

-   $$C_p({\cal M}) = \frac{SSE({\cal M})}{\widehat{\sigma}^2} + 2 \cdot p({\cal M}) - n.$$

-   Akaike (AIC) defined as
    $$AIC({\cal M}) = - 2 \log L({\cal M}) + 2 p({\cal M})$$ where
    $L({\cal M})$ is the maximized likelihood of the model.

-   Bayes (BIC) defined as
    $$BIC({\cal M}) = - 2 \log L({\cal M}) + \log n \cdot p({\cal M})$$

-   Adjusted $R^2$

-   Stepwise (step) vs. best subsets (leaps).

### Shrinking an estimator

[R
code](http://stats191.stanford.edu/selection.html#bias-variance-tradeoff)

### Model selection

$K$-fold cross-validation

-   Fix a model ${\cal M}$. Break data set into $K$ approximately equal
    sized groups $(G_1, \dots, G_K)$.

-   for (i in 1:K)

    Use all groups except $G_i$ to fit model, predict outcome in group
    $G_i$ based on this model
    $\widehat{Y}_{j,{\cal M}, G_i}, j \in G_i$.

-   Estimate
    $$CV({\cal M}) = \frac{1}{n}\sum_{i=1}^K \sum_{j \in G_i} (Y_j - \widehat{Y}_{j,{\cal M},G_i})^2.$$

### Logistic regression

Logistic model

-   Logistic model
    $$\pi(X_1,X_2) = \frac{\exp(\beta_0 + \beta_1 X_1 + \beta_2 X_2)}{1 + \exp(\beta_0 + \beta_1 X_1 + \beta_2 X_2)}$$

-   This automatically fixes $0 \leq E(Y) = \pi(X_1,X_2) \leq 1$.

-   **Note:**

    $$\text{logit}(\pi(X_1, X_2)) = \log\left(\frac{\pi(X_1, X_2)}{1 - \pi(X_1,X_2)}\right) = \beta_0 + \beta_1 X_1 + \beta_2 X_2$$

### Logistic regression

Odds Ratios

-   One reason logistic models are popular is that the parameters have
    simple interpretations in terms of **odds**
    $$ODDS(A) = \frac{P(A)}{1-P(A)}.$$

-   Logistic model:
    $$OR_{X_j} = \frac{ODDS(\dots, X_j=x_j+1, \dots)}{ODDS(\dots, X_j=x_j, \dots)} = e^{\beta_j}$$

-   If $X_j \in {0, 1}$ is dichotomous, then odds for group with
    $X_j = 1$ are $e^{\beta_j}$ higher, other parameters being equal.

### Logistic regression

Deviance

-   For a model ${\cal M}$, $DEV({\cal M})$ replaces $SSE({\cal M})$.

-   In least squares regression, we use
    $$SSE({\cal M}_R) - SSE({\cal M}_F) \sim \sigma^2 \chi^2_{df_R-df_F}$$

-   This is replaced with
    $$DEV({\cal M}_R) - DEV({\cal M}_F) \overset{n \rightarrow \infty}{\sim} \chi^2_{df_R-df_F}$$

-   An example of a *generalized linear model*.

### Poisson regression

Poisson (log-linear) regression model

-   Given observations and covariates
    $Y_i , X_{ij} , 1 \leq i  \leq n, 1 \leq j  \leq p$.

-   **Model:**

    $$Y_{i} \sim Poisson \left(\exp\left(\beta_0 + \sum_{j=1}^p \beta_j X_{ij} \right)\right)$$

-   Poisson assumption implies the variance function is
    $$V (\mu) = \mu.$$

### Poisson regression

Interpretation of coefficients

-   The log-linear model means covariates have *multiplicative* effect.

-   Log-linear model model:
    $$\frac{E(Y|\dots, X_j=x_j+1, \dots)}{E(Y|\dots, X_j=x_j, \dots)} = e^{\beta_j}$$

-   So, one unit increase in variable $j$ results in $e^{\beta_j}$
    (multiplicative) increase the expected count, all other parameters
    being equal.


