#!/usr/bin/env bash

set -e

# DEVO Deployment Script
# Automated deployment for DEVO multi-agent system

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAINS=("api.dev-o.ai" "dev-o.ai" "www.dev-o.ai" "docs.dev-o.ai")
EMAIL="${SSL_EMAIL:-admin@dev-o.ai}"

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                                      ║${NC}"
    echo -e "${BLUE}║     DEVO Deployment Script           ║${NC}"
    echo -e "${BLUE}║     Multi-Agent Development System   ║${NC}"
    echo -e "${BLUE}║                                      ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi

    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi

    print_success "All prerequisites satisfied"
}

# Check DNS
check_dns() {
    print_info "Checking DNS configuration..."

    for domain in "${DOMAINS[@]}"; do
        if host "$domain" &> /dev/null; then
            print_success "DNS configured for $domain"
        else
            print_warning "DNS not configured for $domain"
        fi
    done
}

# Build Docker images
build_images() {
    print_info "Building Docker images..."
    docker compose build --no-cache
    print_success "Docker images built successfully"
}

# Start services
start_services() {
    print_info "Starting Docker services..."
    docker compose up -d
    print_success "Services started"
}

# Wait for services
wait_for_services() {
    print_info "Waiting for services to be healthy..."

    for i in {1..30}; do
        if docker compose ps | grep -q "healthy"; then
            print_success "Services are healthy"
            return 0
        fi
        echo -n "."
        sleep 2
    done

    print_warning "Some services may not be healthy yet"
}

# Run migrations
run_migrations() {
    print_info "Running database migrations..."
    docker compose exec -T backend python manage.py migrate
    print_success "Migrations completed"
}

# Collect static files
collect_static() {
    print_info "Collecting static files..."
    docker compose exec -T backend python manage.py collectstatic --noinput
    print_success "Static files collected"
}

# Create superuser
create_superuser() {
    print_info "Creating superuser..."
    print_warning "You will be prompted for superuser credentials"
    docker compose exec backend python manage.py createsuperuser
}

# Setup SSL
setup_ssl() {
    print_info "Setting up SSL certificates..."

    for domain in "${DOMAINS[@]}"; do
        print_info "Obtaining certificate for $domain..."
        docker compose run --rm certbot certonly --webroot \
            -w /var/www/certbot \
            -d "$domain" \
            --email "$EMAIL" \
            --agree-tos \
            --non-interactive || print_warning "Failed to obtain certificate for $domain"
    done

    print_info "Restarting Nginx..."
    docker compose restart nginx
    print_success "SSL setup completed"
}

# Verify deployment
verify_deployment() {
    print_info "Verifying deployment..."

    # Check backend health
    if docker compose exec -T backend curl -f http://localhost:8000/api/health/ &> /dev/null; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
    fi

    # Check services
    print_info "Running services:"
    docker compose ps
}

# Show next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  Deployment Complete! 🚀             ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
    echo ""
    print_info "Your DEVO system is now running!"
    echo ""
    echo "Services:"
    echo -e "  ${BLUE}Backend API:${NC} https://api.dev-o.ai"
    echo -e "  ${BLUE}Main Site:${NC} https://dev-o.ai"
    echo -e "  ${BLUE}Documentation:${NC} https://docs.dev-o.ai"
    echo -e "  ${BLUE}Admin Panel:${NC} https://api.dev-o.ai/admin"
    echo -e "  ${BLUE}API Docs:${NC} https://api.dev-o.ai/api/docs"
    echo ""
    echo "CLI Installation:"
    echo -e "  ${BLUE}curl -fsSL https://dev-o.ai/install.sh | bash${NC}"
    echo ""
    echo "Management Commands:"
    echo -e "  ${BLUE}View logs:${NC} docker compose logs -f"
    echo -e "  ${BLUE}Restart:${NC} docker compose restart"
    echo -e "  ${BLUE}Stop:${NC} docker compose down"
    echo -e "  ${BLUE}Update:${NC} git pull && docker compose up -d --build"
    echo ""
}

# Main deployment flow
main() {
    print_banner

    check_prerequisites
    check_dns

    # Build and start
    build_images
    start_services
    wait_for_services

    # Setup application
    run_migrations
    collect_static

    # Optional SSL setup
    read -p "Setup SSL certificates? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_ssl
    fi

    # Optional superuser
    read -p "Create superuser account? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_superuser
    fi

    verify_deployment
    show_next_steps
}

# Run main deployment
main
