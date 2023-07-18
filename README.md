Orchard Experiments
=================

This repository contains the script to generate figures 1-4 in the [Orchard manuscript](https://biorxiv.org/). 

To get started, it's necessary to first clone the [Orchard Github repo](https://github.com/morrislab/orchard). Please follow the directions in the *README* to properly install Orchard.

We assume that the following environmental variable is set 

```
ORCH_DIR=/path/to/orchard
```

Next, clone this repository

```
cd $ORCH_DIR 
git clone https://github.com/ethanumn/orchard_experiments
```

If you'd like to generate any of the figures, use the following commands

```
num=1 # set this to the particular figure number (1,2,3,4)
figure_folder=$ORCH_DIR/orchard_experiments/figures/figure$num
unzip $figure_folder/data.zip -d $figure_folder
open $ORCH_DIR/orchard_experiments/figures/figure$num/instructions.txt
```

You can then use the commands in a figures *instructions.txt* file to reproduce the results for the figure.



We use (3) different metrics to evaluate bulk DNA cancer phylogeny reconstructions. 

### (1) *Perplexity*

Formally, we measure a reconstructed tree using the perplexity of cellular prevalence matrix $F$ fit to the tree $$t$$ under a binomial likelihood model. 

Let $D$ be the bulk DNA read count data, $t$ be a phylogenetic tree reconstructed by an algorithm, and $F$ be the cellular prevalence matrix fit to the tree $t$. We define the perplexity of a probability model

$$
PP(t) 
$$

$$
PP(t) = 2^{\epsilon}, \quad \epsilon = - \frac{1}{nm}p(D\big|t)
$$

where $p\left(D\big|t\right)$ is defined as the binomial likelihood of the VAF data $D$ given the cellular prevalence matrix $F$  fit to the tree $t$.

In some instances, we can compare the tree $t$ reconstructed by an algorithm to a baseline tree matrix $t^{(baseline)}$. For a simulated phylogenetic tree $t^{(sim)}$, we have a ground truth cellular prevalence matrix $F^{(true)}$ used to generate the simulated bulk DNA data. For real data that have an expert-derived clone or mutation tree $t^{(expert)}$, we can fit a *maximum a posteriori* cellular prevalence matrix $F^{(MAP)}$ to the tree. In this case, we can use the *perplexity ratio* $\frac{PP(t)}{PP\left(t^{(baseline)}\right)}$ to measure our reconstructed tree  in reference to the baseline. A perplexity ratio near zero means the tree $$t$$ reconstructed by an algorithm is much better than the baseline, a perplexity ratio of 1 means that the tree reconstructed by an algorithm is as good as the baseline tree, and a large perplexity ratio means the tree reconstructed by an algorithm fits the VAF data poorly. In practice, however, **we use the log perplexity ratio** 

$$
log_2\left(\frac{PP(t)}{PP\left(t^{(baseline)}\right)}\right) = \epsilon - \epsilon^{(baseline)}
$$

or in the case we do not have a baseline, we use the log perplexity

$$
log_2\left(PP(t)\right) = \epsilon
$$

In prior work, the *log perplexity ratio* has been called the *VAF reconstruction loss*.

### (2) Relationship reconstruction loss

The relationship reconstruction loss is used to measure how well the pairwise evolutionary relationships in a tree $t$ reconstructed by an algorithm match the pairwise evolutionary relationships in in the ground truth trees. **Please note** that the relationship reconstruction loss is generally not used for real bulk DNA data.

We denote the pairwise evolutionary relationship between node $u$ and node $v$ in the tree $t$ as $E_{uv}$. We can now define the following

$$
    \qquad\qquad p(E_{uv} = r|t_j) = 1 \quad \text{ iff } E_{uv} = r \text{ in tree } t
$$

$$
      p(E_{uv} = r|t_j) = 0 \quad \text{ otherwise.}
$$

where $r$ is a particular pairwise evolutionary relationship and $r \in (ancestral, descendant, branched)$.

Finally, we can compute the difference in the pairwise evolutionary relationships for the reconstructed tree $E_{uv}$ and the ground truth evolutionary relationships from the ground truth trees $\tilde{E}_{uv}$ using the Jensen Shannon divergence

$$
    \epsilon_{R}= \frac{2}{n(n+1)}\sum{JSD(E_{uv}|| \tilde{E}_{uv})}
$$

where $JSD$ is the [Jensen-Shannon Divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence).

### (3) Wall clock run time

We use the number of seconds that a method takes to complete it reconstruction(s) to compare run times between different algorithms. We generally report wall clock run time in seconds as a power of ten.
