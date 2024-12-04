import {
  ConsecutiveBreaker,
  ExponentialBackoff,
  retry,
  handleAll,
  circuitBreaker,
  wrap,
  CircuitBreakerPolicy,
  RetryPolicy,
  
} from 'cockatiel';


// IMergedPolicy<IRetryContext & IDefaultPolicyContext, never, [RetryPolicy, CircuitBreakerPolicy]>

/**
 * 
 * @returns {import('cockatiel').IMergedPolicy<import('cockatiel').IRetryContext & import('cockatiel').IDefaultPolicyContext, never, [RetryPolicy, CircuitBreakerPolicy]>} 
 */
function newBreaker() {
  // Create a retry policy that'll try whatever function we execute 3
  // times with a randomized exponential backoff.
  const retryPolicy = retry(handleAll, { maxAttempts: 3, backoff: new ExponentialBackoff() });

  // Create a circuit breaker that'll stop calling the executed function for 10
  // seconds if it fails 5 times in a row. This can give time for e.g. a database
  // to recover without getting tons of traffic.
  const circuitBreakerPolicy = circuitBreaker(handleAll, {
    halfOpenAfter: 10 * 1000,
    breaker: new ConsecutiveBreaker(5),
  });

  // Combine these! Create a policy that retries 3 times, calling through the circuit breaker
  const retryWithBreaker = wrap(retryPolicy, circuitBreakerPolicy);
  retryWithBreaker.onFailure((error, context) => {
    console.error('Error:', error);
  });
  return retryWithBreaker
}

export { newBreaker }