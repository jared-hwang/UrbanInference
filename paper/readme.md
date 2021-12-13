---
author:
- |
  Samuel Griesemer\
  email\
  University of Southern California\
- |
  Jared Hwang\
  <jaredhwa@usc.edu>\
  University of Southern California
bibliography:
- references.bib
title: Applying simulation inference to city planning tools
---

::: {#Abstract}
## Abstract {#Abstract}
:::

The way cities are structured and designed can have a massive impact on
everything ranging from human health, to climate change, to societal
equity. Understanding the relationship between a city's features to
these qualities is paramount to designing cities according to our goals
as a society. Simulation-based inference is a method in which a
simulator is described by a joint distribution over some output of a
simulation and some latent variables, contitioned on some input. We
thereby can attempt to learn the relationship between the output and the
input parameters. We apply this technique to A/B Street, a traffic
simulation tool, by investigating the impact of an intersection's
structure on the average trip time in the wider area. We find that\....
We hope that these results show that simulation inference can be applied
on the wider urban planning field as a whole.

::: {#background}
## Background
:::

City and infrastructure design is only becoming more crucial as we as a
society become more cognizant of out impact on climate change, public
health, and racial and socio-economic equity. It is widely understood
that the structural design of our cities have a marked impact on our
wellbeing both individually and collectively, so it is therefore in our
best interest to design and propose policy that actively strives towards
\"better\" cities.

However, a major impedance of this goal is the number of conflating
factors and differing goals (politically and technically) when
considering optimal design. Each can have innumerable differences from
another: their geographic topology, climate, socio-economic and race
composition, historical features, and so on.

As a result, a deeper understanding of a city's design on its residents,
resource usage, and so on, is extremely desirable to motivate better
policy and design recommendations, but correspondingly can be difficult
to pin down.

To approach this problem, we attempt to apply an inference technique
developed by Papamakarios and Murray [@Cranmer30055] on A/B Street, a
road/city planning simulation [@Carlino], as a proof-of-concept
application of simulation inference on city planning simulations to
broadly learn the impacts of traffic and road design on the efficiency
and resource use of a city.

::: {#method}
## Method
:::

\[inference\]

\[ab street\]

A/B Street is a city and traffic simulator developed by Dustin Carlino,
built using the Open Street Map (OSM) format [@4653466]. It is widely
flexible and supports importing any map through OSM, changing lane type
(driving, bus, bike) and speed limits, traffic light timings, among
others. It also has built in visualization, data aggregation, and an API
through which we can control the simulation headlessly via Python code.
We chose A/B Street due to these factors, contributing to its ease of
using it as a black box for the simulation inference.

Street

GUI

output

We plan to write an inference package that runs and accepts output from
the A/B street simulations and understand the underlying posterior of
road structure on city and travel efficiency.

::: {#expected-results}
## Expected Results
:::

Using simulation inference, we hope to gain deeper insight on the design
of intersections and intra-city roads on overall travel time and
throughput, which may be counter-intuitive to what we may expect.

::: {#future-goals}
## Future Goals
:::

As stated above, we use A/B Street and road design as a preliminary
proof-of-concept on the application of simulation inference on city
design. However, there are many more ways we can utilize this technique
beyond just roads.

A burgeoning field is that of understanding city design on the emissions
produced by a city, and understanding how the block and road structure
impacts the city's contribution to climate change. Gim performed a
global study of land-use on a various city's emissions, for example,
congestion leading to longer trip times leading to greater emissions
[@doi:10.1080/15568318.2021.1901163]. By using a model and performing
inference on it, we can potentially understanding how to more granularly
change current cities or motivate future cities to reduce resource use
and CO$_2$ emissions.

Relatedly is the concept of urban heat islands--when the city itself is
warmer than the surrounding areas, resulting in greater air-pollution,
heat-related illnesses. Understanding how building material and block
structure impacts this could be of massive benefit. Gober et al.
explored this for Phoenix, Arizona, by modeling three different
scenarios based on gathered data [@doi:10.1080/01944360903433113]. We
could potentially use simulation inference on their model to more
fundamentally understand the land-use and heat island relationship.

Another area of interest is how policy changes can influence land-use in
certain areas, thereby influencing everything about the city
itself--from emissions to all the other qualities discussed above.
Landis investigated this using their California Urban Futures Model,
where they simulated the results of three different scenarios:
\"business as usual\", \"Maximum Environmental Protection\", and
\"Compact Cities\" [@doi:10.1080/01944369508975656]. By applying
inference on the model, perhaps we can obtain more optimal, fine grained
policy recommendations than just three scenarios would illuminate.

We've discussed several potential paths and application for this
research moving forward, however, there are many more that can and
should be investigated. Urban planning as a field is growing rapidly,
and in turn, applications of computational techniques in the urban
planning space are similarly growing. With the results we have presented
here, we hope to have shown that the application of computational
techniques developed for physics, math, and so on could have countless
uses in urban planning, and could serve to benefit society as a whole.

::: {#Author Contributions}
## Author Contributions {#Author Contributions}
:::

J.H. proposed the paths and topics that could benefit from applying
computational methods upon. S.G. proposed applying the inference
technique to city planning simulations and found the specific simulator
A/B Street. Both members discussed the potential areas of exploration
using A/B Street. S.G. wrote the inference wrapper upon A/B Street and
J.H. ran and enabled the software to run (via singularity container) on
the USC computing cluster.
