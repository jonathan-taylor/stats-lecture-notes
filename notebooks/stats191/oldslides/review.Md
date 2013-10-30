Outline

-   What is a regression model?

-   Descriptive statistics – numerical

-   Descriptive statistics – graphical

-   Inference about a population mean

-   Difference between two population means

What is course about?

-   It is a course on applied statistics.

-   Hands-on: we use [R](http://cran.r-project.org), an open-source
    statistics software environment.

-   We will start out with a review of introductory statistics to see R
    in action.

-   Main topic is “(linear) regression models”: these are the *bread and
    butter* of applied statistics.

What is a “regression” model?

A regression model is a model of the relationships between some
*covariates (predictors)* and an *outcome*. Specifically, regression is
a model of the *average* outcome *given* the covariates.

Heights of couples

-   To study height of the wife in a couple, based on the husband’s
    height and her parents height: Wife is the outcome, and the
    covariates are Husband, Mother, Father.

-   A mathematical model, using only Husband’s height:
    $${\tt Wife} = f({\tt Husband}) + \varepsilon$$ where $f$ gives the
    average height of the wife of a man of height Husband and
    $\varepsilon$ is “error”: not *every* man of height of Husband
    marries a woman of height $f({\tt Husband})$.

-   A statistical question: is there *any* relationship between
    covariates and outcomes – is $f$ just a constant?

-   Here is some [data](http://stats191.stanford.edu/review.html) using
    only Husband’s height.

### Heights data

[R code](http://stats191.stanford.edu/review.html)

### Heights data

Linear regression models

-   We might model the data as
    $${\tt Wife} = \beta_{0} + \beta_{1} {\tt Husband} + \varepsilon.$$

-   This model is *linear* in Husband, it is a *simple linear regression
    model*.

-   Another model:
    $${\tt Wife} = \beta_{0} + \beta_{1} {\tt Husband} + \beta_{2} {\tt Mother} + \beta_{3}
       {\tt Father} + \varepsilon.$$

-   Also linear (in Husband, Mother, Father).

-   Which model is better? We need a tool to compare models …

### Right-to-work example

[Data](http://www.ilr.cornell.edu/~hadi/RABE4/Data4/P005.txt)
description

-   Income: income for a four-person family

-   COL: cost of living for a four-person family

-   PD: Population density

-   URate: rate of unionization in 1978

-   Pop: Population

-   Taxes: Property taxes in 1972

-   RTWL: right-to-work indicator

### Right-to-work vs. cost of living

[R code](http://stats191.stanford.edu/review.html)

### Right-to-work vs. income

[R code](http://stats191.stanford.edu/review.html)

### Unionization vs. cost of living

[R code](http://stats191.stanford.edu/review.html)

### Unionization vs. income

[R code](http://stats191.stanford.edu/review.html)

### Unionization vs. income

[R code](http://stats191.stanford.edu/review.html)

### Unionization vs. population

[R code](http://stats191.stanford.edu/review.html)

### Cost-of-living vs. income

[R code](http://stats191.stanford.edu/review.html)

### Full dataset

[R code](http://stats191.stanford.edu/review.html)

### Without NYC

[R code](http://stats191.stanford.edu/review.html)

### Right-to-work example

Building a model

Some of the main goals of this course:

-   Build a statistical model describing the “effect of RTWL” on “COL”

-   This model should recognize that other variables also affect “COL”

-   What sort of “statistical confidence” do we have in our conclusion
    about “RTWL” and “COL”?

-   Is the model adequate do describe this dataset?

-   Are there other (simpler, more complicated) models?

### Descriptive statistics – numerical

Mean of a sample

Given a sample of numbers $X=(X_1, \dots, X_n)$ the sample mean,
$\overline{X}$ is $$\overline{X} = \frac1n \sum_{i=1}^n X_i.$$

Standard deviation of a sample

Given a sample of numbers $X=(X_1, \dots, X_n)$ the sample standard
deviation $S_X$ is
$$S^2_X = \frac{1}{n-1}  \sum_{i=1}^n (X_i-\overline{X})^2.$$

### Descriptive statistics – numerical

Median of a sample

Given a sample of numbers $X=(X_1, \dots, X_n)$ the sample median is the
“middle” of the sample: if $n$ is even, it is the average of the middle
two points. If $n$ is odd, it is the midpoint.

Quantiles of a sample

Given a sample of numbers $X=(X_1, \dots, X_n)$ the $q$-th quantile is a
point $x_q$ in the data such that $q \cdot 100\%$ of the data lie to the
left of $x_q$.

**Example:**

the $0.5$-quantile is the median: half of the data lie to the right of
the median.

### Histogram

[R code](http://stats191.stanford.edu/review.html)

### Inference about a population mean

A testing scenario

-   Suppose we want to determine the efficacy of a new drug on blood
    pressure.

-   Our study design is: we will treat a large patient population with
    the drug and measure their blood pressure before and after taking
    the drug.

-   One way to conclude that the drug is effective if the blood pressure
    has decreased. That is, if the average difference is negative.

### Testing hypotheses

Setting up the test

-   We could set this up as drawing from a box of *differences in blood
    pressure*.

-   The *null hypothesis*, $H_0$ is: “the average difference is greater
    than zero.”

-   The *alternative hypothesis*, $H_a$, is: “the average difference is
    less than zero.”

-   Sometimes, people will test the alternative, $H_a$: “the average
    difference is not zero” and $H_0$: “the average difference is zero.”

-   We test the null with observed data by estimating the average
    difference and converting to standardized units.

### Sample of blood pressures

Sample of 50

### Inference about a population mean

Testing whether mean is 0: two-sided

-   Suppose we want a two-sided test of whether $\mu=0$ based on a
    sample $X$, at level $\alpha$.

-   Compute
    $$T = \frac{\overline{X}}{S_X/\sqrt{n}} = \frac{-0.7}{2.7/\sqrt{50}}=-1.8$$

-   If $|T| > t_{n-1, 1-\alpha/2}$, then reject $H_0:\mu=0$.

-   Above, $t_{n-1, 1-\alpha/2}$ is the $1-\frac \alpha 2$ quantile of
    $t_{n-1}$ random variable, defined by
    $$\mathbb{P}(T_{n-1} \leq t_{n-1,1-\alpha/2}) = 1 - \frac\alpha 2.$$

-   With $df=49, \alpha=0.05$, we see that $t_{49,0.975}=2.00$. So, we
    do not reject $H_0$.

### Student’s $T$

Two-sided 5% rejection rule, df=49

### Inference about a population mean

Testing whether mean is $<$ 0: one-sided

-   Suppose we want a one-sided test of whether $\mu < 0$ based on a
    sample $X$, at level $\alpha$.

-   For this test, the *null* is $H_0:\mu \geq 0$ and the alternative is
    $H_a: \mu < 0$.

-   Compute
    $$T = \frac{\overline{X}}{S_X/\sqrt{n}} = \frac{-0.7}{2.7/\sqrt{50}}=-1.8$$

-   If $T < t_{n-1, \alpha}$, then reject $H_0:\mu=0$.

-   With $df=49, \alpha=0.05$, we see that $t_{49,0.05}=-1.68$. So, we
    reject $H_0$.

### Student’s $T$

One-sided 5% rejection rule for $H_0:\mu \geq 0$, df=49

### Student’s $T$

One-sided 5% rejection rule for $H_0:\mu \geq 0$, df=5

### Inference about a population mean

Confidence interval

-   If $(X_1, \dots, X_n)$ are independent, all having a normal
    distribution $N(\mu, \sigma^2)$, then a $(1 - \alpha)$-confidence
    interval for $\mu$ is
    $$\overline{ X} \pm t_{n-1, 1 - \alpha/2}\cdot S_X / \sqrt{n}$$

-   That is, if $\alpha=0.05$, and we repeat the experiment many times
    then 95% of the time, the true $\mu$ will be in the interval
    $$[\overline{ X} - t_{n-1, 1 - \alpha/2}\cdot S_X / \sqrt{n},\overline{ X} + t_{n-1, 1 - \alpha/2}\cdot S_X / \sqrt{n}]$$

-   Again, $t_{n-1, 1-\alpha/2}$ is the $1-\frac \alpha 2$ quantile of
    $t_{n-1}$ random variable, defined by
    $$\mathbb{P}(T_{n-1} \leq t_{n-1,1-\alpha/2}) = 1 - \frac\alpha 2.$$

### 20 different confidence 85% intervals

### Another 20

### Yet another 20

### Yes, 20 more

### A final 20

Out of 100, 90 covered the true mean...

### Review

Effect of calcium on BP

-   A study was conducted to study the effect of calcium supplements on
    blood pressure.

-   More detailed data description can be found
    [](http://lib.stat.cmu.edu/DASL/Datafiles/Calcium.html).

Questions

-   What is the mean decrease in BP in the treated group? placebo group?

-   What is the median decrease in BP in the treated group? placebo
    group?

-   What is the standard deviation of decrease in BP in the treated
    group? placebo group?

-   Is there a difference between the two groups? Did BP decrease more
    in the treated group?

### Boxplot

[R code](http://stats191.stanford.edu/review.html)

### Histogram of Treated response

[R code](http://stats191.stanford.edu/review.html)

### Histogram of Placebo response

[R code](http://stats191.stanford.edu/review.html)

### Difference between means

BP example

-   In our setting, we have two groups that we have reason to believe
    are different.

-   We have two samples:

    1.  $(X_1, \dots, X_{10})$ (Calcium)

    2.  $(Z_1, \dots, Z_{11})$ (Placebo)

-   Does treatment have an effect?

-   We can answer this statistically by testing the null hypothesis
    $H_0:\mu_X = \mu_Z$?

### Difference between means

Testing $H_0:\mu_X=\mu_Z$

-   If variances are assumed equal, pooled $t$-test is appropriate
    $$T = \frac{\overline{X} - \overline{Z}}{S_P \sqrt{\frac{1}{10}
       + \frac{1}{11}}}, \qquad S^2_P = \frac{9 \cdot S^2_X + 10 \cdot S^2_Z}{19}.$$

-   For two-sided test at level $\alpha=0.05$, reject if
    $|T| > t_{19, 0.975}$.

-   Confidence interval: for example, a $90\%$ confidence interval for
    $\mu_X-\mu_Z$ is
    $$\overline{X}-\overline{Z} \pm S_P \sqrt{\frac{1}{10}
       + \frac{1}{11}} \cdot  t_{19,0.95}$$

### Difference between means

Pooled estimate $S_P$

-   The rule for the $SD$ of differences is
    $$SD(\overline{X}-\overline{Z}) = \sqrt{SD(\overline{X})^2+SD(\overline{Z})^2}.$$

-   By this rule, we might take our estimate to be
    $$\widehat{SD(\overline{X}-\overline{Z})} = \sqrt{\frac{S^2_X}{10} + \frac{S^2_Z}{11}}$$

-   But, the pooled estimate assumes
    $\mathbb{E}(S^2_X)=\mathbb{E}(S^2_Z)=\sigma^2$ and replaces the
    $S^2$’s above with $S^2_P$, a “better” estimate of $\sigma^2$ than
    either $S^2_X$ or $S^2_Z$.

### Difference between means

Pooled estimate $S_P$

-   Where do we get 19 degrees of freedom?

-   Well, the $X$ (Treatment) sample has $10-1=9$ degrees of freedom to
    estimate $\sigma^2$ while the $Z$ (Placebo) sample has $11-1=10$
    degrees of freedom.

-   The total degrees of freedom is $9+10=19$.

### Our first regression model

Unified dataset

-   Put two samples together:
    $$Y=(X_1,\dots, X_{10}, Z_1, \dots, Z_{11}).$$

-   Under the same assumptions as the pooled $t$-test: $$\begin{aligned}
       Y_i &\sim N(\mu_i, \sigma^2)\\
       \mu_i &=
       \begin{cases}
       \mu_X & 1 \leq i \leq 10 \\ \mu_Z & 11 \leq i \leq 21
       \end{cases}
       \end{aligned}$$

### Our first regression model

$t$-test as regression model

-   This is a (regression) model for the sample $Y$. The (qualitative)
    variable is called a “covariate” or “predictor”.

-   The decrease in BP is an outcome variable.

-   We assume that the relationship between treatment and average
    decrease in BP is simple: it depends only on which group a subject
    is in.

-   This relationship is “modelled” through the mean vector
    $\mu=(\mu_1, \dots, \mu_{21})$.


