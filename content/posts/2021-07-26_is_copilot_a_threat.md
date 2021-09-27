Title: Is GitHub Copilot a Threat to Developers? (Spoiler: It's Not)
Slug: is_copilot_a_threat
Date: 2021-07-26
Category: Around Computer Science
Tags: showerthoughs
Author: Antoine Veuiller
Summary: GitHub Copilot provides potentially scary possibilities but can be a fine addition to the developers' tools.
-----

### Availability Disclaimer

This article can be found on other sources:

- Hacker Noon: [link](https://hackernoon.com/will-github-copilot-replace-developers-spoiler-no-jh5r35fl)
- Medium: [link](https://medium.com/geekculture/towards-abstraction-of-computer-science-cc68e4c30654)
- Dev.to: [link](https://dev.to/aveuiller/is-github-copilot-a-threat-to-developers-spoiler-it-s-not-5ee1)

-----


![Illustration](/images/posts/2021-07-26_abstraction_computer_science/copilot.png)

Computer science provides more and more abstraction layers with time, to the point that we don’t really know what’s running underneath.

GitHub recently released [Copilot](https://copilot.github.com/) in technical preview.
Copilot is an AI-based assistant that will automatically generate code from the context of your application, with the aim of easing software development.

A question that arises with simplification and automation in computer science is generally _“will the developer still be needed?”_.
And every time it happened, the answer was _“yes”_.
Abstraction in computer science reduces the cost of entering the domain, thus attracts a larger population.
But it also usually creates opportunities with new technologies, practices, and more complex systems.

This short article aims to summarize the evolution of abstraction layers in computer science to help understand the impact that GitHub Copilot may have.

### A Bit of History

The example that seems the oldest and most sensible would be the [Turing Machine](https://en.wikipedia.org/wiki/Turing_machine).
It was created with the specific idea to break the cryptographic code [Enigma](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma),
but the concepts behind it are now considered as a [ground reference of algorithmic capabilities](https://en.wikipedia.org/wiki/Turing_completeness) for programming languages.

Since then, we created processors, able to take a random set of instructions and process them generically.
Those instructions were originally described using [machine code](https://en.wikipedia.org/wiki/Machine_code), which is hard to manipulate for a human.
This is why programming languages of higher abstraction appeared.

Generally speaking, we can describe the goal of a programming language as to _write human-readable specifications that can be converted into machine code._

### Evolution of Programming

Programming languages evolved from _low (abstraction) level_ languages to _higher levels_, each iteration adding automation and helpers to the common operations.
Those abstractions can take many forms, from [garbage collection](https://en.wikipedia.org/wiki/Garbage_collection_%28computer_science%29) to libraries
[reading CSV files](https://docs.python.org/3/library/csv.html?highlight=read#examples).

These evolutions enable developers to add more complexity to their software, as there is less complexity on the technical parts.
They can in turn abstract away even more for others. Thanks to this, taking on programming is becoming easier with time.
We even see some programming languages using almost natural languages (e.g. [Gherkin](https://docs.behat.org/en/v2.5/guides/1.gherkin.html))
and requiring next to zero computer science knowledge to write.

This does not mean that people will stop using languages with lower abstraction levels.
On the contrary, even if they are generally harder to master and more verbose, they can be way more flexible for some use cases,
memory management for instance.

We can also note the appearance of Machine Learning, creating dynamic processes over data that would have been tedious to analyse, either by hand or through specific code.
This enables writing potentially complex behaviours with a few lines of code in some cases. 
Even then, there is some [automation](https://cloud.google.com/automl) of it to the point where you only have to provide data to get working results.

That being said, having a minimum of knowledge on the layers underneath remains very important to really comprehend the code execution.
Otherwise, it would be difficult to adapt to issues that may, and will, arise.

### Evolution of Infrastructure

We talked about code, but the same kind of evolution happened on the servers too.
At first, companies were starting on personal computers until they could get a hold of some space in a datacenter, renting one or more _baremetal_ servers.
This was costly and required technical knowledge for both the installation and deployment processes.

The virtualization technology evolved to the point where you can now rent a _virtual machine_ hosted on a physical host anywhere through 
[cloud providers](https://www.redhat.com/en/topics/cloud-computing/what-are-cloud-providers). 
This tremendously reduces the costs and enhances accessibility, but still requires technical knowledge to administrate correctly the machine on top of the deployments pipelines.

Since more recently, the technology of _containerization_ is heavily used with powerful tools like [Docker](https://www.docker.com/) and 
[Kubernetes](https://aveuiller.medium.com/kubernetes-apprentice-cookbook-90d8c11ccfc3). 
Those tools can help you deploy applications on a VM without necessarily mastering the system underneath\*.
In the same fashion as machine learning, there are projects aiming to further [reduce the knowledge required](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)
to use such technologies.

On top of that, a new abstraction layer called _serverless_ is emerging.
This enables you to directly execute code on a remote container, without having to take care of the hosting problematics at all.
While this is currently mostly used for stateless operations, there are no doubts about the growth of use cases and tools around this ecosystem.

_\*Note: Those tools may be better used with knowledge on the underlying layer, but you can redirect your learning to a more practical proficiency._

### A Glimpse on The Future of Copilot

GitHub Copilot is a pretty interesting advancement in software engineering, even if not completely on point at the moment.
According to the FAQ, the system gets the generation right around 50% of the time, and it is recommended to stay wary of the generated code.

If we look a bit differently on GitHub Copilot, we can consider this as a new programming language.
The input of this language is the documentation and function name and those are [transpiled](https://en.wiktionary.org/wiki/transcompiler) into source code for another programming language.

The generation is today limited to methods but we can imagine that this will evolve to classes or even packages.
We can also imagine the generation becoming almost flawless for well-known use cases.

Even if everything is one day working on a larger scale and flawlessly, the generated code will still require developers to handle the direction it takes,
and connect the even bigger pictures altogether.

### Conclusion

In regard to what we just saw, it makes no doubt that GitHub Copilot will further abstract development and ease the creation of software.
This breakthrough has the power to move the development industry, as other abstraction layers did before.

Having said that, developers will probably never lack opportunities, as the scope of the projects will get bigger thanks to this new abstraction layer.
The day to day work done as a developer may change, but developers will still be required for a long time.

As a matter of comparison, we already saw system administration positions evolve to SRE, still working on providing reliable hardware, but on a scale never seen before.
In the same way, developers may evolve to something close, adapting to the new tools.

_Thanks to Sarra Habchi for the review_
