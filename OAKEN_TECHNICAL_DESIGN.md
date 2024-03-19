# Oaken Spirits Technical Design Document

## 1. Description of the Problem

Oaken Spirits is looking to expand and the current application implementations are not scalable, do not deliver real-time updates, have multiple databases, and lack a consolidated analytics solutions.

## 2. Solution Requirements

1. Create a scalable solution.
1. Create a data pipeline that integrates the systems and provides real-time updates.
1. Create a single database as the single source of truth.
1. Provide an analytics solution for management.

## 3. Glossary

- **A single source of truth (SSOT):** The practice of aggregating the data from many systems within an organization to a single location.
- **Scope creep:** Adding additional features or functions of a new product, requirements, or work that is not authorized during project scoping.
- **OLTP:** Online Transactional Processing. I.e. every day business services.
- **OLAP:** Online analytical processing.For data analytics.
- **Apache Kafka:** A pub/sub message queue.
- **Pub/sub message queue:** Publisher and subscriber message queue. Where a source publishes messages to a queue and a subscribers get those messages from the queue.
- **ETL:** Extract, Transform, Load. The order of operations in a data transfer.
- **SuperSet:** Data analytics and dashboard application.
- **Airflow:** Application for scheduling and orchestration of data pipelines or workflows.
- **Virtual Machine (VM):** a compute resource that uses software instead of a physical computer to run programs and deploy apps.

## 4. Out of Scope (Non-goals)

1. Implementing new applications that are not required for the initially identified requirements.
1. Implementation team is not the training team.
    - Documentation provided, but team trainers retain responsibility.

## 5. Assumptions

1. IT leadership is willing to learn new applications and processes to support post implementation.
1. Data contracts will be enforced.

## 6. Solution

![App Services Diagram](images/oaken-service-diagram.png)

1. Scalable: use of cloud services will allow scalability to a national level if desired.
    - Virtual Machines (VM) allows auto scaling.
        - Machines Images can be used for quick service recovery.
        - Machine images can be imported into different cloud services.
    - Cloud services have high uptime service agreements which reduces downtime and recovery as services grow.
1. Service Integration:
    - Kafka Pub/sub Message queue to transfer data between services.
        - Apache Kafka can scale to over a 1 million messages a second.
    - API for invoice integration with MySQL.
1. SSOT: Integrate into MySQL database for OLTP.
1. Analytics:
    - Database snapshot used for ETL to data warehouse.
    - Data extract to SuperSet.
    - Automate with Airflow.

## 7. Security Considerations

1. For local machine IP:
    - All VMs SSH port 22.
    - Kafka port 9092 (for Invoice application).
    - MySQL 33060.
1. For cloud resources:
    - Kafka port 9092.
    - MySQL 33060.
1. Sensitive environment variables.
    - AWS Systems Manager Parameter Store.

## 8. Cost Analysis

Oaken Spirits is still a small company and preference is to budget conscious choices that will grow as the company grows rather than a system that can necessarily support future growth out of the box.

Open source applications are preferred over paid with in-house support.

### Application Cost Estimate

1. No additional cost.

### Cloud Cost Estimate

1. AWS Parameter Store
    - Standard = Free

#### AWS 3 year commitment

1. Business applications virtual machines
    - VM: m6i.large (business apps)
        - Monthly: $44.43
    - 10GB Block Storage
        - Monthly $0.80
    - Data transfer
        - free
    - 4 virtual machines total (business apps)
        - $182.52 month
        - $2190.24 year
    - VM: r6i.xlarge (database)
        - $ 95.96 month
    - 10GB Block storage
        - Monthly: $0.80  
    - 2X Daily Snapshot
        - Monthly: $2.80
    - 1 virtual machine total (database)
        - Monthly: $99.56
        - Yearly: $1194.72
    - TOTAL
        - Monthly: $282.08
        - Yearly: $3384.96

## 9. Cross-region Considerations

Not applicable.

## 10. Operational Readiness Considerations

Discuss how your solution will support operational excellence, ensuring customer satisfaction with a frugal level of support.

Aim to answer:

How your chosen solution will be deployed?
What metrics and alarms will be key to monitoring the health of your solution?
How are your solution limits enforced?
Will there be any throttling or blacklisting mechanisms in place?
Will there be any data recovery mechanisms in place?
If this is a multi-tenant solution, how are you dealing with noisy neighbor issues?
How will your solution be debugged when problems occur?
How will your solution recover in case of a brown-out?
Are there any operational tools required for your solution?

## 11. Risks and Open Issues

If there are any risks or unknowns, list them here. Are there any open questions which could impact your design for which you do not currently have answers? How are you going to get answers? Will any required team members be loaned to other teams during the time slated for implementation? Are all of required dependencies available in all the regions you need them? What are the one way doors, and are we sure we want to go through them?

## 12. Solutions considered and discarded

What alternatives have you have considered and discarded? Why don’t these work? Be brief, linking to other documents for details is ok, but always provide a summary inline.

Only alternative solutions that an impartial observer would deem credible need be documented.

If an alternative solution is not appropriate now, but may be in the future, please discuss potential migration paths.

## 13. Work Required

Include a high level breakdown of the work required to implement your proposed solution, including t-shirt size estimates (S, M, XL) where appropriate. Also, specifically call out if this solution requires resources from other teams to be completed (away teams, dependencies etc.)

## 14. High-level Test Plan

At a high level, describe how your chosen solution be tested.

## 15. References

Links to any other documents that may be relevant, or sources you wish to cite.
