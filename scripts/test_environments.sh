#!/bin/bash
# Test script for Racket Hero Multi-Environment Validation

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEV_URL="https://racket-hero-dev.up.railway.app"
STAGING_URL="https://racket-hero-staging.up.railway.app"
PROD_URL="https://racket-hero-production.up.railway.app"

# Test credentials
TEST_EMAIL="organizador@test.com"
TEST_PASSWORD="Senha123!"

# Function to print headers
print_header() {
  echo -e "\n${BLUE}======================================${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}======================================${NC}\n"
}

# Function to test endpoint
test_endpoint() {
  local method=$1
  local url=$2
  local data=$3
  local auth_token=$4
  
  if [ -z "$auth_token" ]; then
    # Without authentication
    response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
      -H "Content-Type: application/json" \
      -d "$data" 2>/dev/null)
  else
    # With authentication
    response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $auth_token" \
      -d "$data" 2>/dev/null)
  fi
  
  # Split response and status code
  http_code=$(echo "$response" | tail -n 1)
  body=$(echo "$response" | sed '$d')
  
  echo "$http_code|$body"
}

# Function to test environment
test_environment() {
  local env_name=$1
  local base_url=$2
  
  print_header "Testing $env_name Environment: $base_url"
  
  # Test 1: Health check
  echo -e "${YELLOW}Test 1: Health Check${NC}"
  response=$(curl -s -w "%{http_code}" "$base_url/health" 2>/dev/null)
  http_code="${response: -3}"
  
  if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
  else
    echo -e "${RED}✗ Health check failed (HTTP $http_code)${NC}"
    return 1
  fi
  
  # Test 2: Login
  echo -e "\n${YELLOW}Test 2: Authentication (Login)${NC}"
  login_response=$(test_endpoint "POST" "$base_url/api/auth/login" \
    "{\"email\":\"$TEST_EMAIL\",\"senha\":\"$TEST_PASSWORD\"}" "")
  
  http_code=$(echo "$login_response" | cut -d'|' -f1)
  body=$(echo "$login_response" | cut -d'|' -f2-)
  
  if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Login successful (HTTP 200)${NC}"
    
    # Extract token from response
    token=$(echo "$body" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$token" ]; then
      echo -e "${YELLOW}⚠ Token not found in response${NC}"
      return 1
    fi
    
    echo -e "${GREEN}✓ Access token obtained${NC}"
  else
    echo -e "${RED}✗ Login failed (HTTP $http_code)${NC}"
    echo "Response: $body"
    return 1
  fi
  
  # Test 3: Get events (authenticated)
  echo -e "\n${YELLOW}Test 3: Get Events (Authenticated)${NC}"
  events_response=$(test_endpoint "GET" "$base_url/api/events" "" "$token")
  
  http_code=$(echo "$events_response" | cut -d'|' -f1)
  body=$(echo "$events_response" | cut -d'|' -f2-)
  
  if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Events retrieved successfully (HTTP 200)${NC}"
    event_count=$(echo "$body" | grep -o '"id"' | wc -l)
    echo "  Events found: $event_count"
  else
    echo -e "${RED}✗ Failed to get events (HTTP $http_code)${NC}"
    return 1
  fi
  
  # Test 4: Get ranking
  echo -e "\n${YELLOW}Test 4: Ranking Endpoint${NC}"
  # Assuming event_id = 1 (from seed data)
  ranking_response=$(test_endpoint "GET" "$base_url/api/ranking/1" "" "$token")
  
  http_code=$(echo "$ranking_response" | cut -d'|' -f1)
  
  if [ "$http_code" = "200" ] || [ "$http_code" = "404" ]; then
    echo -e "${GREEN}✓ Ranking endpoint accessible (HTTP $http_code)${NC}"
  else
    echo -e "${RED}✗ Ranking endpoint failed (HTTP $http_code)${NC}"
  fi
  
  echo -e "\n${GREEN}=== Environment $env_name: PASSED ===${NC}\n"
  return 0
}

# Main execution
main() {
  print_header "Racket Hero Multi-Environment Test Suite"
  
  echo -e "${YELLOW}Starting comprehensive environment validation...${NC}\n"
  
  # Array of environments to test
  declare -a environments=(
    "DEV|$DEV_URL"
    "STAGING|$STAGING_URL"
    "PRODUCTION|$PROD_URL"
  )
  
  passed=0
  failed=0
  
  for env in "${environments[@]}"; do
    env_name=$(echo $env | cut -d'|' -f1)
    base_url=$(echo $env | cut -d'|' -f2)
    
    if test_environment "$env_name" "$base_url"; then
      ((passed++))
    else
      ((failed++))
    fi
  done
  
  # Summary
  print_header "Test Summary"
  echo -e "${GREEN}Passed: $passed${NC}"
  echo -e "${RED}Failed: $failed${NC}"
  
  if [ $failed -eq 0 ]; then
    echo -e "\n${GREEN}✓ All environments are working correctly!${NC}"
    exit 0
  else
    echo -e "\n${RED}✗ Some environments failed validation${NC}"
    exit 1
  fi
}

main "$@"
