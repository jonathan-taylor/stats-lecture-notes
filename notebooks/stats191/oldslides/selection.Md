### Topics

Outline

-   Goals of model selection.

-   Criteria to compare models.

-   (Some) model selection.

-   Bias- variance trade-off.

### Election data

Description

   Variable  Description
  ---------- -------------------------------------------------------
     $V$     votes for a presidential candidate
     $I$     are they incumbent?
     $D$     Democrat or Republican incumbent?
     $W$     wartime election?
     $G$     GDP growth rate in election year
     $P$     (absolute) GDP deflator growth rate
     $N$     number of quarters in which GDP growth rate $> 3.2\%$

### Model selection

Problem & Goals

-   When we have many predictors (with many possible interactions), it
    can be difficult to find a good model.

-   Which main effects do we include?

-   Which interactions do we include?

-   Model selection procedures try to *simplify / automate* this task.

-   Election data has $2^6=64$ different models with just main effects!

### Model selection

General comments

-   This is an “unsolved” problem in statistics: there are no magic
    procedures to get you the “best model.”

-   In some sense, model selection is “data mining.”

-   Data miners / machine learners often work with very many predictors.

-   Our model selection problem is generally at a much smaller scale
    than “data mining” problems.

### Model selection

Hypothetical example

-   Suppose we fit a a model
    $$F: \quad Y_{n \times 1} = X_{n \times (p+1)} \beta_{(p+1) \times 1} + \varepsilon_{n \times 1}$$
    with predictors ${\pmb X}_1, \dots, {\pmb X}_p$.

-   In reality, some of the $\beta$’s may be zero. Let’s suppose that
    $\beta_{j+1}= \dots= \beta_{p+1}=0$.

-   Then, any model that includes $\beta_0, \dots, \beta_j$ is
    *correct*: which model gives the *best* estimates of
    $\beta_0, \dots, \beta_j$?

-   Principle of *parsimony* (i.e. Occam’s razor) says that the model
    with *only* $\pmb{X}_1, \dots, \pmb{X}_j$ is “best”.

### Model selection

Hypothetical example: continued

-   For simplicity, let’s assume that $j=1$ so there is only one
    coefficient to estimate.

-   Then, because each model gives an *unbiased* estimate of $\beta_1$
    we can compare models based on $$\text{Var}(\widehat{\beta}_1).$$

-   The best model, in terms of this variance, is the one containing
    only ${\pmb X}_1$.

-   What if we didn’t know that only $\beta_1$ was non-zero (which we
    don’t know in general)?

### Model selection

Strategies

-   To “implement” a model selection procedure, we first need a
    criterion or benchmark to compare two models.

-   Given a criterion, we also need a search strategy.

-   With a limited number of predictors, it is possible to search all
    possible models (leaps in R).

### Model selection

Possible criteria

-   $R^2$: not a good criterion. Always increase with model size
    $\implies$ “optimum” is to take the biggest model.

-   Adjusted $R^2$: better. It “penalized” bigger models. Follows
    principle of parsimony / Occam’s razor.

-   Mallow’s $C_p$ – attempts to estimate a model’s predictive power,
    i.e. the power to predict a new observation.

### Best subsets, $R^2$

