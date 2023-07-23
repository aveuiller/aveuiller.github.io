---
Title: "Introduction to Flaky Tests by Example"
Slug: introduction_to_flaky_tests_by_example
Date: 2020-08-10
Category: Software Engineering
Tags: Testing, Best Practice
Author: Antoine Veuiller
Summary: "Some real world examples of flaky tests"
---

### Availability Disclaimer

This article can be found on other sources:

- Medium: [link](https://medium.com/@aveuiller/stories-of-flaky-test-encounters-in-the-wild-a152bf7151f5)

-----

![Flakiness effect](/images/posts/2020-08-10_Introduction-to-Flaky-Tests-by-Example/red_light.gif)

Tests are an essential part of software development as they give a ground truth about the code sanity. As developers, we reasonably expect our unit tests to give the same results if the source code does not change. It can happen, however, that the result of a unit test changes over multiple executions of a test suite without any change in the code. Such a test is named a flaky test.

A flaky test is not dangerous _per se_ but reduces the confidence a developer can give to his test suite, diminishing the benefits of the latter. It is thus recommended to eradicate such issue as soon as possible.

However, depending on the origin of the flakiness, one may find out only a few days, months or even years later that the tests are flaky.
It may be hard to dive back into those and find the root causes, [so usually, we tend to put those tests aside to make them less annoying or we rerun them until success](https://martinfowler.com/articles/nonDeterminism.html).

![Fingers crossed](/images/posts/2020-08-10_Introduction-to-Flaky-Tests-by-Example/fingers_crossed.gif)

As a real-world example of flaky tests and the logic behind their resolution. I will talk about two interesting cases I had the opportunity to fix during my career.

### Storytime!

During my career, I stumbled onto a couple of flaky tests issues. There are two instances that, in my opinion, are quite symptomatic of test flakiness, with quite different contexts.

The examples are voluntary adapted to a simpler context than the original ones to keep a short and focused article.

#### Story 1: 5 days a month isn’t a big deal

I entered a project where continuous integration was broken during the 5 first days of each month. 
I was told that this wasn’t a big deal since we don’t need to deploy this project at the beginning of a month.
The priority of fixing those tests was so low that it has remained like this for years before we took the time to tackle this issue.

```python
def add_data(input_datetime, data):
    # Store the data along with the input date
    # [...]

def retrieve_data(lower_date):
    # Retrieve all data from lower date to now 
    # [...]

def compute_stats():
    # Compute some statistics about stored data
    month = arrow.get().floor('month') 
    data = retrieve_data(month)
    return len(data)

def test_compute_stats():
    # Test method checking the behaviour of compute_stats
    now = arrow.get()
    
    add_data(now.shift(days=-5))
    add_data(now.shift(days=-1))
    stat = compute_stats()
    
    assert stat == 2, "We retrieve the two data input"
```
The faulty feature was computing statistics about the current month. As the developer creating the initial tests wanted to take all cases into consideration, he created a test that gave as input multiple dates relative to the current _datetime_.

Among those inputs, one was _5 days before the current date,_ and the test was always computing the statistics as if it was part of the same month. As a result, it led to the tests being faulty at the beginning of each month. We can then imagine that the flakiness was detected under one to three weeks after the feature development and from then on, ignored.

This test is time-dependent because _compute\_stats_ will call for the date of analysis itself. As a result, the computation will always be dependent on the current date. One way of fixing such issues would be to sandbox the execution of the tests in order to control the current date.

At first, we wanted to rely on [dependency injection](https://medium.com/swlh/about-design-patterns-dependency-injection-ab9c1742d4aa) and make _compute\_stats_ ask for a month to compute the statistics. This would create an easy way of sandboxing the execution and also potentially open the door to new features. However, in this project, this wasn’t trivial to implement because there was a lot of code dependent on this feature.

Another way of doing so would be to inject the value directly to the method. Python has a very good library to sandbox the tests when using the built-in _datetime_ objects: [freezegun](https://github.com/spulec/freezegun). Once again, and unfortunately for us, the project was using [arrow](https://github.com/crsmithdev/arrow) so this was not a possibility.

Fortunately, and thanks to some previously well-thought environment on the project, we had a central method to provide the current date, which was initially intended to prevent the use of a wrong timezone.

By mixing this method to the awesome [patch decorator](https://docs.python.org/3/library/unittest.mock.html#the-patchers) of python mock library (which is part of the standard _unittest_ library since 3.3), we solved the issue with a simple modification.

```python
def add_data(input_datetime, data):
    # Store the data along with the input date
    # [...]

def retrieve_data(lower_date):
    # Retrieve all data from lower date to now 
    # [...]

def compute_stats():
    # Compute some statistics about stored data
    month = arrow.get().floor('month') 
    data = retrieve_data(month)
    return len(data)

def test_compute_stats():
    # Test method checking the behaviour of compute_stats
    now = arrow.get()
    
    add_data(now.shift(days=-5))
    add_data(now.shift(days=-1))
    stat = compute_stats()
    
    assert stat == 2, "We retrieve the two data input"
```

By sandboxing the execution to a given point in time, we ensured the reproducibility of the build at any given time.

#### Story 2: We use that configuration!

In another project, while creating a new feature we happened to break tests unrelated to our changes. This case could have been tedious to pinpoint, fortunately, due to the project organization, we were certain that the new feature did not affect the code covered by the now failing tests.

The code below is a synthetic representation of what happened, a global _config_ object was interacting with both the existing and new features.

```python
# Global state configuration
config = {}

def existing_feature():
    if "common_entry" not in config:
        raise ValueError("Not configured")

    # Process [...]
    return True

def our_new_feature():
    if "common_entry" not in config:
        raise ValueError("Not configured")

    # Process [...]
    return True
```

From the isolation of the two features, we knew that the new tests had to be the ones creating a faulty global state. There were globally two possibilities for the faulty state.
Either the new test was injecting something new to the global state, or removing something essential to the existing test.

The test cases below were always run in the specific order _ConfiguredFeatureTest, ExistingFeatureTestCase_ before integrating the new feature, then in the order _ConfiguredFeatureTest, NewFeatureTestCase, ExistingFeatureTestCase._

```python
class ConfiguredFeatureTest(unittest.TestCase):
    def setUp(self):
        config["entry"] = "anything"

    def test_configured(self):
        self.assertIsNotNone(config.get("entry"))


class ExistingFeatureTestCase(unittest.TestCase):
    def test_feature_one(self):
        self.assertTrue(existing_feature())


class NewFeatureTestCase(unittest.TestCase):
    def setUp(self):
        config["entry"] = "anything"

    def tearDown(self):
        config.clear()

    def test_new_feature(self):
        self.assertTrue(our_new_feature())
```

In order to understand the behaviour of the existing test, we ran it alone, both with and without the new changes. It appeared that the test was failing in both cases. This gave us the information that this test was using an existing global state, and that we might be cleaning this state. So we took a deeper interest in the _tearDown_ method.

It happened that the global configuration was injected and cleared in our new test suite. This configuration was used but rarely cleared in other tests. As a result, the existing test was relying on the execution of the previous ones to succeed. Clearing the configuration removed the context required by the existing test, thus made it fail.

By “chance” the tests were always run in the right order for years. This situation could have been detected way earlier by using a random execution order for tests. [It happens that python has simple modules to do so](https://github.com/pytest-dev/pytest-randomly).

To fix the tests and avoid this situation to happen in the future, we decided to force the configuration clearing in the project’s test suite superclass. This meant to fix a bunch of other tests failing after this but also enforced a clean state for all new tests.

#### Bonus story: A good flakiness

On top of the previous stories, where flakiness is obviously a bad thing, I also stumbled into a case where I found flakiness somehow beneficial to the codebase.

In this particular case, the test intended to assert some data consistency for any instances of the same class. To do so, the test was generating numerous instances of the class with randomized inputs.

This test happened to fail during some executions as the inputs were creating a behaviour not accounted for by the feature. That enabled to extract a specific test case for the input and fix the behaviour in this case.

While I agree that edge cases should be analyzed during the development process, sometimes the input scope is too wide to consider all of them, let alone test all possibilities.

In those cases, randomizing the input of a method that should keep a consistent output is a good way to assert the codebase sanity in the long run.

### Conclusion

This article showed some real-life examples of flaky tests. They were not the worst to track down, but they pinpoint the fact that flakiness can resurface at any time, even years after their introduction!

Once they appear, the flaky tests need to be fixed as soon as possible out of fear that the failing test suite will be considered as a normal state. The developers may then not rely on the tests suites anymore.

Flakiness is mostly due to non-deterministic behaviour in the code, in this article we had an example of:

*   _Specific execution time_. If the code is dependent on time, there may be failing tests at specific dates.
*   _Randomness._ Using random values in the main code or in the tests needs extra care or the behaviour may vary depending on those random values.
*   _Modified global state._ Using a global state in a project can create inconsistencies in tests if the state is not managed correctly.

Some behaviour can help to limit the amount of flakiness that hides in the tests, such as:

*   _Control your test execution environment_ to keep reproducible execution.
*   _Avoid global states_ to minimize the side effects of environment settings.
*   _Randomize the test execution order_ to determine dependencies between tests.

#### Continue on the subject:

*   [https://hackernoon.com/flaky-tests-a-war-that-never-ends-9aa32fdef359](https://hackernoon.com/flaky-tests-a-war-that-never-ends-9aa32fdef359)
*   [https://martinfowler.com/articles/nonDeterminism.html](https://martinfowler.com/articles/nonDeterminism.html)
*   [https://docs.pytest.org/en/stable/flaky.html](https://docs.pytest.org/en/stable/flaky.html)

If you are curious about the context that led to the apparition of those flaky tests, my former manager [Kevin Deldycke](https://kevin.deldycke.com/) provides a more detailed view in a very interesting post: [_Billing Pipeline: A Critical Time Sensitive System_](https://kevin.deldycke.com/2020/10/billing-pipeline-critical-time-sensitive-system/).
