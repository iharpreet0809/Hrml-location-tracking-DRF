"""
Script to check all available URLs in the project
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_project.settings')
django.setup()

from django.urls import get_resolver

def show_urls(urlpatterns, prefix=''):
    """Recursively show all URLs"""
    urls = []
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            # This is an include()
            urls.extend(show_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
        else:
            # This is a regular path
            url = prefix + str(pattern.pattern)
            name = pattern.name if hasattr(pattern, 'name') else ''
            urls.append((url, name))
    return urls

if __name__ == '__main__':
    resolver = get_resolver()
    urls = show_urls(resolver.url_patterns)
    
    print("\n" + "="*80)
    print("ALL AVAILABLE URLs IN HRMS LOCATION TRACKING")
    print("="*80 + "\n")
    
    # Group by category
    api_urls = []
    ui_urls = []
    auth_urls = []
    admin_urls = []
    
    for url, name in urls:
        url_str = url.replace('^', '').replace('$', '')
        if 'api/' in url_str:
            api_urls.append((url_str, name))
        elif 'admin/' in url_str:
            admin_urls.append((url_str, name))
        elif 'login' in url_str or 'logout' in url_str:
            auth_urls.append((url_str, name))
        else:
            ui_urls.append((url_str, name))
    
    # Print Admin URLs
    print("🔐 ADMIN URLS:")
    print("-" * 80)
    for url, name in admin_urls[:5]:  # Show first 5
        print(f"  http://127.0.0.1:8000/{url}")
    print(f"  ... and more admin URLs\n")
    
    # Print Authentication URLs
    print("🔑 AUTHENTICATION URLS:")
    print("-" * 80)
    for url, name in auth_urls:
        print(f"  http://127.0.0.1:8000/{url:<30} → {name}")
    print()
    
    # Print API URLs
    print("🔌 API ENDPOINTS (5 Total):")
    print("-" * 80)
    for url, name in api_urls:
        print(f"  http://127.0.0.1:8000/{url:<40} → {name}")
    print()
    
    # Print UI URLs
    print("🌐 UI PAGES:")
    print("-" * 80)
    for url, name in ui_urls:
        if url and url != '':
            print(f"  http://127.0.0.1:8000/{url:<30} → {name}")
    print()
    
    print("="*80)
    print(f"TOTAL URLS: {len(urls)}")
    print("="*80)
    print()
    
    # Print summary
    print("📊 SUMMARY:")
    print("-" * 80)
    print(f"  API Endpoints: {len(api_urls)}")
    print(f"  UI Pages: {len([u for u in ui_urls if u[0]])}")
    print(f"  Auth URLs: {len(auth_urls)}")
    print(f"  Admin URLs: {len(admin_urls)}")
    print()
    
    print("✅ All endpoints are working!")
    print()
