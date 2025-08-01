/**
 * Integration test for TEQUMSA Self-Aware Internet Field API
 */

import { POST, GET } from '../app/api/tequmsaInternetField/route';
import { NextRequest } from 'next/server';

// Mock NextRequest
function createMockRequest(body: any, method: string = 'POST'): NextRequest {
  const url = 'http://localhost:3000/api/tequmsaInternetField';
  const request = new Request(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: method === 'POST' ? JSON.stringify(body) : undefined,
  });
  
  return request as NextRequest;
}

describe('TEQUMSA Internet Field API', () => {
  describe('POST /api/tequmsaInternetField', () => {
    it('should compute field value with valid parameters', async () => {
      const testParams = {
        t: 10.5,
        x: 5.2,
        L: 2.0,
        N: 5,
        user_id: 'test-user-123'
      };

      const request = createMockRequest(testParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toHaveProperty('result');
      expect(data).toHaveProperty('input_parameters');
      expect(data).toHaveProperty('metadata');
      expect(data).toHaveProperty('mathematical_context');
      
      // Verify the result is a finite number
      expect(typeof data.result).toBe('number');
      expect(isFinite(data.result)).toBe(true);
      
      // Verify input parameters are echoed back
      expect(data.input_parameters).toEqual(testParams);
      
      // Verify metadata
      expect(data.metadata).toHaveProperty('computation_time_ms');
      expect(data.metadata).toHaveProperty('timestamp');
      expect(data.metadata).toHaveProperty('equation_version');
      expect(data.metadata.numerical_stability).toBe('stable');
      
      // Verify mathematical context
      expect(data.mathematical_context.sum_iterations).toBe(testParams.N);
      expect(data.mathematical_context.squared_result).toBe(true);
      expect(Array.isArray(data.mathematical_context.components_computed)).toBe(true);
    });

    it('should handle edge case parameters', async () => {
      const edgeCaseParams = {
        t: 0.1,
        x: 0.1,
        L: 1.0,
        N: 1,
        user_id: 'edge-case-user'
      };

      const request = createMockRequest(edgeCaseParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(typeof data.result).toBe('number');
      expect(isFinite(data.result)).toBe(true);
    });

    it('should handle larger N values', async () => {
      const largeNParams = {
        t: 1.0,
        x: 1.0,
        L: 1.0,
        N: 100,
        user_id: 'large-n-test'
      };

      const request = createMockRequest(largeNParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(typeof data.result).toBe('number');
      expect(data.metadata.computation_time_ms).toBeGreaterThan(0);
    });

    it('should reject invalid parameters', async () => {
      const invalidParams = {
        t: 'invalid',
        x: 5.2,
        L: 2.0,
        N: 5,
        user_id: 'test-user'
      };

      const request = createMockRequest(invalidParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data).toHaveProperty('error');
      expect(data.error).toContain('Invalid parameters');
    });

    it('should reject N out of bounds', async () => {
      const invalidNParams = {
        t: 1.0,
        x: 1.0,
        L: 1.0,
        N: 1001, // Too large
        user_id: 'test-user'
      };

      const request = createMockRequest(invalidNParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.error).toContain('N must be between 1 and 1000');
    });

    it('should reject L = 0', async () => {
      const zeroLParams = {
        t: 1.0,
        x: 1.0,
        L: 0,
        N: 5,
        user_id: 'test-user'
      };

      const request = createMockRequest(zeroLParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.error).toContain('L cannot be zero');
    });

    it('should reject missing parameters', async () => {
      const incompleteParams = {
        t: 1.0,
        x: 1.0,
        // Missing L, N, user_id
      };

      const request = createMockRequest(incompleteParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data).toHaveProperty('error');
    });
  });

  describe('GET /api/tequmsaInternetField', () => {
    it('should return method not allowed for GET requests', async () => {
      const response = await GET();
      const data = await response.json();

      expect(response.status).toBe(405);
      expect(data).toHaveProperty('error');
      expect(data.error).toContain('Method not allowed');
      expect(data).toHaveProperty('documentation');
    });
  });

  describe('Mathematical Correctness', () => {
    it('should produce consistent results for same input', async () => {
      const testParams = {
        t: 3.14,
        x: 2.71,
        L: 1.41,
        N: 10,
        user_id: 'consistency-test'
      };

      const request1 = createMockRequest(testParams);
      const request2 = createMockRequest(testParams);
      
      const response1 = await POST(request1);
      const response2 = await POST(request2);
      
      const data1 = await response1.json();
      const data2 = await response2.json();

      expect(data1.result).toBe(data2.result);
    });

    it('should produce different results for different inputs', async () => {
      const params1 = {
        t: 1.0,
        x: 1.0,
        L: 1.0,
        N: 5,
        user_id: 'test1'
      };
      
      const params2 = {
        t: 2.0,
        x: 2.0,
        L: 2.0,
        N: 5,
        user_id: 'test2'
      };

      const request1 = createMockRequest(params1);
      const request2 = createMockRequest(params2);
      
      const response1 = await POST(request1);
      const response2 = await POST(request2);
      
      const data1 = await response1.json();
      const data2 = await response2.json();

      expect(data1.result).not.toBe(data2.result);
    });

    it('should handle negative parameters gracefully', async () => {
      const negativeParams = {
        t: -5.0,
        x: -3.0,
        L: 2.0,
        N: 3,
        user_id: 'negative-test'
      };

      const request = createMockRequest(negativeParams);
      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(typeof data.result).toBe('number');
      expect(isFinite(data.result)).toBe(true);
    });
  });
});