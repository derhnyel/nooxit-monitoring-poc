from prometheus_client import Counter, Histogram, Gauge, start_http_server, Summary
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Metrics definitions with labels
statements_processed = Counter('statements_processed_total', 'Total banking statements processed', ['customer'])
processing_errors = Counter('process_errors_total', 'Total errors during processing', ['customer'])
latency = Histogram('process_latency_seconds', 'Processing latency in seconds', ['customer'])
model_correctness = Gauge('model_correctness_ratio', 'Model correctness rate (0-1)', ['customer'])
open_positions = Gauge('open_positions', 'Number of open positions left', ['customer', 'transaction'])
closed_positions = Counter('closed_positions_total', 'Total positions closed', ['customer', 'transaction'])
unique_logins = Counter('unique_logins_total', 'Total unique logins', ['customer', 'location', 'latitude', 'longitude'])
erp_http_responses = Counter('erp_http_responses_total', 'Total HTTP responses from ERP service', ['status_code', 'customer','endpoint'])
cpu_usage = Gauge('worker_cpu_usage', 'Simulated CPU usage percentage')
memory_usage = Gauge('worker_memory_usage', 'Simulated memory usage percentage')
network_throughput = Gauge('worker_network_throughput', 'Simulated network throughput in bytes per second')
validation_duration = Summary('validation_duration_seconds', 'Time taken to validate a statement')
validate_failed = Counter('validate_failed_total', 'Total failed validations', ['customer', 'reason'])
validate_success = Counter('validate_success_total', 'Total successful validations', ['customer'])
# Start metrics server
start_http_server(8000)

# Simulate worker behavior
def process_statement(customer, reason, location):
    start = time.time()
    try:
        # Simulating processing logic
        if random.random() < 0.1:  # Simulate 10% error rate
            processing_errors.labels(customer=customer).inc()
            raise Exception("Error processing statement")
        statements_processed.labels(customer=customer).inc()
        open_positions.labels(customer=customer, transaction='').set(random.randint(0, 50))  # Randomize remaining open positions

        if random.random() < 0.1:  # Simulate 10% chance of closing a position
            closed_positions.labels(customer=customer,transaction='').inc()

        model_correctness.labels(customer=customer).set(random.uniform(0.8, 1.0))  # Random correctness between 80% and 100%
        latitude, longitude = get_coordinates(location)
        unique_logins.labels(customer=customer, location=location, latitude=latitude, longitude=longitude).inc()  # Increment unique logins

        # Simulate ERP service request
        response_status = simulate_erp_request()
        erp_http_responses.labels(status_code=str(response_status), customer=customer, endpoint="erp.com").inc()

        # Simulate validation duration
        with validation_duration.time():
            time.sleep(random.uniform(0.1, 0.5))  # Simulate validation taking between 100ms and 500ms

        if random.random() < 0.1:  # Simulate 10% validation failure rate
            validate_failed.labels(customer=customer, reason=reason).inc()
            raise Exception("Validation failed")
        else:
            validate_success.labels(customer=customer).inc()

        # Update system metrics
        cpu_percent = random.uniform(10, 90)  # Simulate CPU usage between 10% and 90%
        memory_percent = random.uniform(30, 80)  # Simulate memory usage between 30% and 80%
        network_bytes = random.uniform(1000, 10000)  # Simulate network throughput between 1KB/s and 10KB/s

        cpu_usage.set(cpu_percent)
        memory_usage.set(memory_percent)
        network_throughput.set(network_bytes)
    except Exception as e:
        logging.error(f"Error processing statement for {customer}: {e}")
    finally:
        latency.labels(customer=customer).observe(time.time() - start)

def get_coordinates(location):
    coordinates = {
        'US': (37.0902, -95.7129),
        'EU': (54.5260, 15.2551),
        'APAC': (-8.7832, 124.5085),
        'NA': (54.5260, -105.2551)
    }
    return coordinates.get(location, (0, 0))

def simulate_erp_request():
    # Simulate making a request to the ERP service and receiving a response
    if random.random() < 0.1:  # 10% chance of 500 error
        return 500
    else:
        return 200

if __name__ == "__main__":
    customers = ['companyA', 'companyB', 'companyC', 'companyD']
    reasons = ['invalid_data', 'open_positions_used_twice']
    locations = ['US', 'EU', 'APAC', 'NA']
    while True:
        customer = random.choice(customers)
        reason = random.choice(reasons)
        location = random.choice(locations)
        logging.info(f"Processing statement for {customer}... ")
        process_statement(customer, reason, location)
        time.sleep(0.5)  # Simulate two statements processed per second