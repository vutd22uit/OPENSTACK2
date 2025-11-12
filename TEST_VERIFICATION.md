# Test & Verification Guide

## 🎯 Overview

This guide helps you test the microservices locally and verify all components work correctly.

## ✅ Bugs Fixed

### Critical Bugs Resolved
1. ✅ **Dockerfile Path Errors** - Fixed COPY commands for shared library
2. ✅ **Pydantic Configuration** - Removed complex BaseSettings, simplified to basic class
3. ✅ **Import Path Issues** - Added proper PYTHONPATH and sys.path configuration
4. ✅ **Heavy Dependencies** - Minimized to core dependencies only
5. ✅ **API Gateway Rate Limiting** - Added error handling for Redis connection
6. ✅ **Health Check Logic** - Fixed database connectivity checks

## 🚀 Quick Start (Local Testing)

### Prerequisites
```bash
# Required
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

# Optional
- Docker & Docker Compose
- RabbitMQ 3+ (for async features)
```

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Stop services
docker-compose -f docker-compose.microservices.yml down
```

### Option 2: Local Python (Development)

#### Setup Databases
```bash
# PostgreSQL
createdb users_db
createdb products_db
createdb orders_db

# Or use Docker
docker run -d --name postgres \\
  -e POSTGRES_USER=devuser \\
  -e POSTGRES_PASSWORD=devpass \\
  -p 5432:5432 postgres:15-alpine

docker run -d --name redis -p 6379:6379 redis:7-alpine
```

#### Run User Service
```bash
cd services/user-service

# Set environment
export DATABASE_URL="postgresql://devuser:devpass@localhost:5432/users_db"
export SECRET_KEY="dev-secret-key"
export JWT_SECRET_KEY="dev-jwt-secret"
export REDIS_URL="redis://localhost:6379"
export PORT=5001

# Install dependencies
pip install -r requirements.txt
pip install -r ../shared/requirements.txt

# Run
python app.py
```

#### Run Product Service
```bash
cd services/product-service

export DATABASE_URL="postgresql://devuser:devpass@localhost:5432/products_db"
export SECRET_KEY="dev-secret-key"
export PORT=5002

pip install -r requirements.txt
pip install -r ../shared/requirements.txt

python app.py
```

#### Run Order Service
```bash
cd services/order-service

export DATABASE_URL="postgresql://devuser:devpass@localhost:5432/orders_db"
export SECRET_KEY="dev-secret-key"
export USER_SERVICE_URL="http://localhost:5001"
export PRODUCT_SERVICE_URL="http://localhost:5002"
export PORT=5003

pip install -r requirements.txt
pip install -r ../shared/requirements.txt

python app.py
```

#### Run API Gateway
```bash
cd services/api-gateway

export REDIS_URL="redis://localhost:6379"
export USER_SERVICE_URL="http://localhost:5001"
export PRODUCT_SERVICE_URL="http://localhost:5002"
export ORDER_SERVICE_URL="http://localhost:5003"
export PORT=8080

pip install -r requirements.txt
pip install -r ../shared/requirements.txt

python app.py
```

## 🧪 API Testing

### 1. Health Checks

```bash
# Check all services are running
curl http://localhost:5001/health  # User Service
curl http://localhost:5002/health  # Product Service
curl http://localhost:5003/health  # Order Service
curl http://localhost:8080/health  # API Gateway

# Check readiness (includes DB check)
curl http://localhost:5001/ready
curl http://localhost:5002/ready
curl http://localhost:5003/ready
```

### 2. User Service Tests

```bash
# Register a new user
curl -X POST http://localhost:5001/api/v1/users/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "alice@example.com",
    "username": "alice",
    "password": "SecurePass123",
    "first_name": "Alice",
    "last_name": "Smith"
  }'

# Expected: 201 Created with user object

# Login
curl -X POST http://localhost:5001/api/v1/users/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "alice",
    "password": "SecurePass123"
  }'

# Expected: 200 OK with JWT token
# Save the token for authenticated requests

# Get user by ID (requires auth)
TOKEN="<JWT_TOKEN_FROM_LOGIN>"
curl -H "Authorization: Bearer $TOKEN" \\
  http://localhost:5001/api/v1/users/1

# List users
curl -H "Authorization: Bearer $TOKEN" \\
  http://localhost:5001/api/v1/users/?page=1&limit=10
```

### 3. Product Service Tests

```bash
# Create product
curl -X POST http://localhost:5002/api/v1/products/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "MacBook Pro",
    "description": "16-inch M3 Max",
    "price": 2499.99,
    "sku": "MBP-16-M3",
    "stock_quantity": 50,
    "category": "Laptops"
  }'

# Expected: 201 Created with product object

# List products (paginated)
curl "http://localhost:5002/api/v1/products/?page=1&limit=10"

# Expected: 200 OK with products array

# Get product by ID
curl http://localhost:5002/api/v1/products/1

# Expected: 200 OK with product object

# Create more products for testing
curl -X POST http://localhost:5002/api/v1/products/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "iPhone 15 Pro",
    "description": "256GB, Titanium",
    "price": 999.99,
    "sku": "IPH-15-PRO-256",
    "stock_quantity": 100,
    "category": "Phones"
  }'
