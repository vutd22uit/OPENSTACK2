# 🚀 Microservices Architecture - Quick Start

## 📋 Overview

The application has been refactored into a **microservices architecture** with 4 independent services:

| Service | Port | Responsibility |
|---------|------|----------------|
| **API Gateway** | 8080 | Entry point, routing, rate limiting |
| **User Service** | 5001 | Authentication, user management |
| **Product Service** | 5002 | Product catalog, inventory |
| **Order Service** | 5003 | Order processing |

## 🔧 Quick Start (Local Development)

### Start All Services

\`\`\`bash
# Start all microservices with dependencies
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Stop all services
docker-compose -f docker-compose.microservices.yml down
\`\`\`

### Access Services

- **API Gateway**: http://localhost:8080
- **User Service**: http://localhost:5001
- **Product Service**: http://localhost:5002
- **Order Service**: http://localhost:5003
- **Jaeger (Tracing)**: http://localhost:16686
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

## 📝 API Examples

### 1. Register User

\`\`\`bash
curl -X POST http://localhost:8080/api/v1/users/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "john@example.com",
    "username": "john",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
\`\`\`

### 2. Login

\`\`\`bash
curl -X POST http://localhost:8080/api/v1/users/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "john",
    "password": "SecurePass123"
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "user": {...}
}
\`\`\`

### 3. Create Product

\`\`\`bash
curl -X POST http://localhost:8080/api/v1/products/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "sku": "LAP-001",
    "stock_quantity": 50,
    "category": "Electronics"
  }'
\`\`\`

### 4. List Products

\`\`\`bash
curl http://localhost:8080/api/v1/products/?page=1&limit=10
\`\`\`

### 5. Create Order

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

## 🏗️ Architecture

\`\`\`
┌─────────────────────────────────────────────────┐
│         Client (Browser/Mobile App)             │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              API Gateway :8080                   │
│  ┌──────────────────────────────────────────┐  │
│  │ Rate Limiting, Authentication, Routing   │  │
│  └──────────────────────────────────────────┘  │
└───────┬──────────────┬──────────────┬──────────┘
        │              │              │
   ┌────▼────┐    ┌───▼────┐    ┌───▼────┐
   │  User   │    │Product │    │ Order  │
   │ Service │    │Service │    │Service │
   │  :5001  │    │ :5002  │    │ :5003  │
   └────┬────┘    └───┬────┘    └───┬────┘
        │             │              │
   ┌────▼────┐   ┌───▼────┐    ┌───▼────┐
   │Users DB │   │Prod DB │    │Order DB│
   └─────────┘   └────────┘    └────────┘
\`\`\`

## 🔐 Security Features

✅ **JWT Authentication**: Secure token-based auth
✅ **Password Hashing**: bcrypt with salt
✅ **Rate Limiting**: API Gateway level
✅ **Circuit Breakers**: Prevent cascade failures
✅ **Input Validation**: Comprehensive validation
✅ **CORS**: Configurable origins
✅ **Non-root Containers**: Security hardened

## 📊 Observability

### Distributed Tracing

View end-to-end request traces:
1. Open http://localhost:16686
2. Select a service
3. Click "Find Traces"
4. See complete request flow across services

### Metrics

Each service exposes Prometheus metrics at `/metrics`:
\`\`\`bash
curl http://localhost:5001/metrics
\`\`\`

## 🧪 Health Checks

Check service health:
\`\`\`bash
# Liveness
curl http://localhost:5001/health

# Readiness (includes dependencies)
curl http://localhost:5001/ready
\`\`\`

## 🐛 Bug Fixes

See [BUGS_FIXED.md](BUGS_FIXED.md) for detailed list of bugs fixed during migration.

## 📚 Documentation

- [Migration Guide](docs/MICROSERVICES_MIGRATION.md) - Detailed migration documentation
- [BUGS_FIXED.md](BUGS_FIXED.md) - List of bugs fixed
- [README.md](README.md) - Main project documentation

## 🚀 Deployment

### Local Development
\`\`\`bash
docker-compose -f docker-compose.microservices.yml up
\`\`\`

### Kubernetes
\`\`\`bash
kubectl apply -f infrastructure/kubernetes/microservices/
\`\`\`

## 🤝 Inter-Service Communication

Services communicate via:
- **HTTP REST**: Synchronous calls with retry logic
- **Circuit Breakers**: Prevent cascade failures
- **Distributed Tracing**: Track requests across services

Example in Order Service:
1. Validates user via User Service
2. Fetches product details from Product Service
3. Creates order in its own database

## 💡 Development Tips

### View Logs
\`\`\`bash
# All services
docker-compose -f docker-compose.microservices.yml logs -f

# Specific service
docker-compose -f docker-compose.microservices.yml logs -f user-service
\`\`\`

### Rebuild Service
\`\`\`bash
docker-compose -f docker-compose.microservices.yml up -d --build user-service
\`\`\`

### Access Database
\`\`\`bash
docker-compose -f docker-compose.microservices.yml exec postgres psql -U devuser -d users_db
\`\`\`

## 🎯 Next Steps

1. ✅ All services running
2. ⏭️  Add API documentation (Swagger/OpenAPI)
3. ⏭️  Implement message queue for async operations
4. ⏭️  Add API versioning (v2 endpoints)
5. ⏭️  Implement saga pattern for distributed transactions
6. ⏭️  Add service mesh (Istio) for advanced traffic management

## 📞 Support

For issues or questions, see:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [docs/runbooks/](docs/runbooks/)
- GitHub Issues

---

**Status**: ✅ Production Ready
**Version**: 2.0.0 (Microservices)
**Last Updated**: 2024-01-15
