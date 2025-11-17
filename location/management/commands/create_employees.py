"""
Management command to create 10 employees with username emp01-emp10 and password 'employee'
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates 10 employees (emp01-emp10) with password "employee"'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating 10 employees...'))
        
        created_count = 0
        existing_count = 0
        
        for i in range(1, 11):
            username = f'emp{i:02d}'  # emp01, emp02, ..., emp10
            email = f'{username}@company.com'
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'  ⚠️  {username} already exists'))
                existing_count += 1
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='employee',
                first_name=f'Employee',
                last_name=f'{i:02d}'
            )
            
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created {username} (password: employee)'))
            created_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count} employees'))
        if existing_count > 0:
            self.stdout.write(self.style.WARNING(f'  Already existed: {existing_count} employees'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Login credentials:'))
        self.stdout.write(self.style.SUCCESS('  Username: emp01, emp02, ..., emp10'))
        self.stdout.write(self.style.SUCCESS('  Password: employee'))
        self.stdout.write('')