```

### 4. Order Service Tests (Inter-Service Communication)

```bash
# Create order (demonstrates inter-service calls)
curl -X POST http://localhost:5003/api/v1/orders/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ],
    "shipping_address": "123 Main St, San Francisco, CA 94105"
  }'

# Expected: 201 Created with order object
# This will:
# 1. Call User Service to verify user exists
# 2. Call Product Service to get product details
# 3. Calculate total
# 4. Create order in orders database

# Get order by ID
curl http://localhost:5003/api/v1/orders/1

# Expected: 200 OK with order details
```

### 5. API Gateway Tests

All the above endpoints also work through the API Gateway:

```bash
# User registration through gateway
curl -X POST http://localhost:8080/api/v1/users/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "bob@example.com",
    "username": "bob",
    "password": "SecurePass456",
    "first_name": "Bob",
    "last_name": "Johnson"
  }'

# List products through gateway
curl http://localhost:8080/api/v1/products/

# Create order through gateway
curl -X POST http://localhost:8080/api/v1/orders/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": 1,
    "items": [{"product_id": 1, "quantity": 1}],
    "shipping_address": "456 Oak Ave, New York, NY 10001"
  }'
```

## 🔍 Verification Checklist

### Service Health
- [ ] User Service responds to /health
- [ ] Product Service responds to /health
- [ ] Order Service responds to /health
- [ ] API Gateway responds to /health
- [ ] All services respond to /ready with database:true

### User Service
- [ ] Can register new user
- [ ] Can login and receive JWT token
- [ ] Cannot register duplicate username/email
- [ ] Password is hashed (not stored in plain text)
- [ ] JWT token validates correctly
- [ ] Can get user by ID with valid token
- [ ] Cannot access without token (401 error)

### Product Service
- [ ] Can create new product
- [ ] Can list products with pagination
- [ ] Can get product by ID
- [ ] Returns 404 for non-existent product
- [ ] Pagination works correctly

### Order Service
- [ ] Can create order successfully
- [ ] Validates user exists (calls User Service)
- [ ] Validates products exist (calls Product Service)
- [ ] Calculates total correctly
- [ ] Returns proper error if user/product doesn't exist
- [ ] Can retrieve order by ID

### API Gateway
- [ ] Routes requests to User Service
- [ ] Routes requests to Product Service
- [ ] Routes requests to Order Service
- [ ] Rate limiting works (Redis required)
- [ ] Returns 503 if backend service is down

### Circuit Breakers
- [ ] Order Service handles User Service failures gracefully
- [ ] Order Service handles Product Service failures gracefully
- [ ] Circuit breaker opens after 5 failures
- [ ] Circuit breaker recovers after timeout

## 📊 Monitoring

### View Logs
```bash
# Docker Compose
docker-compose -f docker-compose.microservices.yml logs -f [service-name]

# Local Python
# Logs output to console
```

### Check Database
```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U devuser -d users_db

# List users
SELECT * FROM users;

# Connect to products database
docker exec -it postgres psql -U devuser -d products_db
SELECT * FROM products;

# Connect to orders database
docker exec -it postgres psql -U devuser -d orders_db
SELECT * FROM orders;
```

### Check Redis
```bash
docker exec -it redis redis-cli

# Check rate limit keys
KEYS *

# Get rate limit info
GET rate-limit:*
```

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs [service-name]

# Common issues:
# 1. Database not ready - wait 30 seconds and restart
# 2. Port already in use - change port in docker-compose.yml
# 3. Import errors - rebuild images: docker-compose build --no-cache
```

### Import Errors
```bash
# Verify PYTHONPATH
docker exec -it [container] env | grep PYTHONPATH

# Should show: PYTHONPATH=/app

# Verify shared library exists
docker exec -it [container] ls -la /app/shared
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection
docker exec -it [service-container] bash
python -c "import psycopg2; conn = psycopg2.connect('postgresql://devuser:devpass@postgres:5432/users_db'); print('Connected')"
```

### Inter-Service Communication Fails
```bash
# Check service URLs
echo $USER_SERVICE_URL
echo $PRODUCT_SERVICE_URL

# Test connectivity
curl http://user-service:5001/health
# Or from host:
curl http://localhost:5001/health
```

## ✅ Success Criteria

All tests pass if:
1. ✅ All health checks return 200
2. ✅ User can register and login
3. ✅ Products can be created and listed
4. ✅ Orders can be created with inter-service communication
5. ✅ API Gateway routes all requests correctly
6. ✅ No errors in service logs
7. ✅ Database tables are created and populated

## 📝 Notes

- First run may take longer as databases initialize
- Wait 30-60 seconds for all services to be ready
- Check logs if any service fails to start
- All fixes have been applied and tested
- Services use graceful degradation for optional features

## 🎉 Next Steps

Once all tests pass:
1. Review MICROSERVICES_README.md for usage guide
2. See docs/MICROSERVICES_MIGRATION.md for architecture details
3. Check RUNTIME_FIXES.md for technical fixes applied
4. Ready to deploy to staging/production!
