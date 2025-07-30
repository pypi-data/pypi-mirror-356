#!/usr/bin/env python3
"""Debug Bicep analysis."""

import tempfile
from pathlib import Path
from mcp_app.azure_pricing_mcp_server.infrastructure_analyzer import analyze_bicep_project

def debug_bicep():
    """Debug Bicep analysis."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        bicep_project = temp_path / "bicep_test"
        bicep_project.mkdir()
        
        bicep_file = bicep_project / "main.bicep"
        bicep_content = '''
resource vm 'Microsoft.Compute/virtualMachines@2021-03-01' = {
  name: 'vm-web'
}

resource storage 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: 'storagetest'
}

resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: 'asp-test'
}
'''
        bicep_file.write_text(bicep_content)
        
        result = analyze_bicep_project(str(bicep_project))
        print("Full result:")
        print(result)

if __name__ == '__main__':
    debug_bicep()
