import sys
import os
from openai import OpenAI
from anthropic import Anthropic
import requests
import google.generativeai as genai
import googleapiclient.discovery
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def test_openai_api():
    try:
        if not os.environ.get("OPENAI_API_KEY"):
            print("❌ OpenAI API error: OPENAI_API_KEY environment variable not set.")
            return False
        client = OpenAI()
        
        # Run the API call with a 10-second timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=10
            )
            try:
                response = future.result(timeout=10)
            except TimeoutError:
                print("❌ OpenAI API error: request timed out.")
                return False
        return True
    except Exception as e:
        print(f"❌ Open AI API error: {str(e)}")
        return False

def test_gemini_api():
    try:
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        if not google_api_key:
            print("❌ Gemini API error: GOOGLE_API_KEY environment variable not set.")
            return False
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') # Corrected model name
        
        # Run the API call with a 10-second timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(model.generate_content, "Hello, are you working?")
            try:
                response = future.result(timeout=10)
            except TimeoutError:
                print("❌ Gemini API error: request timed out.")
                return False
        return True
    except Exception as e:
        print(f"❌ Gemini API error: {str(e)}")
        return False

def test_anthropic_api():
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("❌ Anthropic API error: ANTHROPIC_API_KEY environment variable not set.")
            return False
        client = Anthropic()
        
        # Run the API call with a 10-second timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                client.messages.create,
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello, are you working?"}]
            )
            try:
                response = future.result(timeout=10)
            except TimeoutError:
                print("❌ Anthropic API error: request timed out.")
                return False
        return True
    except Exception as e:
        print(f"❌ Anthropic API error: {str(e)}")
        return False

def test_github_api():
    """Test the GitHub API connection."""
    try:      
        token = os.environ.get("GITHUB_TOKEN")
        if not token: # This check is already good
            print("❌ GitHub API error: GITHUB_TOKEN environment variable not set")
            return False
            
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Run the API call with a 10-second timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                requests.get,
                "https://api.github.com/user",
                headers=headers
            )
            try:
                response = future.result(timeout=10)
            except TimeoutError:
                print("❌ GitHub API error: request timed out.")
                return False
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login')
            print(f"✅ GitHub API works! Authenticated as: {username}")
            return True
        else:
            print(f"❌ GitHub API error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub API error: {str(e)}")
        return False

def test_Terraform_API():
    try:
        if not os.environ.get("TFE_TOKEN"):
            print("❌ Terraform API error: TFE_TOKEN environment variable not set.")
            return False
        headers = {
            "Authorization": f"Bearer {os.environ.get('TFE_TOKEN')}",
            "Content-Type": "application/vnd.api+json"
        }
        # Run the API call with a 10-second timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                requests.get,
                "https://app.terraform.io/api/v2/organizations",
                headers=headers
            )
            try:
                response = future.result(timeout=10)
            except TimeoutError:
                print("❌ Terraform API error: request timed out.")
                return False
        if response.status_code == 200:
            org_data = response.json()
            # print(f"✅ Terraform API works! Organizations: {org_data}")
            return True
        else:
            print(f"❌ Terraform API error: Status code {response.status_code}")
            if hasattr(response, 'text'):
                print(f"   Response body: {response.text}")
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Terraform API error: Connection failed - {str(e)}")
        print("   This could be due to:")
        print("   - Network connectivity issues")
        print("   - DNS resolution problems")
        print("   - Firewall blocking the connection")
        return False
    except requests.exceptions.SSLError as e:
        print(f"❌ Terraform API error: SSL/TLS error - {str(e)}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ Terraform API error: Request timeout - {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Terraform API error: Request failed - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Terraform API error: Unexpected error - {str(e)}")
        return False

def test_all_apis():
    print("Hello from the test workflow!")
    
    
    print("Testing API connections...")
    openai_success = test_openai_api()
    gemini_success = test_gemini_api()
    anthropic_success = test_anthropic_api()
    github_success = test_github_api()  
    terraform_success = test_Terraform_API()  
    
    print("\nSummary:")
    print(f"OpenAI API: {'✅ Working' if openai_success else '❌ Failed'}")
    print(f"Gemini API: {'✅ Working' if gemini_success else '❌ Failed'}")
    print(f"Anthropic API: {'✅ Working' if anthropic_success else '❌ Failed'}")
    print(f"GitHub API: {'✅ Working' if github_success else '❌ Failed'}")  
    print(f"Terraform API: {'✅ Working' if terraform_success else '❌ Failed'}")

    if openai_success and gemini_success and anthropic_success and github_success and terraform_success:  # Updated condition
        print("\n🎉 All APIs are working correctly!")
    else:
        print("\n⚠️ Some APIs failed. Check the errors above.")