[R
code](http://stats191.stanford.edu/selection.html#election-example-best-subset)

### Best subsets, adjusted $R^2$

[R
code](http://stats191.stanford.edu/selection.html#election-example-best-subset)

### Model selection

Mallow’s $C_p$

-   $$C_p({\cal M}) = \frac{SSE({\cal M})}{\widehat{\sigma}^2} + 2 \cdot p({\cal M}) - n.$$

-   $\widehat{\sigma}^2=SSE(F)/df_F$ is the “best” estimate of
    $\sigma^2$ we have (use the fullest model), i.e. in the election
    data it uses all 6 main effects.

-   $SSE({\cal M})$ is the $SSE$ of the model ${\cal M}$.

-   $p({\cal M})$ is the number of predictors in ${\cal M}$.

-   This is an estimate of the expected mean-squared error of
    $\widehat{Y}({\cal M})$, it takes *bias* and *variance* into
    account.

### Best subsets, Mallow’s $C_p$

[R
code](http://stats191.stanford.edu/selection.html#election-example-best-subset)

### Model selection

Search strategies

-   Given a criterion, we now have to decide how we are going to search
    through all possible models.

-   “Best subset”: search all possible models and take the one with
    highest $R^2_a$ or lowest $C_p$ leaps

-   Stepwise (forward, backward or both): useful when the number of
    predictors is large. Choose an initial model and be “greedy”.

-   “Greedy” means always take the biggest jump (up or down) in your
    selected criterion.

### Model selection

Implementations in

-   “Best subset”: use the function leaps. Works only for multiple
    linear regression models.

-   Stepwise: use the function step. Works for any model with Akaike
    Information Criterion (AIC). In multiple linear regression, AIC is
    (almost) a linear function of $C_p$.

### Model selection

Akaike / Bayes Information Criterion

-   Akaike (AIC) defined as
    $$AIC({\cal M}) = - 2 \log L({\cal M}) + 2 p({\cal M})$$ where
    $L({\cal M})$ is the maximized likelihood of the model.

-   Bayes (BIC) defined as
    $$BIC({\cal M}) = - 2 \log L({\cal M}) + \log n \cdot p({\cal M})$$

-   Strategy can be used for whenever we have a likelihood, so this
    generalizes to many statistical models.

### Model selection

Akaike / Bayes Information Criterion

-   In linear regression with unknown $\sigma^2$
    $$-2 \log L({\cal M}) = n \log(2\pi \widehat{\sigma}^2_{MLE}) + n$$
    where
    $$\widehat{\sigma}^2_{MLE} = \frac{1}{n} SSE(\widehat{\beta})$$

-   In linear regression with known $\sigma^2$
    $$-2 \log L({\cal M}) = n \log(2\pi \sigma^2) + \frac{1}{\sigma^2} SSE(\widehat{\beta})$$
    so AIC is very much like Mallow’s $C_p$.

### Model selection

Akaike / Bayes Information Criterion

-   BIC will always choose a model as small or smaller than AIC.

-   As our sample size grows, we can show that

    -   AIC will (asymptotically) always choose a model that contains
        the true model, i.e. it won’t leave any variables out.

    -   BIC will (asymptotically) choose exactly the right model.

### Cross-validation

$K$-fold cross-validation

-   Fix a model ${\cal M}$. Break data set into $K$ approximately equal
    sized groups $(G_1, \dots, G_K)$.

-   for (i in 1:K)

    Use all groups except $G_i$ to fit model, predict outcome in group
    $G_i$ based on this model
    $\widehat{Y}_{j,{\cal M}, G_i}, j \in G_i$.

-   Estimate
    $$CV({\cal M}) = \frac{1}{n}\sum_{i=1}^K \sum_{j \in G_i} (Y_j - \widehat{Y}_{j,{\cal M},G_i})^2.$$

### Cross-validation

Some facts about cross-validation.

-   It is a general principle that can be used in other situations to
    “choose parameters.”

-   Pros (partial list): “objective” measure of a model.

-   Cons (partial list): inference is, strictly speaking, “out the
    window” (also true for other model selection procedures).

-   If goal is not really inference about certain specific parameters,
    it is a reasonable way to compare models.

### $C_p$ versus 5-fold cross-validation

[R
code](http://stats191.stanford.edu/selection.html#election-example-best-subset)

### 5-fold cross-validation for all $C_p$ models

[R
code](http://stats191.stanford.edu/selection.html#election-example-best-subset)

### Model selection

Caveats

-   Many other “criteria” have been proposed.

-   Some work well for some types of data, others for different data.

-   Check diagnostics!

-   These criteria (except cross-validation) are not “direct measures”
    of predictive power, though Mallow’s $C_p$ is a step in this
    direction.

-   $C_p$ measures the quality of a model based on both *bias* and
    *variance* of the model. Why is this important?

-   *Bias-variance*

    tradeoff is ubiquitous in statistics.

### Bias-variance tradeoff

Comparing estimators

-   When an estimator $\widehat{\beta}_1$ of $\beta_1$ is unbiased:
    $$E((\widehat{\beta}_1 - \beta_1)^2) = \text{Var}(\widehat{\beta}_1)$$
    so it makes sense to compare unbiased estimators in terms of
    variance.

-   Even for biased estimators, the LHS makes sense, called the *mean
    squared error* of $\widehat{\beta}_1$ $$\begin{aligned}
       MSE(\widehat{\beta}_1) &= E((\widehat{\beta}_1 - \beta_1)^2) \\
       &= \text{Var}(\widehat{\beta}_1) + \text{Bias}(\widehat{\beta}_1)^2
       \end{aligned}$$

-   Paradoxically, it is sometimes possible to reduce $MSE$ by *biasing*
    the estimator.

### Bias-variance tradeoff

Shrinking toward zero

-   Suppose we observe $$Y_i \sim N(\mu_i, 1), 1 \leq i \leq n$$ and our
    goal is to estimate the entire vector $\mu$.

-   Minimum variance unbiased estimator is
    $$\widehat{\mu}_i = Y_i, \qquad 1 \leq i \leq n.$$

### Bias-variance tradeoff

Shrinking toward zero

-   How good an estimator is $\widehat{\mu}$?
    $$MSE(\widehat{\mu}, \mu) = \frac{1}{n} E(\sum_{i=1}^n (\widehat{\mu}_i -\mu_i)^2)  = 1.$$

-   *However*

    , we can improve on the MSE very simply by *shrinking*
    $\widehat{\mu}$ toward 0.

-   Define
    $$\widehat{\mu}^{\alpha}_i = \alpha \cdot Y_i, \qquad 1 \leq i \leq n, 0 \leq \alpha \leq 1.$$

### Shrinking an estimator

[R
code](http://stats191.stanford.edu/selection.html#bias-variance-tradeoff)
