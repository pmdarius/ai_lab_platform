## Database Schema Documentation

This document provides a comprehensive overview of the database schema for the KSRCE AI Lab Management Platform. It includes a visual diagram of the database models and a detailed explanation of each model and its fields.

### Database Schema Diagram

The following diagram illustrates the relationships between the different models in the database:

![Database Schema](database_schema.png)

### Model Explanations

The database is composed of several key models that work together to manage users, bookings, payments, and other aspects of the platform.

#### Core Models

- **User**: This is a custom user model that extends Django's `AbstractUser`. It includes fields for user roles, wallet balance, and other profile information.

#### Payments Models

- **Wallet**: Each user has a wallet to store their balance.
- **Transaction**: Records all transactions, including wallet recharges and slot booking payments.

#### Bookings Models

- **GPUSlot**: Represents an available GPU slot that can be booked by users.
- **Booking**: Records a user's booking of a GPU slot for a specific time period.

#### Mentors Models

- **Mentor**: Stores information about available mentors.
- **MentorSession**: Records a user's booking of a session with a mentor.

#### Monitoring Models

- **GPUMetrics**: Stores metrics about GPU usage and performance.

This schema is designed to be scalable and flexible, allowing for future expansion of the platform's features.
