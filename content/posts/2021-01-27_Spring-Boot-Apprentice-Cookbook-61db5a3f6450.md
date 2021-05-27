Title: Spring Boot: Apprentice Cookbook
Slug: spring_boot_apprentice_cookbook
Date: 2021-01-27
Category: Software Engineering
Tags: Cheat sheet
Author: Antoine Veuiller
Summary: Spring Boot cheat sheet to bootstrap an API
-----

### Availability Disclaimer

This article can be found on other sources:

- Medium: [link](https://medium.com/@aveuiller/spring-boot-apprentice-cookbook-61db5a3f6450)

-----

![Spring Boot logo](https://cdn-images-1.medium.com/max/800/1*gxXLMIuJDHCH7fwIgEP1cg.png)

[Spring Boot](https://spring.io/projects/spring-boot) is a web framework built on top of the framework [Spring](https://spring.io/projects/spring-framework). It is designed for easier use and quicker implementation. It does so by configuring the application and its environment as automatically as possible. As a newcomer, I can say that it makes the framework really easy to get into.

My learning led me to read most of the [reference documentation](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#using-boot-structuring-your-code), which is well written and gives you a lot of insights into the internal behavior of Spring Boot. This documentation gives a lot of details, so this article aims to take the counter approach and pinpoint the concepts you will need to implement an API using Spring Boot. I will complement each section with a set of links to related documentation, may you want to dig further.

As a side note, this document will be using version 2.4.2 of the framework, on a Java project using Gradle as the build system. 
However, the information remains applicable to any compatible language and build system.

This article will cover the following aspects of creating an API with Spring Boot:

*   Bootstrap the project
*   Create REST endpoints
*   Handle errors
*   Connect to a persistence layer
*   Paginate the results
*   Test the application
*   Package the Application

### Bootstrap the project

This part may be the easiest, as Spring Boot is providing a package generator at [https://start.spring.io/](https://start.spring.io/). We can select all required modules and retrieve an archived project with the build system, dependencies, and main application class.

Outside of this generator, to declare a RESTful API, our project should define the Spring Boot _starter web_ dependency. 
The _starter_ dependencies are a set of ready to use features packaged by Spring Boot.

```groovy
plugins {
  id 'org.springframework.boot' version '2.4.2'
}

dependencies {
  implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

The application’s main method should be contained in any class, on which we should apply the annotation `@SpringBootApplication`. This annotation is responsible for a lot of automatic configurations, namely the components injection and web server startup.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

Starting the server is as simple as using the embedded command `./gradlew bootRun`. 
The server will start, but we don’t have any endpoint to serve at the moment.

> Documentation links:

> [@SpringBootApplication](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#using-boot-using-springbootapplication-annotation)

> [List of starter dependencies](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#using-boot-starter)

### Create a REST endpoint

To create a controller, we simply have to annotate any class with `@RestController`.
We can then configure any method inside this controller as an endpoint using `@RequestMapping`.

`@RequestMapping` help us configuring the endpoint by providing an URL, the HTTP verb, the expected data type, and more. 
It can be applied both on a class and a method, the configurations applied on the class will be inherited by the methods underneath and the path concatenated.

To control our endpoint status codes we will return a`ResponseEntity`, holding both the response message and `HttpStatus`.

```java
@RestController
@RequestMapping(value = "/hello",
        consumes = MediaType.ALL_VALUE,
        produces = MediaType.APPLICATION_JSON_VALUE)
public class HelloWorldController {
    
    @RequestMapping(value = "/world", method = RequestMethod.GET)
    public ResponseEntity<Map<String, String>> index() {
        HashMap<String, String> output = new HashMap<>();
        output.put("message", "Hello World!");
        return new ResponseEntity<>(output, HttpStatus.OK);
    }
}
```

The `ResponseEntity` will be automatically transformed to an HTTP response, using the `HttpStatus` as response code and transforming the message to a JSON object.
On top of transforming _Maps_ to JSON objects, Spring Boot configure [Jackson](https://github.com/FasterXML/jackson) to map all `public` attributes or getters of any class to a JSON object.

```shell
$ curl -i "localhost:8080/hello/world"
HTTP/1.1 200
{"Hello":"World"}
```

> Documentation links:

> [@RestController and @RequestMapping](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#getting-started-first-application-annotations)

> [@RequestMapping API doc](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html)

> [Customize Json Serialization](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#howto-customize-the-jackson-objectmapper)

### Advanced endpoint configuration

Now that we have a controller, we may want to define dynamic HTTP endpoints. To do so, the main annotations to keep in mind are:

*   `@RequestBody` : Defines a body structure through a java Class.
*   `@PathVariable`: Defines a variable subpart of the endpoint URL.
*   `@RequestParam` : Defines a query parameter.

The controller below showcases the three annotations with two endpoints, each returning a custom “Hello World” depending on the query.

````java
@RestController
@RequestMapping(value = "/hello",
        consumes = MediaType.ALL_VALUE,
        produces = MediaType.APPLICATION_JSON_VALUE)
public class HelloWorldController {
    
    // The behavior is not representative of a typical POST request
    // and only here as a matter of example.
    @RequestMapping(value = "", method = RequestMethod.POST)
    public ResponseEntity<Map<String, String>> greetFromBody(@RequestBody HelloBody helloBody) {
        HashMap<String, String> output = new HashMap<>();
        output.put("message", "Hello " + helloBody.getName());
        return new ResponseEntity<>(output, HttpStatus.OK);
    }
        
    @RequestMapping(value = "/{name}", method = RequestMethod.GET)
    public ResponseEntity<Map<String, String>> greet(@PathVariable String name,
                                                     @RequestParam(required = false,
                                                                   defaultValue = "0") int amount_exclamation) {
        HashMap<String, String> output = new HashMap<>();
        StringBuilder b = new StringBuilder("Hello ");
        b.append(name);
        for (int i = 0; i < amount_exclamation; i++) {
            b.append("!");
        }
        output.put("message", b.toString());
        return new ResponseEntity<>(output, HttpStatus.OK);
    }
}

class HelloBody {
    String name;

    public HelloBody() {
        // Used by Jackson
    }

    public String getName() {
        return this.name;
    }
}
````

The endpoints defined above can be used as follows:

```shell
curl -i "localhost:8080/hello/jack?amount_exclamation=4"
HTTP/1.1 200
{"message":"Hello jack!!!!"}

# -d automatically creates a POST request.
$ curl -i "localhost:8080/hello" -d '{"name": "Bob"}' -H "Content-Type: application/json"
HTTP/1.1 200
{"message":"Hello Bob"}
```

> Documentation links:

> [@RequestBody](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-requestbody)

> [@PathVariable](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-requestmapping-uri-templates)

> [@RequestParam](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-requestparam)

### Handle errors

By default, Spring Boot will return the HTTP code 200 for any successful request, 404 if the endpoint is not registered, and 500 for any error. We already saw that using `ResponseEntity` enables us to override this behavior for successful requests, but we still need to handle error codes more finely.

To do so, we will define custom API exceptions that will be automatically transformed into HTTP codes. 
This transformation is done by a class extending `ResponseEntityExceptionHandler` and annotated with `@ControllerAdvice`. 
In this class, we can define methods to handle exceptions using the annotations `@ExceptionHandler` and `@ResponseStatus`.

```java
@ControllerAdvice
public class MyApplicationControllerAdvice extends ResponseEntityExceptionHandler {

    @ExceptionHandler(ApiException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public void handleBadRequest() {
    }

    @ExceptionHandler(NotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public void handleNotFound() {
    }
}

public class ApiException extends Exception {
}

public class NotFoundException extends ApiException {
}
```

After defining the `ControllerAdvice` in your project, any exception thrown by your controllers will be parsed and transformed to the bound `ResponseStatus`.

```java
@RestController
@RequestMapping(value = "/exception")
public class ExceptionController {
    
    @RequestMapping(value = "/404", method = RequestMethod.GET)
    public ResponseEntity<Map<String, String>> notFound() throws NotFoundException {
        throw new NotFoundException();
    }    
    
    @RequestMapping(value = "/400", method = RequestMethod.GET)
    public ResponseEntity<Map<String, String>> badRequest() throws ApiException {
        throw new ApiException();
    }

    @RequestMapping(value = "/500", method = RequestMethod.GET)
    public ResponseEntity<Map<String, String>> ise() throws Exception {
        throw new Exception();
    }
}
```

```shell
$ curl -i "localhost:8080/exception/500"
HTTP/1.1 500

$ curl -i "localhost:8080/exception/404"
HTTP/1.1 404

$ curl -i "localhost:8080/exception/400"
HTTP/1.1 400
```

Our exception handling is very simple and does not return any payload, but it is possible to implement exception parsing in the methods of `ResponseEntityExceptionHandler`.

> Documentation links:

> [ResponseEntityExceptionHandler](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-error-handling)

> [@ControllerAdvice](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-controller-advice)

> [@ExceptionHandler](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-exceptionhandler)

> [@ResponseStatus](https://docs.spring.io/spring-framework/docs/5.2.8.RELEASE/spring-framework-reference/web.html#mvc-ann-exceptionhandler-return-values)

### Connect to a persistence layer

#### Configuration

To use a database, we will need the _Java Persistence API_ (JPA) package and the implementation of any persistence layer.
The former will install interface APIs, while the latter will provide the implementations and drivers.

To pinpoint the minimal changes required to switch between two distinct databases, we will show the integration with both [PostgreSQL](https://www.postgresql.org/) and [H2](https://www.h2database.com/html/main.html) at the same time.
First, let’s declare our dependencies:

```groovy
dependencies {
  implementation 'org.springframework.boot:spring-boot-starter-data-jpa'

  // Dependencies to your used dbms
  implementation 'org.postgresql:postgresql:42.2.1'
  implementation 'com.h2database:h2:1.4.200'
}
```

The second step is to configure the accesses in `application.properties`. The property file is the first and the last time we will have to worry about our persistence configuration. In this file, the 3 lines commented out are the only part to change to switch from PostgreSQL to H2.

```properties
spring.datasource.username=user
spring.datasource.password=password
spring.datasource.generate-unique-name=true
# Automatically create & update the database schema from code.
spring.jpa.hibernate.ddl-auto=update

#spring.datasource.url=jdbc:h2:mem:database_name
spring.datasource.url=jdbc:postgresql://localhost:5432/database_name

#spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.driver-class-name=org.postgresql.Driver

#spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQL10Dialect
```

> Documentation links:

> [Database configuration](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-configure-datasource)

> [Available properties](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#data-properties)

#### Define a model

Defining a model is as simple as using annotations defined on [JSR-317](https://www.jcp.org/en/jsr/detail?id=317). These annotations are available through the package _javax.persistence,_ which is available through the JPA dependency.

For instance, the code below creates a _Delivery_ entity. Our entity identifier is the field _id_, which will be automatically initialized and increased on each new saved entity in the database thanks to the annotation `@GeneratedValue`.

_Note: All attributes publicly available will be set into the JSON representation of the entity in the API responses._

```java
@Entity
@Table(name = "delivery")
public class Delivery {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    long id;

    @Column(nullable = false)
    @NotNull
    @Enumerated(EnumType.STRING)
    DeliveryState state;
    
    @Column(nullable = false)
    @NotNull
    String location;

    public Delivery() {
        // Used by Jackson2
    }

    public Delivery(@NotNull DeliveryState state, @NotNull String location) {
        this.state = state;
        this.location = location;
    }

    public long getId() {
        return id;
    }

    public DeliveryState getState() {
        return state;
    }

    public void setState(DeliveryState state) {
        this.state = state;
    }
    
    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }
}

enum DeliveryState {
    PENDING, DELIVERING, WAITING_AT_ARRIVAL, RETURNING, RETURNED, PICKED_UP;
}
```

To ensure consistency of our data class, we applied `@NotNull` validations from [JSR-303](https://jcp.org/en/jsr/detail?id=303), these validations can be enforced on endpoints as we will see during the next section. 
The constraints are contained in the package _javax.validation.constraints_, available through the dependency `spring-boot-starter-validation`.

```groovy
dependencies {
  implementation 'org.springframework.boot:spring-boot-starter-validation'
}
```

> Documentation links:

> [Entity Declaration](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-entity-classes)

> [javax.persistence API documentation (@Entity, @Column, @Enumerate, …)](https://javaee.github.io/javaee-spec/javadocs/javax/persistence/package-summary.html)

> [@GeneratedValue](https://javaee.github.io/javaee-spec/javadocs/javax/persistence/GeneratedValue.html)

> [javax.validation.constraints API documentation (@NotNull)](https://javaee.github.io/javaee-spec/javadocs/javax/validation/constraints/package-summary.html)

#### Expose the model

To interact with our models, we have to define a [Repository](https://docs.spring.io/spring-data/commons/docs/2.4.2/api/org/springframework/data/repository/Repository.html), for instance, a `CrudRepository`.
Doing so is as easy as extending the class with an empty class. Spring Boot will automatically implement functions to interact with the entity.

```java
@Repository
public interface DeliveryRepository extends CrudRepository<Delivery, Long> {
}
```

We annotate this component `@Repository` to make it available to dependency injection. 
Then we can inject and use the repository in any class, for example directly in a controller. 
Using`@Autowired` will automatically retrieve the `@Repository` declared above_._

_Note:_ `_@Repository_` _and_ `_@Service_` _behave exactly as the main injection annotation_`_@Component_`_, it simply enables to mark a semantic difference._

```java
@RestController
@RequestMapping(value = "/delivery",
        consumes = MediaType.APPLICATION_JSON_VALUE,
        produces = MediaType.APPLICATION_JSON_VALUE)
public class DeliveryController {

    private final DeliveryRepository deliveryRepository;

    @Autowired
    public DeliveryController(DeliveryRepository deliveryRepository) {
        this.deliveryRepository = deliveryRepository;
    }

    @RequestMapping(value = "", method = RequestMethod.POST)
    public ResponseEntity<Delivery> post(@Valid @RequestBody Delivery delivery) throws ApiException {
        try {
            delivery = deliveryRepository.save(delivery);
        } catch (Exception e) {
            throw new ApiException();
        }
        return new ResponseEntity<>(delivery, HttpStatus.OK);
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public ResponseEntity<Delivery> get(@PathVariable long id) throws ApiException {
        Optional<Delivery> delivery = deliveryRepository.findById(id);
        if (delivery.isEmpty()) {
            throw new NotFoundException();
        }
        return new ResponseEntity<>(delivery.get(), HttpStatus.OK);
    }
}
```

We used the annotation`@Valid` to ensure that our constraints defined above are met on the sent _Delivery_ body.

```shell
$ curl -i "localhost:8080/delivery" -H 'Content-Type: application/json' \
  -X POST -d '{"state": "PENDING"}'                  
HTTP/1.1 400 

$ curl -i "localhost:8080/delivery/1" -H 'Content-Type: application/json'
HTTP/1.1 404 

$ curl -i "localhost:8080/delivery" -H 'Content-Type: application/json' \
  -X POST -d '{"state": "PENDING", "location":"Budapest"}'
HTTP/1.1 200 
{"id":1,"state":"PENDING","location":"Budapest"}

$ curl -i "localhost:8080/delivery/1" -H 'Content-Type: application/json'                                                                                 130 ↵
HTTP/1.1 200
{"id":1,"state":"PENDING","location":"Budapest"}
```

_Note: H2 is an in-memory database so the data will be wiped out at each server restart._

> Documentation Links:

> [CrudRepository API Documentation](https://docs.spring.io/spring-data/commons/docs/2.4.2/api/org/springframework/data/repository/CrudRepository.html)

> [Spring Component Declaration](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#using-boot-spring-beans-and-dependency-injection)

> [javax.validation API documentation (@Valid)](https://javaee.github.io/javaee-spec/javadocs/javax/validation/package-summary.html)

### Paginate the results

This section illustrates how well Spring Boot integrates some classic features of a web API. 
To paginate the access to our previous entity _Delivery,_ we simply have to change the repository’s extended class from `CrudRepository` to `PagingAndSortingRepository`.

```java
@Repository
public interface DeliveryRepository extends PagingAndSortingRepository<Delivery, Long> {
}
```

This repository implementation provides a new method `findAll(Pageable)` returning a `Page`. 
The class `Pageable` configures the page and page size to return.

```java
@RestController
@RequestMapping(value = "/delivery",
        consumes = MediaType.APPLICATION_JSON_VALUE,
        produces = MediaType.APPLICATION_JSON_VALUE)
public class DeliveryController {

    private final DeliveryRepository deliveryRepository;

    @Autowired
    public DeliveryController(DeliveryRepository deliveryRepository) {
        this.deliveryRepository = deliveryRepository;
    }

    @RequestMapping(value = "", method = RequestMethod.GET)
    public ResponseEntity<Page<Delivery>> index(@RequestParam(required = false, defaultValue = "0") int page) {
        Pageable pageable = PageRequest.of(page, 50);
        return new ResponseEntity<>(deliveryRepository.findAll(pageable), HttpStatus.OK);
    }
}
```

The endpoint will then serve the whole `Page` object’s data upon request.

```shell
$ curl "localhost:8080/delivery" -H 'Content-Type: application/json' | jq                                                                                   4 ↵
{
  "content": [
    {
      "id": 1,
      "state": "PENDING",
      "location": "Budapest"
    }
  ],
  "pageable": {
    "sort": {
      "sorted": false,
      "unsorted": true,
      "empty": true
    },
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 50,
    "paged": true,
    "unpaged": false
  },
  "totalPages": 1,
  "totalElements": 1,
  "last": true,
  "first": true,
  "size": 50,
  "number": 0,
  "sort": {
    "sorted": false,
    "unsorted": true,
    "empty": true
  },
  "numberOfElements": 1,
  "empty": false
}
```

> Documentation links:

> [PagingAndSortingRepository API Documentation](https://docs.spring.io/spring-data/commons/docs/2.4.2/api/org/springframework/data/repository/PagingAndSortingRepository.html)

> [PageRequest API Documentation](https://docs.spring.io/spring-data/commons/docs/2.4.2/api/org/springframework/data/domain/PageRequest.html)

> [Page API Documentation](https://docs.spring.io/spring-data/commons/docs/2.4.2/api/org/springframework/data/domain/Page.html)

### Test the application

Spring Boot provides every tool to easily test controllers with a set of APIs and [mocks](https://en.wikipedia.org/wiki/Mock_object). 
Mostly, `MockMvc` will enable us to send requests and assert response content without having to worry about technicalities.

As an example, we are testing the _POST_ endpoint from the section above. One of these tests is successfully creating a _Delivery_ entity, and the second one simulates an error coming from the database.

To avoid relying on a physical instance of a persistence layer, we injected our DeliveryRepository instance using `@MockBean`, which creates and injects a mock of our component.

```java
@SpringBootTest
@AutoConfigureMockMvc
class DeliveryControllerTest {
    @Autowired
    private MockMvc mvc;

    @MockBean
    DeliveryRepository deliveryRepository;

    @Test
    void testPostDeliveryOk() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        Map<String, String> delivery = getValidDelivery();
        String body = mapper.writeValueAsString(delivery);
        MockHttpServletRequestBuilder accept =
                MockMvcRequestBuilders.post("/delivery")
                        .accept(MediaType.APPLICATION_JSON)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body);
        mvc.perform(accept).andExpect(status().isOk());
    }

    @Test
    void testPostPersistIssue() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        Map<String, String> delivery = getValidDelivery();
        String body = mapper.writeValueAsString(delivery);
        Mockito.when(deliveryRepository.save(Mockito.any())).thenThrow(new RuntimeException());

        MockHttpServletRequestBuilder accept =
                MockMvcRequestBuilders.post("/delivery")
                        .accept(MediaType.APPLICATION_JSON)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body);

        mvc.perform(accept).andExpect(status().is4xxClientError());
    }

    private Map<String, String> getValidDelivery() {
        Map<String, String> delivery = new HashMap<>();
        delivery.put("state", "PENDING");
        delivery.put("location", "Rome");
        return delivery;
    }
}
```

> Documentation links:

> [@SpringBootTest](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-testing-spring-boot-applications)

> [@AutoConfiguredMockMvc](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-testing-spring-boot-applications-testing-with-mock-environment)

> [@MockBean](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-testing-spring-boot-applications-mocking-beans)

> [MockMvc api Documentation](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/web/servlet/MockMvc.html)

### Package the application

Spring boot also eases the application packaging either as a standalone jar or a docker image.

*   To create a ready to run _fat jar_, execute `./gradlew bootJar`.
*   To build a _docker image_, execute `./gradlew bootBuildImage`.

Note that docker does not like uppercase characters in the image name, but we can easily customize the image name and version.

```groovy
// Only use lowercase on docker image name
tasks.named("bootBuildImage") {
	imageName = "${rootProject.name.toLowerCase()}:${version}"
}
```

> Documentation links:

> [Create an application fat jar](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#getting-started-first-application-executable-jar)

> [Configure Docker Image](https://docs.spring.io/spring-boot/docs/2.4.2/reference/htmlsingle/#boot-features-container-images)

### Conclusion

Spring Boot can be used with a handful of annotations and will manage most of the configuration for you. 
However, most of the configuration can be overridden to provide your own behavior if necessary. 
This makes it a good framework to design proof of concepts while keeping room for optimization if the project grows specific needs.

If you want to know more about the framework, I can’t stress enough the quality of the [Reference Documentation](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/), which gives really good details.

If you want to play around with some code, you can find all those concepts on an example delivery API [on GitHub](https://github.com/aveuiller/frameworks-bootstrap/tree/master/SpringBoot).
