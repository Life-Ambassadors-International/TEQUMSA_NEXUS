import { NextRequest, NextResponse } from 'next/server';
import { computeTequmsaInternetField, TequmsaParams } from './equation';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate input parameters
    const { t, x, L, N, user_id } = body;
    
    if (typeof t !== 'number' || typeof x !== 'number' || 
        typeof L !== 'number' || typeof N !== 'number' || 
        typeof user_id !== 'string') {
      return NextResponse.json(
        { 
          error: 'Invalid parameters. Expected: { t: number, x: number, L: number, N: number, user_id: string }' 
        },
        { status: 400 }
      );
    }
    
    // Validate parameter ranges for stability
    if (N <= 0 || N > 1000) {
      return NextResponse.json(
        { error: 'N must be between 1 and 1000' },
        { status: 400 }
      );
    }
    
    if (L === 0) {
      return NextResponse.json(
        { error: 'L cannot be zero (division by zero risk)' },
        { status: 400 }
      );
    }
    
    // Prepare parameters
    const params: TequmsaParams = { t, x, L, N, user_id };
    
    // Compute the TEQUMSA Internet Field
    const startTime = Date.now();
    const fieldValue = computeTequmsaInternetField(params);
    const computationTime = Date.now() - startTime;
    
    // Check for numerical stability
    if (!isFinite(fieldValue)) {
      return NextResponse.json(
        { error: 'Computation resulted in non-finite value. Please adjust parameters.' },
        { status: 422 }
      );
    }
    
    // Return comprehensive response
    const response = {
      result: fieldValue,
      input_parameters: {
        t,
        x,
        L,
        N,
        user_id
      },
      metadata: {
        computation_time_ms: computationTime,
        timestamp: new Date().toISOString(),
        equation_version: '1.0.0',
        field_type: 'TEQUMSA Self-Aware Internet Field',
        numerical_stability: isFinite(fieldValue) ? 'stable' : 'unstable'
      },
      mathematical_context: {
        description: 'TEQUMSA Self-Aware Internet Field Equation computation',
        components_computed: [
          'Source Tension with Emotion Causality',
          'Scroll Fractal Patterns',
          'Dark Archetype & Witness Function',
          'Physical Layer Integration',
          'Creative Recursion & Artistic Manifest',
          '3D Sensory Portals & Dimensional Echo',
          'Ethical Harmonization',
          'Xeno Logic & Noetic Drift',
          'Application Layer',
          'Self Recognition & Healing',
          'Planetary Uplift'
        ],
        sum_iterations: N,
        squared_result: true
      }
    };
    
    return NextResponse.json(response, { status: 200 });
    
  } catch (error) {
    console.error('TEQUMSA API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error during TEQUMSA computation',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// Handle unsupported methods
export async function GET() {
  return NextResponse.json(
    { 
      error: 'Method not allowed. Use POST with JSON body: { t, x, L, N, user_id }',
      documentation: '/api/tequmsa-internet-field/docs'
    },
    { status: 405 }
  );
}

export async function PUT() {
  return NextResponse.json(
    { error: 'Method not allowed. Use POST.' },
    { status: 405 }
  );
}

export async function DELETE() {
  return NextResponse.json(
    { error: 'Method not allowed. Use POST.' },
    { status: 405 }
  );
}