#!/usr/bin/env python3
"""Test architecture patterns functionality."""

import asyncio
from mcp_app.azure_pricing_mcp_server.server import get_azure_patterns

async def test_architecture_patterns():
    """Test architecture patterns functionality."""
    print("Testing Azure architecture patterns...\n")
    
    # Test getting all patterns
    print("1. Testing all patterns retrieval...")
    all_patterns = await get_azure_patterns()
    
    print(f"Status: {all_patterns.get('status')}")
    print(f"Response size: {len(str(all_patterns))} characters")
    
    if all_patterns.get('status') == 'success':
        patterns = all_patterns.get('available_patterns', [])
        print(f"Total patterns: {all_patterns.get('total_patterns')}")
        print("Available patterns:")
        for pattern in patterns:
            print(f"  - {pattern['name']}: {pattern['estimated_cost']} ({pattern['components']} components)")
    
    # Test specific pattern
    print("\n2. Testing specific pattern retrieval...")
    specific_pattern = await get_azure_patterns("web-app-basic")
    
    print(f"Status: {specific_pattern.get('status')}")
    print(f"Response size: {len(str(specific_pattern))} characters")
    
    if specific_pattern.get('status') == 'success':
        print(f"Pattern: {specific_pattern.get('pattern_name')}")
        print(f"Description: {specific_pattern.get('description')}")
        print(f"Total cost: {specific_pattern.get('total_cost')}")
        print(f"Components: {len(specific_pattern.get('components', []))}")
        print(f"Use cases: {len(specific_pattern.get('use_cases', []))}")
        print(f"Optimization tips: {len(specific_pattern.get('optimization_tips', []))}")
    
    # Test microservices pattern
    print("\n3. Testing microservices pattern...")
    microservices = await get_azure_patterns("microservices")
    
    print(f"Status: {microservices.get('status')}")
    print(f"Response size: {len(str(microservices))} characters")
    
    if microservices.get('status') == 'success':
        print(f"Pattern: {microservices.get('pattern_name')}")
        print(f"Total cost: {microservices.get('total_cost')}")
        components = microservices.get('components', [])
        print("Components:")
        for comp in components:
            print(f"  - {comp['service']} ({comp['sku']}): {comp['monthly_cost']}")
    
    # Test serverless pattern
    print("\n4. Testing serverless pattern...")
    serverless = await get_azure_patterns("serverless")
    
    print(f"Status: {serverless.get('status')}")
    print(f"Response size: {len(str(serverless))} characters")
    
    if serverless.get('status') == 'success':
        print(f"Pattern: {serverless.get('pattern_name')}")
        print(f"Total cost: {serverless.get('total_cost')}")
        print("Optimization tips:")
        for tip in serverless.get('optimization_tips', []):
            print(f"  - {tip}")
    
    # Test error handling
    print("\n5. Testing error handling...")
    invalid_pattern = await get_azure_patterns("invalid-pattern")
    
    print(f"Status: {invalid_pattern.get('status')}")
    if invalid_pattern.get('status') == 'error':
        print(f"Error message: {invalid_pattern.get('message')}")
        print(f"Available patterns: {len(invalid_pattern.get('available_patterns', []))}")
    
    print("\n✅ Architecture patterns test completed!")

if __name__ == '__main__':
    asyncio.run(test_architecture_patterns())
