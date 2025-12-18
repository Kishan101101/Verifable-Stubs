# Verifiable Stubs - AWS Deployment Guide

## Prerequisites
- AWS Account
- AWS CLI configured
- Docker installed (for containerization)
- Git installed

## Deployment Options

### Option 1: Deploy on AWS Elastic Beanstalk

#### Step 1: Create Elastic Beanstalk Application

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init -p python-3.11 verifiable-stubs --region us-east-1

# Create environment
eb create verifiable-stubs-prod
```

#### Step 2: Configure Environment Variables

```bash
# Set environment variables
eb setenv \
  FLASK_ENV=production \
  FLASK_DEBUG=False \
  SECRET_KEY=your-secret-key \
  DB_USER=admin \
  DB_PASSWORD=your-secure-password \
  DB_HOST=your-rds-endpoint.amazonaws.com \
  DB_PORT=5432 \
  DB_NAME=verifiable_stubs \
  DATABASE_URL=postgresql://admin:your-secure-password@your-rds-endpoint.amazonaws.com:5432/verifiable_stubs
```

#### Step 3: Deploy Application

```bash
# Deploy
eb deploy

# Open in browser
eb open
```

### Option 2: Deploy on AWS RDS + EC2

#### Step 1: Create RDS PostgreSQL Database

```bash
# Using AWS Console or CLI
aws rds create-db-instance \
  --db-instance-identifier verifiable-stubs-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password your-secure-password \
  --allocated-storage 20 \
  --publicly-accessible
```

#### Step 2: Launch EC2 Instance

```bash
# Launch Ubuntu 22.04 instance
# SSH into instance and run:

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3.11 python3-pip python3-venv git -y

# Clone repository
git clone your-repo-url
cd Verifable-Stubs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://admin:password@rds-endpoint:5432/verifiable_stubs

# Run migrations
python -m alembic upgrade head

# Start application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Option 3: Deploy using Docker + ECS

#### Step 1: Create Docker Image

```bash
# Create Dockerfile (save as Dockerfile in project root)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

#### Step 2: Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name verifiable-stubs

# Build image
docker build -t verifiable-stubs:latest .

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag verifiable-stubs:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/verifiable-stubs:latest

# Push image
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/verifiable-stubs:latest
```

#### Step 3: Deploy on ECS

Use AWS Console to create ECS Cluster and Task Definition pointing to your ECR image.

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Use RDS PostgreSQL with encrypted credentials
- [ ] Enable CORS appropriately
- [ ] Enable CloudWatch logging
- [ ] Set up auto-scaling
- [ ] Configure security groups properly
- [ ] Use HTTPS/SSL certificates
- [ ] Set up monitoring and alerts
- [ ] Configure backup and disaster recovery
- [ ] Document API endpoints
- [ ] Set up CI/CD pipeline

## AWS Services Used

- **RDS**: PostgreSQL database
- **Elastic Beanstalk**: Application hosting (recommended)
- **EC2**: Virtual servers (alternative)
- **ECS**: Container orchestration (alternative)
- **CloudWatch**: Monitoring and logging
- **S3**: Static assets (optional)
- **Route 53**: DNS management (optional)
- **Certificate Manager**: SSL certificates

## Monitoring

```bash
# View logs
eb logs

# Monitor application
eb health

# SSH into instance
eb ssh
```

## Troubleshooting

### Database Connection Issues
- Check RDS security group allows EC2/EB inbound traffic on port 5432
- Verify DATABASE_URL environment variable
- Check credentials in .env

### Application not starting
- Check CloudWatch logs
- Verify all dependencies in requirements.txt
- Check Python version compatibility

### Migration Issues
```bash
# Run migrations manually
eb ssh
source venv/bin/activate
python -m alembic upgrade head
```

## Scaling

### Auto Scaling Configuration
```bash
# Set up auto-scaling policy
eb scale 2  # Set minimum 2 instances
```

## Cost Optimization

- Use RDS Free Tier for development
- Set appropriate EC2 instance types
- Use CloudFront for static assets
- Monitor CloudWatch for unused resources
- Set up billing alerts
