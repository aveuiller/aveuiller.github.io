---
Title: "A Generic Approach to Troubleshooting"
Slug: troubleshooting_generic_approach
Date: 2022-09-18
Category: Software Engineering
Tags: Best Practice, System Engineering
Author: Antoine Veuiller
Summary: "This article aims to provide a baseline of investigation in case of a generic production incident"
---

### Availability Disclaimer

This article can be found on other sources:

- Medium: [link](https://aveuiller.medium.com/a-generic-approach-to-troubleshooting-dda764fbbb6)
- Dev.to: [link](https://dev.to/aveuiller/a-generic-approach-to-troubleshooting-14jp)

-----

When working with a production system, you may encounter errors at any point, originating either from an application or its underlying host.
While it may become natural for a seasoned engineer to pinpoint its origin, it can be overwhelming at times if you are unsure of where to look.

This article aims to provide a generic framework to tackle production issues.
The framework will serve as a basis for any engineer aiming to learn about troubleshooting basics.
However, as with any generic framework, it may need adjustments for specific use cases.

## Environment

In this article, we consider that you are working on a project that already implements the [best practices in terms of monitoring](https://www.pagerduty.com/resources/learn/best-practices-for-monitoring/)
so that you have access to sensible metrics, defined for instance through the [USE Method](https://brendangregg.com/usemethod.html).
Those metrics can be used to provide performance dashboards and declare alerts triggered in case of faulty or suspicious behavior.
For a more visual reference, the following diagram shows a basic monitoring architecture using [Prometheus](https://prometheus.io/), [Grafana](https://grafana.com/), and [Alert Manager](https://prometheus.io/docs/alerting/latest/alertmanager/).

![Basic Monitoring Environment](/images/posts/2022-09-18_troubleshooting_basics/Monitoring_Environment.svg)

Upon the reception of an alert for an issue impacting a production service, the actions to take can be broken down into three steps: _Analysis_, _Correction_, and _Post-Mortem_.
As some of the traces found or produced during the incident can be transient, it is recommended to keep track of any event and action that was taken on the production during the analysis and correction phases.
This will ease the post-mortem phase.

## Analysis

### Explore The Issue

The first step when receiving an alert will be to find any known information about it.
Usually, a [_Runbook_](https://www.pagerduty.com/resources/learn/what-is-a-runbook/) will explain the reason why this alert fired and the steps to take to solve it.

Even if the solution seems simple, you may want to find the scope of the problem.
Your response might differ if the issue is impacting one or hundreds of hosts.
Likewise, an issue crippling production will require a low response time to issue corrective action,
while a less critical issue, like a decrease in performance, may give you more time for analysis.

While your production servers should behave in the same way,
in some cases you will need to investigate the error before being able to determine the actual number of impacted hosts.


### Check The Basic Metrics

If you have multiple hosts impacted, take one of them as an analysis host before you have a clear view of which metrics are important in the current case.
If you have the chance to have metrics exported to a dashboard, for instance through [node-exporter](https://github.com/prometheus/node_exporter),
you will be able to see the issue quite easily from the different indicators.
Otherwise, you will need to jump on the host and use the [usual tools](https://linuxconfig.org/linux-basic-health-check-commands) to get more insights into the host's health.
In any case, you will be looking for issues with the CPU, RAM, Load, Disk, and Network.

This first step will indicate if the issue is purely applicative, or if your server is over-used to some extent.
This will also help you reduce the scope of where to look further down the investigation.

Regardless of the result of the previous check, you will need to look at the application-specific metrics,
both for performance through CPU and RAM usage, as well as applicative metrics such as response time, workload queues, and more.
You also need to check the applicative logs looking for anything that stands out of the ordinary.

From there, if you have enough information to at least recognize the issue and perform a temporary corrective action,
you should go for it and fix the production as soon as possible before digging Further.

### Dive Deeper into The Application Metrics

If you didn't find the root cause of the error yet, you need to dig into the application behavior and its interaction with the system.
This step is mostly dependent on the application, but there are some common checks that could show irregularities.

On the system side, you can take a look at:

- The network communications and connectivity (e.g.
  [tcpdump](https://man7.org/linux/man-pages/man1/tcpdump.1.html),
  [netstat](https://man7.org/linux/man-pages/man8/netstat.8.html),
  [telnet](https://www.commandlinux.com/man-page/man1/telnet.1.html),
  [mtr](https://www.commandlinux.com/man-page/man8/mtr.8.html)).
- The Kernel and related logs (e.g.
  [journalctl](https://man7.org/linux/man-pages/man1/journalctl.1.html),
  [dmesg](https://man7.org/linux/man-pages/man1/dmesg.1.html), …)

On the applicative side, you can take a look at:

- The configuration through files and environment variables (e.g. [/proc](https://man7.org/linux/man-pages/man5/proc.5.html)).
- The opened file handles and connections (e.g. [lsof](https://man7.org/linux/man-pages/man8/lsof.8.html)).
- The system calls that are performed by the application (e.g. [strace](https://man7.org/linux/man-pages/man1/strace.1.html)).
- The application performances in a specific code path (e.g. [gdb](https://man7.org/linux/man-pages/man1/gdb.1.html), [pprof](https://github.com/google/pprof), …).

## Correction

### Protect The Production

It is important to protect production from the issue as soon as possible.
This can take many forms but usually, you will either implement a quick fix,
that will enable the instance to still run until a long-term solution is implemented,
or isolate the faulty application from the production pools.
The latter can be done for instance by redirecting the load-balancer flow to other instances.

With orchestration solutions and stateless services,
it could be appealing to simply restart the application and use a brand-new instance.
This may work in some cases, but be sure to backup all data required for further investigation before doing so,
otherwise, you may end up in the same situation later.

### Implement a Long-Term Solution

Once the production is secured, you can catch your breath and start digging further into the data you collected to find the actual root cause of the alert that was triggered.
Even if the situation is stable for now, you may want to improve the overall code quality so the _future you_ don't have to investigate this issue again.

This section is entirely specific to the encountered issue, the actual fix could range from host configuration or code update to a complete architectural refactor in some cases.
I would advise performing the long-term fix as soon as possible, but you may be compelled to write down the Post-Mortem beforehand if the fix is big or impacts multiple components.

## Post-Mortem

### Write The Actual Post-Mortem

The main point of a [Post-Mortem](https://sre.google/sre-book/postmortem-culture/) is to hold all relevant events and actions that took place during the incident.
This helps to understand the issue and improve the response process for future incidents.
It also helps fellow engineers to map potential side effects they experienced to the main incident.

On top of the precise timeline, you need to describe the actual root cause from which the incident originates and the action you and your team are proposing to avoid this issue from recurring.
In case of a corrective action impacting multiple components, you will need to have this post-mortem reviewed by the right stakeholders before taking action.
The post-mortem should hold enough information for a peer to have a strong opinion about the proposal.

### Improve Runbooks And Alerts

Depending on the corrective action you took, you may need to create new alerts to cover different edge cases and modify the runbook sections with up-to-date data.

Even if the changes you performed are trivial, use this step as a feedback loop on the data you were missing during the investigation to help the _future you_ during the next investigation.

## Conclusion

This article aims to provide a baseline of investigation in case of a generic production incident.
The procedure will not show you the error if you don't ask the right questions but defines a framework to help you find the right questions to ask, and where to write the answers.

As a picture is worth a thousand words, here is a summary of the article through a simple flow chart.

![Troubleshooting Operations Flowchart](/images/posts/2022-09-18_troubleshooting_basics/Generic_Troubleshooting_Guide.svg)

_Thanks to Sarra Habchi for the review_
