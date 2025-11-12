# Microservices Migration Guide

## Overview

This document describes the migration from monolithic architecture to microservices.

## Architecture Changes

### Before: Monolithic Application
```
┌─────────────────────────────────┐
│      Flask Application          │
│  ┌───────────────────────────┐ │
│  │   User Management         │ │
│  ├───────────────────────────┤ │
│  │   Product Catalog         │ │
│  ├───────────────────────────┤ │
│  │   Order Processing        │ │
│  └───────────────────────────┘ │
│          ↓                      │
│  ┌───────────────────────────┐ │
│  │   Single Database         │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

### After: Microservices Architecture
```
┌─────────────────────────────────────────────────┐
│              API Gateway (Port 8080)            │
│        Rate Limiting, Routing, Auth             │
└────────┬────────────┬────────────┬──────────────┘
         │            │            │
    ┌────▼────┐  ┌───▼────┐  ┌───▼────┐
    │  User   │  │Product │  │ Order  │
    │ Service │  │Service │  │Service │
    │  :5001  │  │ :5002  │  │ :5003  │
    └────┬────┘  └───┬────┘  └───┬────┘
         │           │            │
    ┌────▼────┐ ┌───▼────┐  ┌───▼────┐
    │Users DB │ │Prod DB │  │Order DB│
    └─────────┘ └────────┘  └────────┘
```

## Services

### 1. User Service (Port 5001)
**Responsibilities:**
- User registration and authentication
- JWT token generation
- User profile management

**Endpoints:**
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/:id` - Get user profile
- `PUT /api/v1/users/:id` - Update user profile

### 2. Product Service (Port 5002)
**Responsibilities:**
- Product catalog management
- Inventory tracking
- Product search and filtering

**Endpoints:**
- `GET /api/v1/products` - List products
- `GET /api/v1/products/:id` - Get product details
- `POST /api/v1/products` - Create product
- `PUT /api/v1/products/:id` - Update product

### 3. Order Service (Port 5003)
**Responsibilities:**
- Order creation and processing
- Order status tracking
- Integration with user and product services

**Endpoints:**
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/:id` - Get order details
- `GET /api/v1/orders/user/:userId` - Get user orders

### 4. API Gateway (Port 8080)
**Responsibilities:**
- Single entry point for all client requests
- Request routing to appropriate services
- Rate limiting and authentication
- Load balancing

## Running Locally

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### Start All Services
\`\`\`bash
# Start all microservices
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Check service health
curl http://localhost:8080/health
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
\`\`\`

### Stop Services
\`\`\`bash
docker-compose -f docker-compose.microservices.yml down
\`\`\`

## Testing the Microservices

### 1. Register a User
\`\`\`bash
curl -X POST http://localhost:8080/api/v1/users/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
\`\`\`

### 2. Login
\`\`\`bash
curl -X POST http://localhost:8080/api/v1/users/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
\`\`\`

### 3. Create a Product
\`\`\`bash
curl -X POST http://localhost:8080/api/v1/products/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Sample Product",
    "description": "A test product",
    "price": 29.99,
    "sku": "PROD-001",
    "stock_quantity": 100,
    "category": "Electronics"
  }'
\`\`\`

### 4. Create an Order
\`\`\`bash
curl -X POST http://localhost:8080/api/v1/orders/ \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -d '{
    "user_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ],
    "shipping_address": "123 Main St, City, Country"
  }'
\`\`\`

## Inter-Service Communication

Services communicate via HTTP REST APIs. The Order Service demonstrates this by:

1. Calling User Service to verify user exists
2. Calling Product Service to get product details and validate
3. Calculating order total
4. Creating order in its own database

Circuit breakers prevent cascade failures when services are unavailable.

## Distributed Tracing

View traces in Jaeger UI:
- Open http://localhost:16686
- Select service (user-service, product-service, etc.)
- View request traces across services

## Monitoring

- **Jaeger**: http://localhost:16686 (Distributed tracing)
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Prometheus Metrics**: Each service exposes `/metrics` endpoint

## Deployment to Kubernetes

See `infrastructure/kubernetes/microservices/` for Kubernetes manifests.

\`\`\`bash
# Deploy all services
kubectl apply -f infrastructure/kubernetes/microservices/

# Check status
kubectl get pods -n microservices
kubectl get services -n microservices
\`\`\`

## Benefits of Microservices

1. **Independent Scaling**: Scale services based on load
2. **Technology Flexibility**: Different services can use different tech stacks
3. **Resilience**: Service failures are isolated
4. **Team Autonomy**: Teams can develop services independently
5. **Faster Deployment**: Deploy services independently

## Trade-offs

1. **Complexity**: More moving parts to manage
2. **Network Latency**: Inter-service calls add latency
3. **Data Consistency**: Distributed transactions are challenging
4. **Testing**: End-to-end testing more complex

## Next Steps

1. Add message queue for async communication
2. Implement API versioning
3. Add service mesh (Istio) for advanced traffic management
4. Implement saga pattern for distributed transactions
5. Add API documentation (Swagger/OpenAPI)
