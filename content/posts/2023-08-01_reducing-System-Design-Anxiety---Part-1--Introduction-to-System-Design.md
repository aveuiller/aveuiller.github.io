---
Title: "Reducing Software Design Anxiety — Part 1: Introduction to System Design"
Slug: reducing-Software-Design-Anxiety-Part-1-Introduction-to-System-Design
Date: 2023-08-01
Author: Antoine Veuiller
Category: Software Engineering
Tags: TODO
Summary: "TODO"
---

---

![](https://cdn-images-1.medium.com/max/800/1*OwofP5Q14C6hxzSCcsPbbg.jpeg)[Designed by pch.vector / Freepik](https://fr.freepik.com/vecteurs-libre/minuscules-personnes-testant-assurance-qualite-dans-logiciel-isole-illustration-vectorielle-plane-personnage-dessin-anime-fixant-bogues-dans-peripherique-materiel-test-application-concept-service-informatique_10613736.htm#page=1&query=software%20system&position=1)

When developing a new idea, being for a personal project, creating a startup, or even implementing a new feature within an existing project, we want to go as fast as possible to production and start gathering feedback. While this is a good idea, going to production without a plan could be harmful as the [first interaction with your application is critical](https://www.nngroup.com/articles/first-impressions-human-automaticity/). Users will probably not come back if they find your application or website badly designed, laggy, or even unresponsive.

To avoid the aforementioned issue, you need to design your software carefully. Designing software systems is an important part of software engineering and is also very present in job interviews. This practice covers a lot of subjects, technical or not. For instance, you will have to take into account user experience, metrics, scalability, availability, responsiveness, and more. Thinking about everything at once may become anxiety-inducing.

To avoid getting stuck by the apparent complexity of system design, this series of articles proposes a thinking process and tradeoffs to consider. While many decisions should be taken pragmatically, there is a personal take on this kind of exercise. As a result, it’s normal and even better if you feel the need to inject your personal beliefs into the giveaway.

### Where to Start?

Fortunately, designing a software system is articulated around project management concepts that you can handle one by one:

1. First, you need to frame the project: highlight features that are critical, with a way to check if the goals defined by those features are well met.
2. Once framed, you will have to plan for the resources that your software will require to run correctly.
3. This resource consumption can help you determine the best software design to reduce issues in the long run.
4. With all this data, you will be able to make an informed decision about the technologies that fit best.

This series will be discussing distributed software systems as they are the most present nowadays and probably the most complex subjects to consider during the design. However, most of the concepts remain completely valid for non-distributed software systems, even for non-software projects! 

Furthermore, this process can be applied recursively inside each component of complex systems.

### You Do Not Need to Master Everything

Depending on the situation, you may have to only consider a subpart of these subjects, either alone or with a team. However, having at least some knowledge about the whole picture will help to make informed decisions.

For instance, if you are designing a system for a new startup, you will have to dig through every subject, and probably even deeper than where this guide will leave you. However, you may have time to reach out for constructive feedback and even brainstorm the design with other people.

On the other hand, during an interview, your time will be limited. As a result, interviewers usually cover a subpart of those subjects. It’s okay to not master every subject, but you need to be aware of the knowledge you are lacking. During an interview, it usually comes a long way to express what you would try to learn to get insights on a decision you can’t take on the spot.

### Conclusion

The original plan of this series is to provide articles articulated around a specific subject:

1. Introduction to System Design (this article)
2. Define Features, Contracts, and Metrics ([link](https://aveuiller.github.io/Reducing-System-Design-Anxiety-Part-2--Define-Features-Contracts-and-Metrics.html))
3. Showcase of Basic Architectures ([link](https://aveuiller.github.io/Reducing-System-Design-Anxiety-Part-3-Showcase-of-Basic-Architectures))
4. Effective Load Planning (_WIP_)
5. Choose the Communication Technologies (_WIP_)
6. Choose the Storage Technologies (_WIP_)
7. Choose the Hosting Technologies (_WIP_)

If you are ready to continue on the subject, let’s go to the second article to think about user experience and the project scope.
If you feel that you are comfortable enough with the thinking process and want more technical details, I can recommend the [system-design-primer](https://github.com/donnemartin/system-design-primer) repository by Donne Martin, which contains a lot of useful resources.
