### Multiple linear regression

Outline

-   Specifying the model.

-   Fitting the model: least squares.

-   Interpretation of the coefficients.

-   More on $F$-statistics.

-   Matrix approach to linear regression.

-   $T$-statistics revisited.

-   More $F$ statistics.

-   Tests involving more than one $\beta$.

### Job supervisor data: $n=30$

Description

   Variable  Description
  ---------- --------------------------------------
     $Y$     Overall supervisor job rating
    $X_1$    How well do they handle complaints
    $X_2$    Do they allow special priveleges
    $X_3$    Give opportunity to learn new things
    $X_4$    Raises based on performance
    $X_5$    Too critical of poor performance
    $X_6$    Good rate of advancement

### Job supervisor data

[R
code](http://stats191.stanford.edu/multiple.html#job-supervisor-example)

### Specifying the model

Multiple linear regression model

-   Rather than one predictor, we have $p=6$ predictors.

-   $$Y_i = \beta_0 + \beta_1 X_{i1} + \dots + \beta_p X_{ip} + \varepsilon_i$$

-   Errors $\varepsilon$ are assumed independent $N(0,\sigma^2)$, as in
    simple linear regression.

-   Coefficients are called (partial) regression coefficients because
    they “allow” for the effect of other variables.

### Geometry of Least Squares: Multiple Regression

### Fitting the model

Least squares

-   Just as in simple linear regression, model is fit by minimizing
    $$\begin{aligned}
       SSE(\beta_0, \dots, \beta_p) &= \sum_{i=1}^n(Y_i - (\beta_0 + \sum_{j=1}^p \beta_j X_{ij}))^2 \\
       &= \|Y - \widehat{Y}(\beta)\|^2
       \end{aligned}$$

-   Minimizers:
    $\widehat{\beta} = (\widehat{\beta}_0, \dots, \widehat{\beta}_p)$
    are the “least squares estimates”: are also normally distributed as
    in simple linear regression.

### Error component

Estimating $\sigma^2$

-   As in simple regression
    $$\widehat{\sigma}^2 = \frac{SSE}{n-p-1} \sim \sigma^2 \cdot \frac{\chi^2_{n-p-1}}{n-p-1}$$
    independent of $\widehat{\beta}$.

-   Why $\chi^2_{n-p-1}$? Typically, the degrees of freedom in the
    estimate of $\sigma^2$ is
    $n-\# \text{number of parameters in regression function}$.

### Interpretation of $\beta_j$’s

Supervisor example

-   Take $\beta_1$ for example. This is the amount the average job
    rating increases for one “unit” of “Handles complaints”, keeping
    everything else constant.

-   Units of “Handles complaints” are individual favorable responses, so
    on average for every extra person who rated the supervisor as good
    at handling complaints (other things being fixed), the average job
    rating increases by $\beta_1$.

-   We often phrase this as the effect of “Handles complaints” *allowing
    for* or *controlling for* the other variables.

### Interpretation of $\beta_j$’s

Why are they *partial* regression coefficients?

-   The term *partial* refers to the fact that the coefficient $\beta_j$
    represent the partial effect of $\pmb{X}_j$ on $\pmb{Y}$, i.e. after
    the effect of all other variables have been removed.

-   Specifically,
    $$Y_i - \sum_{l=1, l \neq j}^k X_{il} \beta_l = \beta_0 + \beta_j X_{ij} + \varepsilon_i.$$

-   Let $e_{i,(j)}$ be the residuals from regressing $\pmb{Y}$ onto all
    $\pmb{X}_{\cdot}$’s except $\pmb{X}_j$, and let $X_{i,(j)}$ be the
    residuals from regressing $\pmb{X}_j$ onto all $\pmb{X}_{\cdot}$’s
    except $\pmb{X}_j$, and let $X_{i,(j)}$.

-   If we regress $e_{i,(j)}$ against $X_{i,(j)}$, the coefficient is
    *exactly* the same as in the original model (see [R
    code](http://stats191.stanford.edu/multiple.html)).

### Goodness of fit for multiple regression

Sums of squares

$$\begin{aligned}
   SSE &= \sum_{i=1}^n(Y_i - \widehat{Y}_i)^2 \\
   SSR &= \sum_{i=1}^n(\overline{Y} - \widehat{Y}_i)^2 \\
   SST &= \sum_{i=1}^n(Y_i - \overline{Y})^2 \\
   R^2 &= \frac{SSR}{SST}
   \end{aligned}$$ $R^2$ is called the *multiple correlation
coefficient* of the model, or the *coefficient of multiple
determination*.

### Adjusted $R^2$

Compensating for more variables

-   As we add more and more variables to the model – even random ones,
    $R^2$ will increase to 1.

-   Adjusted $R^2$ tries to take this into account by replacing sums of
    squares by *mean squares*
    $$R^2_a = 1 - \frac{SSE/(n-p-1)}{SST/(n-1)} = 1 - \frac{MSE}{MST}.$$

### Goodness of fit test

Another $F$-test

-   As in simple linear regression, we measure the goodness of fit of
    the regression model by
    $$F = \frac{MSR}{MSE} = \frac{\|\overline{Y}\cdot \pmb{1} - \widehat{\pmb{Y}}\|^2/p}{\|Y - \widehat{\pmb{Y}}\|^2/(n-p-1)}.$$

-   Under $H_0:\beta_1 = \dots = \beta_p=0$, $$F \sim F_{p, n-p-1}$$ so
    reject $H_0$ at level $\alpha$ if $F > F_{p,n-p-1,1-\alpha}.$

### Geometry of Least Squares: Full Model

### Geometry of Least Squares: Reduced Model

### Geometry of Least Squares: Both Models

### Intuition behind the $F$ test

Measuring lengths

-   The $F$ statistic is a ratio of lengths of orthogonal vectors
    (divided by degrees of freedom).

-   We can prove that our model implies $$\begin{aligned}
       \mathbb{E}\left(MSR\right) &= \sigma^2 + \underbrace{\|\pmb{\mu} - \overline{\mu} \cdot \pmb{1}\|^2 / p}_{(*)} \\
       \mathbb{E}\left(MSE\right) &= \sigma^2 \\
       \mu_i &= \mathbb{E}(Y_i) = \beta_0 + X_{i1} \beta_1  + \dots +  X_{ip} \beta_p
       \end{aligned}$$ so $F$ should be not be too far from 1 if $H_0$
    is true, i.e. $(*)=0$.

-   If $F$ is large, it is evidence that $(*) \neq 0$, i.e. $H_0$ is
    false.

### $F$-test revisited

Example in more detail

-   *Full (bigger) model :*

    $$Y_i = \beta_0 + \beta_1 X_{i1} + \dots \beta_p X_{ip} + \varepsilon_i$$

-   *Reduced (smaller) model:*

    $$Y_i = \beta_0  + \varepsilon_i$$

-   The $F$-statistic has the form
    $$F=\frac{(SSE(R) - SSE(F)) / (df_R - df_F)}{SSE(F) / df_F}.$$

### Geometry of Least Squares: Goodness of Fit Test

### Geometry of Least Squares: Goodness of Fit Test

### Matrix formulation

Equivalent formulation

$${\pmb Y}_{n \times 1} = \pmb{X}_{n \times (p + 1)} \pmb{\beta}_{(p+1) \times 1} + \pmb{\varepsilon}_{n \times 1}$$

-   $\pmb{X}$ is called the *design matrix* of the model

-   $\pmb{\varepsilon} \sim N(0, \sigma^2 I_{n \times n})$ is
    multivariate normal

$SSE$ in matrix form

$$SSE(\beta) = (\pmb{Y} - \pmb{X} \pmb{\beta})'(\pmb{Y} - \pmb{X} \pmb{\beta})$$

### Matrix formulation

Design matrix

-   The design matrix is the $n \times (p+1)$ matrix with entries
    $$\pmb{X} =
       \begin{pmatrix}
       1 & X_{11} & X_{12} & \dots & X_{1,p} \\
       \vdots &   \vdots & \ddots & \vdots \\
       1 & X_{n1} & X_{n2} &\dots & X_{n,p} \\
       \end{pmatrix}$$

### Least squares solution

Solving for $\widehat{\beta}_{}$

-   Normal equations
    $$\frac{\partial}{\partial \beta_j} SSE \biggl|_{\widehat{\beta}_{}} = -2 \left(\pmb{Y} - \pmb{X} \widehat{\beta}_{} \right)^t \pmb{X}_j = 0, \qquad 0 \leq j \leq p.$$

-   Equivalent to $$\begin{aligned}
       (\pmb{Y} - \pmb{X}\pmb{\widehat{\beta}_{}})^t\pmb{X} &= 0 \\
       \pmb{\widehat{\beta}_{}} &= (\pmb{X}^t\pmb{X})^{-1}\pmb{X}^t\pmb{Y}
       \end{aligned}$$

-   Properties: $$ \~N(, ^2^ (^t^ )^-1^ ), $$

-   [R code](http://stats191.stanford.edu/multiple.html)

### Inference for multiple regression

Regression function at one point

-   One thing one might want to *learn* about the regression function in
    the supervisor example is something about the regression function at
    some fixed values of $\pmb{X}_{1}, \dots, \pmb{X}_{6}$, i.e. what
    can be said about

    $$\label{eq:comb}
       \beta_0 + 65 \cdot \beta_1  + 50 \cdot \beta_2  + 55 \cdot \beta_3 + 64 \cdot \beta_4 + 75 \cdot \beta_5 + 40 \cdot \beta_6   \tag{*}$$

    roughly the regression function at “typical” values of the
    predictors.

-   The expression is equivalent to
    $$\sum_{j=0}^6 a_j \beta_j, \qquad a=(1,65,50,55,64,75,40).$$

### Inference for $\sum_{j=0}^p a_j \beta_j$

Confidence interval for $\sum_{j=0}^p a_j \beta_j$

-   Suppose we want a $(1-\alpha)\cdot 100\%$ CI for
    $\sum_{j=0}^p a_j\beta_j$.

-   Just as in simple linear regression:

    $$\sum_{j=0}^p a_j \widehat{\beta}_j \pm t_{1-\alpha/2, n-p-1} \cdot SE\left(\sum_{j=0}^p a_j\widehat{\beta}_j\right).$$

### Inference for $\sum_{j=0}^p a_j \beta_j$

$T$-statistics revisited

-   Suppose we want to test $$H_0:\sum_{j=0}^p a_j\beta_j= h.$$ As in
    simple linear regression, it is based on
    $$T = \frac{\sum_{j=0}^p a_j \widehat{\beta}_j - h}{SE(\sum_{j=0}^p a_j \widehat{\beta}_j)}.$$

-   If $H_0$ is true, then $T \sim t_{n-p-1}$, so we reject $H_0$ at
    level $\alpha$ if $$\begin{aligned}
       |T| &\geq t_{1-\alpha/2,n-p-1}, \qquad \text{ OR} \\
       p-\text{value} &= {\tt 2*(1-pt(|T|, n-p-1))} \leq \alpha.
       \end{aligned}$$

### Inference for $\sum_{j=0}^p a_j \beta_j$

One-sided tests

-   Suppose, instead, we wanted to test the one-sided hypothesis
    $$H_0:\sum_{j=0}^p a_j\beta_j \leq  h, \  \text{vs.} \ H_a: \sum_{j=0}^p a_j\beta_j >  h$$

-   If $H_0$ is true, then $T$ is no longer exactly $t_{n-p-1}$ but
    $$\mathbb{P}\left(T > t_{1-\alpha, n-p-1}\right) \leq 1 - \alpha$$
    so we reject $H_0$ at level $\alpha$ if $$\begin{aligned}
       T &\geq t_{1-\alpha,n-p-1}, \qquad \text{ OR} \\
       p-\text{value} &= {\tt (1-pt(T, n-p-1))} \leq \alpha.
       \end{aligned}$$

### Inference for $\sum_{j=0}^p a_j \beta_j$

Standard error of $\sum_{j=0}^p a_j \widehat{\beta}_j$

-   Based on matrix approach to regression
    $$SE\left(\sum_{j=0}^p a_j\widehat{\beta}_j \right) = \sqrt{\widehat{\sigma}^2 a (X^TX)^{-1} a^T}.$$

-   Don’t worry too much about implementation – will do this for you in
    general, [R code](http://stats191.stanford.edu/multiple.html)

### Inference for $\sum_{j=0}^p a_j \beta_j$

Prediction interval

-   “Identical” to simple linear regression.

-   Prediction interval at $X_{1,new}, \dots, X_{p,new}$:
    $$\begin{aligned}
       \lefteqn{\widehat{\beta}_0 + \sum_{j=1}^p X_{j,new} \widehat{\beta}_j\pm t_{1-\alpha/2, n-p-1}} \\
       & \qquad \qquad  \times \ \sqrt{\widehat{\sigma}^2 + SE\left(\widehat{\beta}_0 + \sum_{j=1}^p X_{j,new}\widehat{\beta}_j\right)^2}.
       \end{aligned}$$

### Inference for multiple regression

Questions about many (combinations) of $\beta_j$’s

-   In multiple regression we can ask more complicated questions than in
    simple regression.

-   For instance, we could ask whether

    -   $X_2:$ Do they allow special priveleges

    -   $X_3:$ Give opportunity to learn new things

    explains little of the variability in the data, and might be dropped
    from the regression model.

-   These questions can be answered answered by $F$-statistics.

### Inference for more than one $\beta$

Dropping one or more variables

-   Suppose we wanted to test whether how the supervisor handles special
    priveleges, or allows employees to try new things explains a
    significant amount of the variability in the overall job rating.
    Formally, this is: $$ H~0~:~2~=~3~=0,     H~a~: $$

-   This test is again an $F$-test based on two models $$\begin{aligned}
       R: Y_i &= \beta_0 + \beta_1 X_{i1} + \beta_4 X_{i4} + \beta_5 X_{i5} + \beta_6 X_{i6} + \varepsilon_i \\
       F: Y_i &= \beta_0 + \sum_{j=1}^6 \beta_j X_{ij} + \varepsilon_i \\
       \end{aligned}$$

-   **Note:**

    The reduced model $R$ must be a special case of the full model $F$
    to use the $F$-test.

### Geometry of Least Squares: Full Model

### Geometry of Least Squares: Reduced Model

### Geometry of Least Squares: Both Models

### Inference for more than one $\beta$

$SSE$ of a model

-   In the graphic, a “model”, ${\cal M}$ is a subspace of
    $\mathbb{R}^n$ = column space of $\pmb{X}$.

-   Least squares fit = projection onto the subspace of ${\cal M}$,
    yielding predicted values $\widehat{Y}_{{\cal M}}$

-   Error sum of squares:
    $$SSE({\cal M}) = \|Y - \widehat{Y}_{{\cal M}}\|^2.$$

### Inference for more than one $\beta$

$F$-statistic for $H_0:\beta_2=\beta_3=0$

-   $$\begin{aligned}
       F &=\frac{\frac{SSE(R) - SSE(F)}{2}}{\frac{SSE(F)}{n-1-p}} \\
       & \sim F_{2, n-p-1}       \qquad   (\text{if $H_0$ is true})
       \end{aligned}$$

-   Reject $H_0$ at level $\alpha$ if $F > F_{1-\alpha, 2, n-1-p}$.

-   Here is an example [R
    code](http://stats191.stanford.edu/multiple.html).

### Inference for more than one $\beta$

Dropping an arbitrary subset

-   For an arbitrary model, suppose we want to test $$

    H~0~:&~i~1~~=…=~i~j~~=0\
    H~a~:&

    $$ for some subset $\{i_1, \dots, i_j\} \subset \{0, \dots, p\}$.

### Inference for more than one $\beta$

$F$-statistic for $H_0:\beta_{i_1}=\dots=\beta_{i_j}=0$

-   You guessed it: it is based on the two models: $$\begin{aligned}
       R: Y_i &= \sum_{l=0, l \not \in \{i_1, \dots, i_j\}}^p \beta_j X_{il} + \varepsilon_i \\
       F: Y_i &=  \sum_{j=0}^p \beta_j X_{il} + \varepsilon_i \\
       \end{aligned}$$ where $X_{i0}=1$ for all $i$.

### Inference for more than one $\beta$

$F$-statistic for $H_0:\beta_{i_1}=\dots=\beta_{i_j}=0$

-   $$

    F &=\
    & \~F~j,\\ n-p-1~ ()

    $$

-   Reject $H_0$ at level $\alpha$ if $F > F_{1-\alpha, j, n-1-p}$.

### Geometry of Least Squares: Full Model

### Geometry of Least Squares: Reduced Model

### Geometry of Least Squares: Both Models

### Inference for more than one $\beta$

General $F$-tests

-   Given two models $R \subset F$ (i.e. $R$ is a subspace of $F$), we
    can consider testing $$ H~0~: $$vs.$$ H~a~:
    .$$\item The test statistic is$$ F = $$

-   If $H_0$ is true, $F \sim F_{df_R-df_F, df_F}$ so we reject $H_0$ at
    level $\alpha$ if $F > F_{df_R-df_F, df_F, 1-\alpha}$.

### Constraints

Constraining $\beta_1=\beta_3$ (after deciding
$\beta_2=\beta_4=\beta_5=\beta_6=0$)

-   Full model:
    $$Y_i = \beta_0 + \beta_1 X_{i1}  + \beta_3 X_{i3} + \varepsilon_i$$

-   Reduced model: $$\begin{aligned}
       Y_i &= \beta_0 + \tilde{\beta}_1 X_{i1}  + \tilde{\beta}_1 X_{i3} + \varepsilon_i \\
       &= \beta_0 + \tilde{\beta}_1 (X_{i1}  + X_{i3}) + \varepsilon_i \\
       \end{aligned}$$

[R code](http://stats191.stanford.edu/multiple.html).

### Constraints

Constraining $\beta_1+\beta_3=1$ (after deciding
$\beta_2=\beta_4=\beta_5=\beta_6=0$)

-   Full model:
    $$Y_i = \beta_0 + \beta_1 X_{i1}  + \beta_3 X_{i3} + \varepsilon_i$$

-   Reduced model: $$\begin{aligned}
       Y_i &= \beta_0 + \tilde{\beta}_1 X_{i1}  + (1 - \tilde{\beta}_1) X_{i3} + \varepsilon_i \\
       Y_i - X_{i3} &= \beta_0 + \tilde{\beta}_1 (X_{i1}  - X_{i3}) + \varepsilon_i \\
       \end{aligned}$$

[R code](http://stats191.stanford.edu/multiple.html).

### Back to interpretation of $\beta_j$’s

Supervisor example

-   Earlier, we said that $\beta_1$ is the effect for “Handles
    complaints” controlling for the other variables.

-   Why? Let’s look at the $T$ for testing $H_0:\beta_1=0$:
    $$T = \frac{\widehat{\beta}_1}{SE(\widehat{\beta}_1)}$$

-   Under $H_0:\beta_1=0$, $T^2 \sim F_{1, n-p-1}$ and $F$ tests are
    “always” a comparison of two models.

-   The full model has all variables while the reduced model has
    $\beta_1=0$. Hence, both model include or *control for* the other
    variables.


