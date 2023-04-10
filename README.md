# Custom-Asynchronus-Sockets

In project 2, we will implement a set of programs that mimic an implementation of load balancing
across DNS servers. Spreading the load of incoming DNS queries among replica DNS servers is
one method by which DNS scales to meet the needs of Internet users. In its simplest form, a “load
balancer” simply picks a single DNS server to respond to any given request, spreading requests as
evenly across servers as possible. This has the effect of using several server machines to simulate
one powerful DNS server.
This project will explore a slightly more sophisticated form of balancing load that also takes
into account the need to respond to requests as early as possible. We will explore request duplication,
i.e., sending the same request to two servers, and picking the response that arrives first. At
the cost of using more system resources, this allows the overall system to hide the delay caused by
a slow server. In this project, we will model a slow server in the extreme by implementing servers
that do not send any response at all in some cases.
