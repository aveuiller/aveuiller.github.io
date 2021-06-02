Title: About design patterns: Dependency Injection
Slug: about_design_patterns-dependency_injection
Date: 2020-01-05
Category: Software Engineering
Tags: Design Patterns, Best Practice, Software Architecture
Author: Antoine Veuiller
Summary: A walk through dependency injection
-----

### Availability Disclaimer

This article can be found on other sources:

 - Medium: [link](https://medium.com/@aveuiller/about-design-patterns-dependency-injection-ab9c1742d4aa)

-----

![credit photo: [Bamboo Complexity, taufuuu](https://www.flickr.com/photos/ghailon/13082228923/)](/images/posts/2020-01-05_About-design-patterns--Dependency-Injection/bamboo_complexity.jpeg)

### What is dependency injection?

_Dependency injection_ (DI) is a very simple concept that aims to decouple components of your software and ease their integration and testing. It does so by asking for their sub-components instead of creating them.

During this article, we will also mention _inversion of control_ (IoC), which is commonly used along with dependency injection. This pattern aims to avoid asking for implementations but rather interfaces while injecting dependencies.

This article will use a simple example in Java to present dependency injection but aims towards a technology-agnostic explanation of the concept and its advantages. Moreover, even if it is an object-oriented design pattern, you can still adapt the behaviour in many programming languages.

### Let’s clarify all this using an example!

We will present a weather service that shows an intelligible representation of the weather. In the current implementation, we rely solely on a thermometer.

#### Let’s start without dependency injection.

![Weather service without IoC](https://raw.githubusercontent.com/aveuiller/design-tutorials/master/dependencyinjection/specs/classes_without_ioc.svg)

As you can see on the diagram, the _WeatherService_ is relying on a _Thermometer_, which can be configured with a _TemperatureUnit_. 
Not using dependency injection will result in a code creating a new instance of _Thermometer_ in the service, and a _Thermometer_ configuring the _TemperatureUnit_ to use:

````java
public class Thermometer {
  private final TemperatureUnit unit;
  
  public Thermometer() {
    this.unit = TemperatureUnit.CELSIUS;
  }
}

public class WeatherService implements WeatherContract {

  private final Thermometer thermometer;
 
  // This constructor is not using dependency injection
  public WeatherService() {
    this.thermometer = new Thermometer();
  }
}
````
Now let’s imagine that we want to use a _Thermometer_ configured to use Fahrenheit degrees instead of Celsius. For this, we add a parameter to switch between both units.

````java
public Thermometer(boolean useCelsius) {
  if (useCelsius) {
    this.unit = TemperatureUnit.CELSIUS;
  } else {
    this.unit = TemperatureUnit.FAHRENHEIT;
  }
}
````

One can also argue that the user of our program won’t always have access to an actual thermometer on their device, thus you may want to be able to fall back to another implementation in this case. 
For instance, an API sending the current temperature in your area. Integrating multiple implementations inside the service could be done as shown below.

````java
public WeatherService(boolean useRealDevice, 
                      boolean useCelsius,
                      String apiKey) {
  if (useRealDevice) {
    this.thermometer = new Thermometer(useCelsius);
  } else {
    this.thermometer = new ThermometerWebService(useCelsius, apiKey);
  }
}
````

As a result, initializing the service can be done as follows:

````java
public static void main(String[] args) {
  // Not using dependency injection
  WeatherContract weather = new WeatherService(true, true, null);
}
````

Even if it is easy to use, our current version of the _WeatherService_ is not evolutive. If we take a closer look at its constructor, we can see multiple design flaws that will haunt us in the long run:

*   The constructor is choosing its _Thermometer_. Adding a new type of Thermometer would require some parameter tricks to guess the implementation to use.
*   The constructor is managing the _Thermometer_ constructor parameters. Adding the _ThermometerWebService_ forced us to add a new _apiKey_ parameter to it, even if unrelated to the _WeatherService_.

As a result, any change to any _Thermometer_ implementation may require changes on the _WeatherService_ constructors. This behaviour is unwanted and breaks the _Separation of Concerns_ principle.

#### Will dependency injection improve my project?

Dependency injection, associated with inversion of control, is a good way to cover this use case. It allows you to choose which kind of thermometer you want in your program depending on the situation. The following diagram gives a quick overview of our new architecture:

![Weather service using IoC](https://raw.githubusercontent.com/aveuiller/design-tutorials/master/dependencyinjection/specs/classes_using_ioc.svg)

The **inversion of control** is represented in this diagram by the fact that our _WeatherService_ implementation is linked to _ThermometerContract_ rather than any of its implementations. That’s nothing more than this.

As for **dependency injection**, _WeatherService_ will now take a _ThermometerContract_ in its constructor, requiring the block using the service to build an instance filling this contract:

````java
public class WeatherService implements WeatherContract {
  // We now use the Interface   
  private final ThermometerContract thermometer;

  // New constructor using dependency injection    
  public WeatherService(ThermometerContract thermometer) {
    this.thermometer = thermometer;
  }
}
````

As a result, the initialization of a _WeatherService_ for both constructors will look like the following:

````java
public static void main(String[] args) {
  // Using dependency injection
  TemperatureUnit celsius = TemperatureUnit.CELSIUS;
  ThermometerContract thermometer = new Thermometer(celsius);
  WeatherContract weather = new WeatherService(thermometer);
}
````

Now, our _ThermometerContract_ can be fully configured by an external part of the software. More important so, the _WeatherService_ doesn’t need to know any of the available implementations of _ThermometerContract_, thus decoupling your software packages.

This could seem like nothing important, but this simple switch of responsibility is critical leverage for multiple aspects of software design. It enables you to control the instance creation from your software entry point by chaining dependencies. You won’t have to take care of the instantiation until it is necessary. This behaviour could be compared to raised exceptions, that are ignored until taken care of in a significant context.

### That’s all there is to dependency injection?

It is important to know that even if you can find libraries that help you manage your dependency injection, it is not always necessary to use them.

Those libraries tend to cover a lot of cases thus be offputting to developers not comfortable with the pattern in the first place. In reality, they simply ease the instantiation of complex dependency trees and are not required at all.

The following section is an example of injecting our service using [Guice](https://github.com/google/guice/wiki), a dependency injection framework for Java made by Google. The concept is to reference bindings of every component you can inject in your program, so that the library can generate a class of any type, automatically.

Let’s consider that we have two implementations with the following constructors:

```java
public class WeatherService implements WeatherContract {
  private final ThermometerContract thermometer;

  @Inject
  public WeatherService(ThermometerContract thermometer) {
    this.thermometer = thermometer;
  }
}

public class Thermometer implements ThermometerContract {
  private final TemperatureUnit unit;
  
  @Inject
  public Thermometer(@Named(WeatherModule.TEMPERATURE_UNIT) 
                     TemperatureUnit unit) {
    this.unit = unit;
  }
}
```

The _injection module_ should be configured to bind all needed interfaces to a given implementation.
It should also be able to inject any object without a specific interface, such as the enumerate _TemperatureUnit_. 
The injection will then be bound to a specific name, “_temp\_unit”_ in this case.

````java
public class WeatherModule extends AbstractModule {
  public static final String TEMPERATURE_UNIT = "temp_unit";

  @Override
  protected void configure() {
    // Named input configuration bindings
    bind(TemperatureUnit.class)
      .annotatedWith(Names.named(TEMPERATURE_UNIT))
      .toInstance(TemperatureUnit.CELSIUS);
      
    // Interface - Implementation bindings
    bind(ThermometerContract.class).to(Thermometer.class);
    bind(WeatherContract.class).to(WeatherService.class);
  }
}
````

Ultimately, the module can be used as follow, here instantiating a _WeatherContract_.

```java
public static void main(String[] args) {
  // Creating the injection module configured above.
  Injector injector = Guice.createInjector(new WeatherModule());

  // We ask for the injection of a WeatherContract, 
  // which will create an instance of ThermometerContract
  // with the named TemperatureUnit under the hood.
  WeatherContract weather = injector.getInstance(WeatherContract.class);
}
```

Such modules usually provide a good power of customization to the injected elements, thus we can consider configuring the injection depending on the available implementations.

As a result, using a library is not required when integrating dependency injection. However, this could save a lot of time and cumbersome code in big projects.

### Show me some tests!

As a side effect of decoupling your code, the dependency injection pattern is a real asset to improve unit testability of each component. This section contains an example of unit tests for our _WeatherService_.

As said above, making _WeatherService_ asking for a _ThermometerContract_ enables us to use any implementation we want. Hence, we can send a _mock_ in the constructor, then control its behaviour from the outside.

```java
public void testTemperatureStatus() {
  ThermometerContract thermometer = Mockito.mock(ThermometerContract.class);
  Mockito.doReturn(TemperatureUnit.CELSIUS).when(thermometer).getUnit();
  WeatherContract weather = new WeatherService(thermometer);
  
  Mockito.doReturn(-50f).when(thermometer).getTemperature();
  assertEquals(
    TemperatureStatus.COLD,
    weather.getTemperatureStatus()
  );
  
  Mockito.doReturn(10f).when(thermometer).getTemperature();
  assertEquals(
    TemperatureStatus.MODERATE,
    weather.getTemperatureStatus()
  );
}
```

As you can see, we can then control our thermometer without a struggle from outside our tested class.

### Conclusion

_Dependency injection_ is a way of thinking your code architecture and can be simple to implement by yourself. In bigger projects, integrating a dependency injection framework can save you a lot of time in the long run.

_Dependency injection_ provides multiple non-negligible advantages such as:

*   _Code decoupling_: use the contracts and ignore implementation specificities.
*   _Enhanced testability_: Unit tests almost become a pleasure to write.
*   _Configurability_: you can more easily swap injected instances.

[You can find the full code example in my design tutorials repository on GitHub](https://github.com/aveuiller/design-tutorials)