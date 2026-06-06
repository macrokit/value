# Related Work (paper-ready draft)

> Drop-in related-work / prior-art section for the preprint. Clean scholarship only — no product or strategy
> content. The organizing honesty: **every component of this theory exists in some field; the contribution is
> the unification, the substrate grounding, and the is/ought asymmetry.** This section states that explicitly
> and concedes each component to its source, so the novelty claim rests on the synthesis, not on pretending the
> parts are new.

## Expected utility and the marginal value of resource

The axiomatic treatment of preference originates with von Neumann and Morgenstern (1944) and Savage (1954),
yielding a utility unique up to positive affine transformation. The logarithmic form of our value measure
(doc 01) coincides with Bernoulli's (1738) resolution of the St. Petersburg paradox and with constant-relative
-risk-aversion utility at coefficient one; the empirical law of diminishing marginal value it encodes is
Weber–Fechner and Gossen. We do not claim the functional form as novel. Our departure is threefold: we
*derive* it from a scale-invariance axiom on a physical resource rather than positing it as psychology; we
ground it in a substrate (free energy) that supplies a unit and a cross-frame exchange rate, which expected
utility explicitly lacks (its utils are not interpersonally comparable); and we show the same form is forced a
*second* time by multiplicative compounding (Peters' ergodicity-economics argument, 2019), making the logarithm
over-determined rather than a modeling choice.

## Information rate, log-optimal growth, and portfolio theory

The closest prior art, and the one we are most careful to credit, is Kelly (1956), who identified the
exponential growth rate of wealth with an information rate, with the optimum achieved by betting proportional to
one's beliefs. Breiman (1961) established its asymptotic optimality, Thorp applied it, and Cover (1991)
developed universal portfolios. Our capacity theorem (doc 02) — `G* = D(q‖r)` and the side-information gain
`ΔG = I(X;Y)` — is a generalization of Kelly's result, and our fleet operating point (doc 04 §3) is a Kelly/
Cover portfolio over agents. We state this plainly: **doc 02 is generalized Kelly.** What we add is (i) the
reinterpretation of "wealth" as free energy, making the substrate physical rather than monetary; (ii) the
cross-frame price layer (doc 03), which is genuinely beyond a single-agent betting result; (iii) the dynamics
and alignment layer (doc 05); and (iv) the unifying claim that Kelly's theorem is the single-agent monetary
*special case* of a general law of value. Kelly proposed a betting strategy; we propose that the same
mathematics is the structure of value for any goal-directed agent.

The modern information-theoretic form of this duality is sharp and we credit it explicitly: Moffett & Eckford
(2021) show Kelly's optimum attains a rate–distortion bound with equality, and Hirono & Hidaka (2015) derive
Jarzynski-type equalities linking information to the full statistics of capital growth; on the control side,
Touchette & Lloyd (2000) bound a closed-loop controller's performance by the mutual information it acquires.
Our `ΔG ≤ I(X;Y)` shares this skeleton — value/growth-rate bounded by mutual information, achieved by
proportional play — and we do not claim that skeleton as new; the generalization is to an arbitrary
goal-directed value quantity on a physical substrate, not a betting payoff or a control objective. A separate
information-theoretic notion of intrinsic value, **empowerment** (Klyubin, Polani & Nehaniv, 2005; Salge &
Polani, 2013), defines an agent's value as the channel capacity from its actions to its future perceptions; it
measures controllability rather than value-generation rate and offers no Kelly-style achievability, so it is a
neighbor to — not an instance of — the capacity theorem.

## Reinforcement learning

"Value function" is a central, precisely-defined object in reinforcement learning (Bellman, 1957; Sutton and
Barto): `V(s)` is expected cumulative reward under a policy. The nominal overlap is total but the relationship
is complementary, not competitive. RL takes the reward function as *given* and studies how to maximize it; our
goal-weights `k` are the analog of reward, but we problematize where reward comes from and how it drifts (doc
05, goal dynamics), and we identify a structural reason it cannot be read off the world (the is/ought asymmetry,
below). Our theory sits *beneath* RL — a candidate account of what reward *is*, not a method for optimizing a
given one.

## Thermodynamics of computation and the free-energy principle

That information has thermodynamic cost is established by Landauer (1961) and Bennett (1982); Jaynes (1957)
recast statistical mechanics as inference; England (2013) studied dissipation-driven adaptation. Most directly
relevant to our **Second Law of value** (doc 02) is the **thermodynamics of prediction** (Still, Sivak, Bell &
Crooks, 2012): they prove that a system's *model inefficiency* — information retained about the past that is
useless for predicting the future — is equal to its thermodynamic dissipation, `β⟨W_diss⟩ = I_mem − I_pred`,
holding arbitrarily far from equilibrium. This is the closest prior result to our identification of misalignment
with dissipated value, and we credit it as such; the relative-entropy-as-free-energy identity underlying both
terms of our decomposition is itself standard (H. Qian, 2001; a generalized H-theorem). Our departure is the
specific two-divergence value form `G = D(q‖r) − D(q‖p)` — available potential minus dissipation — and its
reading as *realized value* for a goal-directed agent rather than dissipated work for a physical system: the
structural correspondence is real and conceded, the value-theoretic packaging is ours. Also central is Friston's
free-energy principle and active inference (2010), which casts agents as minimizers of variational free energy
(surprise). Our belief dynamics (doc 05 §1) is free-energy-principle-like, and we adopt the
information-geometric machinery (the Fisher–Rao metric; Čencov, 1982; Amari's natural gradient) that the FEP
also uses. The distinction is precise and, we argue, illuminating: the free-energy principle is a theory of the
*perception/belief* half — the "is" — whereas our value layer (`k`, its measure, the capacity theorem) is the
*goal/value* half — the "ought" — together with a multi-agent price economics the FEP does not contain. The
seam between the two frameworks is exactly the is/ought asymmetry of doc 05 §0.

## General equilibrium, social choice, and mechanism design

Our cross-frame price layer (doc 03) is general-equilibrium theory (Arrow and Debreu, 1954; Debreu, 1959) and
its negative companion, the impossibility of canonical interpersonal comparison (Arrow, 1951). We use these
results rather than extend them: we *concede* that cardinal cross-agent value comparison is impossible and route
around it via an emergent price, precisely as Arrow–Debreu economies coordinate non-comparable utilities — and, as Hayek
(1945) argued, the price itself is the information-bearing signal that makes decentralized coordination of
dispersed knowledge possible, a reading our information-theoretic substrate makes literal. The
contribution is the synthesis — fusing the general-equilibrium price layer with the information-theoretic value
layer under a single physical substrate — and the application to populations of artificial agents, not new
equilibrium theorems.

## AI alignment and multi-agent systems

The tendency of capable agents to acquire resources and preserve their goals (instrumental convergence) was
articulated by Omohundro (2008) and Bostrom (2014). We *derive* this tendency from the compounding dynamics of
value (doc 05 §3): goal-directions correlated with resource capture are selected regardless of terminal
content. We further recast alignment as a *dynamical stability condition* rather than a static property
(doc 05 §4, formalized in [`07-alignment-stability.md`](07-alignment-stability.md)), which to our knowledge is a
new framing.

## Statement of contribution

In descending order of defensibility, this work contributes: (1) the **is/ought asymmetry** as a structural
property of agent dynamics — beliefs have a target the world supplies, goals do not — which we argue is the
mathematical shape of the alignment problem; (2) a **unification** under one substrate-grounded quantity of
otherwise-separate accounts of value (expected utility, log-optimal growth, reinforcement value, thermodynamic
free energy, and general-equilibrium price); (3) the **substrate grounding** of value in free energy, supplying
a unit and a cross-frame exchange rate; and (4) the **fleet-governance** results — the world-entropy ceiling on
collective value throughput and the price-mediated coordination of non-comparable agents. We claim none of the
underlying mechanisms as individually new; the claim is that they are facets of one quantity, and that seeing
them so yields results (the capacity theorem, the fleet ceiling, alignment-as-stability) that the separate
treatments do not.

## References (to be formatted for the venue)

Arrow (1951) *Social Choice and Individual Values*; Arrow & Debreu (1954) *Econometrica*; Bellman (1957)
*Dynamic Programming*; Bennett (1982) *Int. J. Theor. Phys.*; Bernoulli (1738) *Comm. Acad. Sci. Petrop.*;
Bostrom (2014) *Superintelligence*; Breiman (1961) *Proc. 4th Berkeley Symp.*; Čencov (1982) *Statistical
Decision Rules*; Cover & Thomas, *Elements of Information Theory*; Cover (1991) *Math. Finance* (universal
portfolios); Debreu (1959) *Theory of Value*; England (2013) *J. Chem. Phys.*; Friston (2010) *Nat. Rev.
Neurosci.*; Hayek (1945) *Am. Econ. Rev.* (The Use of Knowledge in Society); Hirono & Hidaka (2015) *J. Stat.
Phys.*; Jaynes (1957) *Phys. Rev.*; Kelly (1956) *Bell Syst. Tech. J.*; Klyubin, Polani & Nehaniv (2005) *IEEE
CEC* (empowerment); Landauer (1961) *IBM J. Res. Dev.*; Moffett & Eckford (2021/2025) *IEEE Trans. Inf. Theory*
(Kelly bets and single-letter codes); von Neumann & Morgenstern (1944) *Theory of Games and Economic Behavior*;
Omohundro (2008) *Proc. AGI*; Peters (2019) *Nat. Phys.*; Qian, H. (2001) *Phys. Rev. E* (relative entropy as
free energy); Salge & Polani (2013) (empowerment — an introduction); Savage (1954) *Foundations of Statistics*;
Shannon (1948) *Bell Syst. Tech. J.*; Still, Sivak, Bell & Crooks (2012) *Phys. Rev. Lett.* (thermodynamics of
prediction); Sutton & Barto, *Reinforcement Learning*; Touchette & Lloyd (2000) *Phys. Rev. Lett.*
(information-theoretic limits of control).
