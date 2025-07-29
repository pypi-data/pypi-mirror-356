#!/usr/bin/env python3
"""
Test script to validate DevOps-in-a-Box R2D functionality
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def test_r2d_cli():
    """Test the R2D CLI functionality"""
    print("🧪 Testing DevOps-in-a-Box R2D CLI...")
    
    # Test 1: Import and basic functionality
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from diagram_to_iac.r2d import main
        print("✅ R2D CLI module imports successfully")
    except ImportError as e:
        print(f"❌ Failed to import R2D CLI: {e}")
        return False
    
    # Test 2: Help command
    try:
        result = subprocess.run([
            sys.executable, "-m", "diagram_to_iac.r2d", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print("✅ R2D CLI help command works")
        else:
            print(f"❌ R2D CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run R2D CLI help: {e}")
        return False
    
    # Test 3: Version command
    try:
        result = subprocess.run([
            sys.executable, "-m", "diagram_to_iac.r2d", "--version"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print(f"✅ R2D CLI version: {result.stdout.strip()}")
        else:
            print(f"❌ R2D CLI version failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run R2D CLI version: {e}")
        return False
    
    return True

def test_container_build():
    """Test container build locally"""
    print("\n🐳 Testing DevOps-in-a-Box Container Build...")
    
    dockerfile_path = Path(__file__).parent.parent / ".github/actions/r2d/Dockerfile"
    
    if not dockerfile_path.exists():
        print(f"❌ Dockerfile not found at {dockerfile_path}")
        return False
    
    print("✅ Dockerfile exists")
    
    # Check if Docker is available
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker available: {result.stdout.strip()}")
        else:
            print("⚠️ Docker not available - skipping container build test")
            return True
    except FileNotFoundError:
        print("⚠️ Docker not installed - skipping container build test")
        return True
    
    # Test container build (dry run)
    try:
        print("🔨 Testing container build (this may take a few minutes)...")
        result = subprocess.run([
            "docker", "build", 
            "-t", "diagram-to-iac-r2d:test",
            "-f", str(dockerfile_path),
            ".",
            "--build-arg", "PACKAGE_VERSION=test"
        ], capture_output=True, text=True, cwd=dockerfile_path.parent)
        
        if result.returncode == 0:
            print("✅ Container builds successfully")
            
            # Test container run
            test_result = subprocess.run([
                "docker", "run", "--rm",
                "diagram-to-iac-r2d:test",
                "--help"
            ], capture_output=True, text=True)
            
            if test_result.returncode == 0:
                print("✅ Container runs successfully")
            else:
                print(f"⚠️ Container run test failed: {test_result.stderr}")
            
            # Clean up
            subprocess.run(["docker", "rmi", "diagram-to-iac-r2d:test"], capture_output=True)
            
        else:
            print(f"❌ Container build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Container build test failed: {e}")
        return False
    
    return True

def test_github_action_definition():
    """Test GitHub Action definition"""
    print("\n🎬 Testing GitHub Action Definition...")
    
    action_path = Path(__file__).parent.parent / ".github/actions/r2d/action.yml"
    
    if not action_path.exists():
        print(f"❌ action.yml not found at {action_path}")
        return False
    
    try:
        # PyYAML is a runtime dependency, so it should already be available
        import yaml
        
        with open(action_path, 'r') as f:
            action_config = yaml.safe_load(f)
        
        # Validate required fields
        required_fields = ['name', 'description', 'inputs', 'outputs', 'runs']
        for field in required_fields:
            if field not in action_config:
                print(f"❌ Missing required field in action.yml: {field}")
                return False
        
        print("✅ action.yml has all required fields")
        
        # Check branding
        if 'branding' in action_config:
            print("✅ action.yml includes branding")
        
        # Check inputs
        required_inputs = ['repo']
        for input_name in required_inputs:
            if input_name not in action_config['inputs']:
                print(f"❌ Missing required input: {input_name}")
                return False
        
        print("✅ action.yml has all required inputs")
        
        # Check if using Dockerfile or published image
        runs_config = action_config['runs']
        if runs_config.get('using') == 'docker':
            image = runs_config.get('image', '')
            if image == 'Dockerfile':
                print("ℹ️ Action uses local Dockerfile (development mode)")
            elif image.startswith('docker://'):
                print(f"✅ Action uses published image: {image}")
            else:
                print(f"⚠️ Unexpected image configuration: {image}")
        
    except Exception as e:
        print(f"❌ Failed to validate action.yml: {e}")
        return False
    
    return True

def test_workflow_definition():
    """Test GitHub workflow definition"""
    print("\n⚙️ Testing GitHub Workflow Definition...")
    
    workflow_path = Path(__file__).parent.parent / ".github/workflows/diagram-to-iac-build.yml"
    
    if not workflow_path.exists():
        print(f"❌ workflow file not found at {workflow_path}")
        return False
    
    try:
        import yaml
        
        with open(workflow_path, 'r') as f:
            content = f.read()
            
        # Parse YAML content, handling the comment properly
        try:
            # First try parsing as-is (in case there's no comment)
            workflow_config = yaml.safe_load(content)
        except yaml.YAMLError:
            # If that fails, try removing the first line if it's a comment
            lines = content.split('\n')
            if lines and lines[0].strip().startswith('#'):
                yaml_content = '\n'.join(lines[1:])
                workflow_config = yaml.safe_load(yaml_content)
            else:
                raise
        
        # Validate required fields
        # Note: GitHub Actions uses 'on' as a trigger key, but PyYAML may parse it as boolean True
        required_fields = ['name', 'jobs']
        trigger_field = 'on'  # Look for 'on' key
        
        for field in required_fields:
            if field not in workflow_config:
                print(f"❌ Missing required field in workflow: {field}")
                return False
        
        # Check for trigger field ('on' or boolean True)
        has_trigger = False
        if 'on' in workflow_config:
            has_trigger = True
            print("✅ Workflow has 'on' trigger field")
        elif True in workflow_config:
            has_trigger = True
            print("✅ Workflow has trigger field (parsed as boolean)")
            # PyYAML converts 'on:' to boolean True, this is normal
        
        if not has_trigger:
            print("❌ Missing trigger field ('on') in workflow")
            return False
        
        print("✅ Workflow has all required fields")
        
        # Check jobs
        jobs = workflow_config['jobs']
        expected_jobs = ['publish-python-package', 'build-r2d-container']
        for job_name in expected_jobs:
            if job_name not in jobs:
                print(f"❌ Missing expected job: {job_name}")
                return False
        
        print("✅ Workflow has all expected jobs")
        
        # Check permissions
        r2d_job = jobs['build-r2d-container']
        if 'permissions' in r2d_job:
            permissions = r2d_job['permissions']
            if permissions.get('contents') == 'write':
                print("✅ R2D container job has write permissions")
            else:
                print("⚠️ R2D container job may not have sufficient permissions")
        
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error in workflow: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to validate workflow: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 DevOps-in-a-Box System Validation")
    print("=" * 50)
    
    tests = [
        ("R2D CLI", test_r2d_cli),
        ("Container Build", test_container_build),
        ("GitHub Action", test_github_action_definition),
        ("GitHub Workflow", test_workflow_definition),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! DevOps-in-a-Box is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
