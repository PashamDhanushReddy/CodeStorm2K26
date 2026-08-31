from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import TeamRegistration
from django.conf import settings
import base64
import urllib.parse
import csv
import json
from datetime import datetime
import pandas as pd
from io import BytesIO

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'dashboard/login.html')

@login_required(login_url='login')
def update_selection_status_view(request):
    """
    API endpoint to update the selection status of a registration.
    Expects POST request with registration_id and selection_status.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        registration_id = data.get('registration_id')
        selection_status = data.get('selection_status')
        
        # Validate inputs
        if not registration_id or not selection_status:
            return JsonResponse({'error': 'registration_id and selection_status are required'}, status=400)
        
        # Validate selection status value
        valid_statuses = ['pending', 'selected', 'rejected', 'waitlisted']
        if selection_status not in valid_statuses:
            return JsonResponse({'error': f'Invalid selection_status. Must be one of: {", ".join(valid_statuses)}'}, status=400)
        
        # Update in PostgreSQL
        updated_count = TeamRegistration.objects.filter(id=registration_id).update(selection_status=selection_status)
        
        if updated_count > 0:
            return JsonResponse({
                'success': True,
                'message': 'Selection status updated successfully',
                'registration_id': registration_id,
                'new_status': selection_status
            })
        else:
            return JsonResponse({'error': 'Failed to update selection status'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def debug_storage_view(request):
    """Debug view to show what's in the Supabase storage bucket"""
    context = {
        'bucket_name': 'Disabled (PostgreSQL Migration)',
        'files': [],
        'error': 'Supabase storage is disabled.'
    }
    
    return render(request, 'dashboard/debug_storage.html', context)

@login_required(login_url='login')
def debug_fields_view(request):
    """Debug view to show actual database field names"""
    # Fetch just one registration to see field names
    registration = TeamRegistration.objects.all().values().first()
    
    context = {
        'registration': registration,
        'fields': list(registration.keys()) if registration else [],
        'sample_data': registration if registration else {}
    }
    
    return render(request, 'dashboard/debug_fields.html', context)

@login_required(login_url='login')
def dashboard_view(request):
    # Get filter parameters from request
    college_code_filter = request.GET.get('college_code', '')
    team_size_filter = request.GET.get('team_size', '')
    has_ppt_filter = request.GET.get('has_ppt', '')
    date_filter = request.GET.get('date', '')
    idea_theme_filter = request.GET.get('idea_theme', '')
    selection_status_filter = request.GET.get('selection_status', '')
    
    # Fetch all data from PostgreSQL
    registrations = list(TeamRegistration.objects.all().values())
    
    # Debug: Print available fields from first registration
    if registrations:
        print("=== DATABASE FIELD ANALYSIS ===")
        print("Available fields in registration:")
        for key, value in registrations[0].items():
            print(f"  {key}: {type(value).__name__}")
            if 'date' in key.lower() or 'time' in key.lower():
                print(f"    -> DATE/TIME FIELD FOUND: {key} = {value}")
        print(f"Total registrations: {len(registrations)}")
        print("=== END FIELD ANALYSIS ===")
    else:
        print("No registrations found")
    
    # Get all unique values for filter dropdowns from unfiltered data
    all_registrations = list(TeamRegistration.objects.all().values())
    
    # Initialize counters for t-shirt sizes and food preferences
    tshirt_counts = {'S': 0, 'M': 0, 'L': 0, 'XL': 0, 'XXL': 0, 'XXXL': 0}
    food_counts = {'veg': 0, 'nonveg': 0}
    
    # Process all registrations to get unique dropdown values and counts
    all_processed = []
    for reg in all_registrations:
        # Count team members (excluding empty ones)
        team_size = 0
        for i in range(1, 7):
            member_name = reg.get(f'member{i}_name')
            if member_name:
                team_size += 1
                # Count t-shirt sizes
                tshirt_size = reg.get(f'member{i}_tshirt_size', '').upper()
                if tshirt_size in tshirt_counts:
                    tshirt_counts[tshirt_size] += 1
                
                # Count food preferences
                food_pref = reg.get(f'member{i}_food_preference', '').lower()
                if 'veg' in food_pref and 'non' not in food_pref:
                    food_counts['veg'] += 1
                elif 'non' in food_pref and 'veg' in food_pref:
                    food_counts['nonveg'] += 1
        
        all_processed.append({
            'college_code': reg.get('member1_college_code') or reg.get('college_code', 'N/A'),
            'team_size': team_size,
            'idea_theme': reg.get('idea_theme', 'N/A'),
        })
    
    # Get unique values for dropdowns from all data
    all_college_codes = sorted(set(reg['college_code'] for reg in all_processed if reg['college_code'] != 'N/A'))
    
    # Team sizes should show all possible options (4, 5, 6 members)
    all_team_sizes = ['4', '5', '6']
    
    standard_themes = [
        'Generative AI & LLM Applications',
        'Smart Cities, IoT & Edge Computing',
        'Robotics, Drones & Autonomous Systems',
        'Green Tech & Energy Optimization',
        'Cybersecurity & Threat Intelligence',
        'Agritech & Rural Innovation',
        'HealthTech, MedAI & Diagnostics',
        'Transportation & Logistics (AI-Driven)',
        'FinTech, Blockchain & Digital Trust',
        'Open Innovation Challenge (Wildcard Track)'
    ]
    all_idea_themes = standard_themes
    
    # Process registrations to generate download links and essential data
    processed_registrations = []
    for reg in registrations:
        # Get standardized values with fallback column names
        idea_theme = reg.get('idea_theme') or reg.get('theme') or reg.get('Theme') or 'N/A'
        ppt_path = reg.get('ppt_file_path') or reg.get('payment_proof') or reg.get('proof') or reg.get('payment_screenshot') or ''
        has_ppt = bool(ppt_path)
        selection_status = reg.get('selection_status', 'pending')
        
        # Apply filters (Python-side)
        if has_ppt_filter == 'yes' and not has_ppt:
            continue
        if has_ppt_filter == 'no' and has_ppt:
            continue
            
        if idea_theme_filter and idea_theme_filter.lower() not in idea_theme.lower():
            continue
            
        if selection_status_filter and selection_status != selection_status_filter:
            continue
            
        if college_code_filter:
            cc = reg.get('college_code', '') or ''
            m1cc = reg.get('member1_college_code', '') or ''
            if college_code_filter.lower() not in cc.lower() and college_code_filter.lower() not in m1cc.lower():
                continue
        
        # Find team leader
        team_leader_name = None
        team_leader_email = None
        team_leader_phone = None
        team_leader_college = None
        team_leader_college_code = None
        
        # Check each member to find the leader
        for i in range(1, 7):
            if reg.get(f'is_leader{i}'):
                team_leader_name = reg.get(f'member{i}_name')
                team_leader_email = reg.get(f'member{i}_email')
                team_leader_phone = reg.get(f'member{i}_phone')
                team_leader_college = reg.get(f'member{i}_college') or reg.get(f'member{i}_college_name')
                team_leader_college_code = reg.get(f'member{i}_college_code')
                break
        
        # Count team members (excluding empty ones)
        team_size = 0
        team_members = []
        for i in range(1, 7):
            member_name = reg.get(f'member{i}_name')
            member_email = reg.get(f'member{i}_email')
            member_phone = reg.get(f'member{i}_phone')
            member_roll = reg.get(f'member{i}_roll')
            is_leader = reg.get(f'is_leader{i}', False)
            
            if member_name:
                team_size += 1
                # Fix: Use correct field name for course (course_name instead of course)
                course_field = f'member{i}_course_name'
                course_data = reg.get(course_field, 'N/A')
                print(f"DEBUG: {course_field} = {course_data}")
                
                team_members.append({
                    'name': member_name,
                    'email': member_email,
                    'phone': member_phone,
                    'roll': member_roll,
                    'gender': reg.get(f'member{i}_gender', 'N/A'),
                    'year': reg.get(f'member{i}_year', 'N/A'),
                    'college': reg.get(f'member{i}_college_name', 'N/A'),
                    'college_code': reg.get(f'member{i}_college_code', 'N/A'),
                    'course': course_data,
                    'tshirt_size': reg.get(f'member{i}_tshirt_size', 'N/A'),
                    'food_preference': reg.get(f'member{i}_food_preference', 'N/A'),
                    'is_leader': is_leader
                })
        
        # Apply team size filter if specified
        if team_size_filter and str(team_size) != team_size_filter:
            continue
        
        # Parse registration date
        registration_date = reg.get('registration_date', 'N/A')
        if registration_date != 'N/A' and registration_date:
            try:
                # Parse the ISO format date string
                registration_date = datetime.fromisoformat(registration_date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                registration_date = 'N/A'
        
        # Apply date filter
        if date_filter and registration_date != 'N/A':
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                if registration_date.date() != filter_date:
                    continue
            except ValueError:
                pass
        
        # Create essential admin data structure
        essential_data = {
            'id': reg.get('id'),
            'team_name': reg.get('team_name', 'N/A'),
            'team_leader_name': team_leader_name or 'N/A',
            'team_leader_email': team_leader_email or 'N/A',
            'team_leader_phone': team_leader_phone or 'N/A',
            'college_name': team_leader_college or reg.get('college') or reg.get('college_name', 'N/A'),
            'college_code': team_leader_college_code or reg.get('college_code', 'N/A'),
            'team_size': team_size,
            'registration_date': registration_date,
            'has_ppt': has_ppt,
            'idea_title': reg.get('idea_title', 'N/A'),
            'idea_theme': idea_theme,
            'youtube_link': reg.get('youtube_link', 'N/A'),
            'ppt_file_path': ppt_path,
            'selection_status': reg.get('selection_status', 'pending'),
            'transaction_id': reg.get('transaction_id', 'N/A'),
        }
        
        essential_data['team_members'] = team_members
        essential_data['team_members_json'] = json.dumps(team_members)
        
        # Process PPT download links
        if ppt_path:
            # Check if it's a Cloudinary URL (or any full URL)
            if ppt_path.startswith('http'):
                essential_data['download_url'] = ppt_path
                essential_data['download_filename'] = ppt_path.split('/')[-1]
            else:
                essential_data['download_error'] = "File storage (Supabase) is disabled." 
        else:
            essential_data['download_error'] = "No PPT file uploaded"
            
        processed_registrations.append(essential_data)
    
    # Get total count of all registrations from database (unfiltered)
    total_registrations = len(all_registrations) if all_registrations else 0
    
    context = {
        'registrations': processed_registrations,
        'filters': {
            'college_code': college_code_filter,
            'team_size': team_size_filter,
            'has_ppt': has_ppt_filter,
            'date': date_filter,
            'idea_theme': idea_theme_filter,
            'selection_status': selection_status_filter,
        },
        'college_codes': all_college_codes,
        'team_sizes': all_team_sizes,
        'idea_themes': all_idea_themes,
        'total_registrations': total_registrations,
        'tshirt_counts': tshirt_counts,
        'food_counts': food_counts,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def download_ppt_view(request, ppt_path):
    return HttpResponse("File downloads are disabled because Supabase was removed.", status=404)

@login_required(login_url='login')
def export_registrations_view(request):
    
    # Get filter parameters
    college_code_filter = request.GET.get('college_code', '')
    team_size_filter = request.GET.get('team_size', '')
    has_ppt_filter = request.GET.get('has_ppt', '')
    date_filter = request.GET.get('date', '')
    idea_theme_filter = request.GET.get('idea_theme', '')
    selection_status_filter = request.GET.get('selection_status', '')
    
    # Fetch all data from PostgreSQL
    registrations = list(TeamRegistration.objects.all().values())
    
    # Process data
    processed_data = []
    for reg in registrations:
        # Get standardized values with fallback column names
        idea_theme = reg.get('idea_theme') or reg.get('theme') or reg.get('Theme') or 'N/A'
        ppt_path = reg.get('ppt_file_path') or reg.get('payment_proof') or reg.get('proof') or reg.get('payment_screenshot') or ''
        has_ppt = bool(ppt_path)
        selection_status = reg.get('selection_status', 'pending')
        
        # Apply filters (Python-side)
        if has_ppt_filter == 'yes' and not has_ppt:
            continue
        if has_ppt_filter == 'no' and has_ppt:
            continue
            
        if idea_theme_filter and idea_theme_filter.lower() not in idea_theme.lower():
            continue
            
        if selection_status_filter and selection_status != selection_status_filter:
            continue
            
        if college_code_filter:
            cc = reg.get('college_code', '') or ''
            m1cc = reg.get('member1_college_code', '') or ''
            if college_code_filter.lower() not in cc.lower() and college_code_filter.lower() not in m1cc.lower():
                continue
                
        # Parse date for filtering
        reg_date_str = reg.get('registration_date', '')
        if date_filter and reg_date_str:
             try:
                 reg_date_obj = datetime.fromisoformat(reg_date_str.replace('Z', '+00:00')).date()
                 filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                 if reg_date_obj != filter_date:
                     continue
             except (ValueError, AttributeError):
                 pass
            
        # Find leader and collect detailed member information
        team_leader_name = 'N/A'
        team_leader_email = 'N/A'
        team_leader_phone = 'N/A'
        team_leader_college = 'N/A'
        team_leader_college_code = 'N/A'
        
        # Calculate team size and members string
        team_size = 0
        members_list = []
        detailed_members = []  # Store detailed member info for export
        
        for i in range(1, 7):
            name = reg.get(f'member{i}_name')
            email = reg.get(f'member{i}_email')
            phone = reg.get(f'member{i}_phone')
            roll = reg.get(f'member{i}_roll')
            is_leader = reg.get(f'is_leader{i}')
            
            if name:
                team_size += 1
                member_str = f"{name} ({roll})"
                if is_leader:
                    team_leader_name = name
                    team_leader_email = email
                    team_leader_phone = phone
                    team_leader_college = reg.get(f'member{i}_college')
                    team_leader_college_code = reg.get(f'member{i}_college_code')
                    member_str += " [LEADER]"
                members_list.append(member_str)
                
                # Store detailed member info
                detailed_members.append({
                    'name': name,
                    'email': email or 'N/A',
                    'phone': phone or 'N/A',
                    'roll': roll or 'N/A',
                    'is_leader': is_leader
                })
        
        if team_size_filter and str(team_size) != team_size_filter:
            continue
            
        processed_data.append({
            'Team Name': reg.get('team_name', 'N/A'),
            'Team Leader': team_leader_name,
            'Leader Email': team_leader_email,
            'Leader Phone': team_leader_phone,
            'College': team_leader_college or reg.get('college', 'N/A'),
            'College Code': team_leader_college_code or reg.get('college_code', 'N/A'),
            'Team Size': team_size,
            'Payment Status': selection_status,
            'Team Members': "; ".join(members_list),
            'Registration Date': reg.get('registration_date', 'N/A'),
            'Theme': idea_theme,
            'Idea Title': reg.get('idea_title', 'N/A'),
            'Payment Proof': ppt_path,
            'Detailed Members': detailed_members,  # Store detailed member info for modal
        })

    # Check export format
    export_format = request.GET.get('format', 'csv')
    
    if export_format == 'excel':
        # Create detailed DataFrame with individual member columns
        detailed_data = []
        for reg in processed_data:
            base_row = {
                'Team Name': reg['Team Name'],
                'Team Leader': reg['Team Leader'],
                'Leader Email': reg['Leader Email'],
                'Leader Phone': reg['Leader Phone'],
                'College': reg['College'],
                'College Code': reg['College Code'],
                'Team Size': reg['Team Size'],
                'Payment Status': reg['Payment Status'],
                'Registration Date': reg['Registration Date'],
                'Theme': reg['Theme'],
                'Idea Title': reg['Idea Title'],
                'Payment Proof': reg['Payment Proof'],
            }
            
            # Add individual member details
            if reg.get('Detailed Members'):
                for i, member in enumerate(reg['Detailed Members'], 1):
                    base_row[f'Member {i} Name'] = member['name']
                    base_row[f'Member {i} Roll No'] = member['roll']
                    base_row[f'Member {i} Email'] = member['email']
                    base_row[f'Member {i} Phone'] = member['phone']
                    base_row[f'Member {i} Role'] = 'Team Leader' if member['is_leader'] else 'Member'
            
            detailed_data.append(base_row)
        
        # Create DataFrame
        df = pd.DataFrame(detailed_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Detailed Registrations')
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Detailed Registrations']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(length + 2, 50)  # Cap at 50 chars
        
        output.seek(0)
        
        # Return Excel response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="codestorm_registrations_detailed.xlsx"'
        return response
    
    # Default to CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="codestorm_registrations_detailed.csv"'

    # Create detailed CSV with individual member columns
    detailed_data = []
    for reg in processed_data:
        base_row = {
            'Team Name': reg['Team Name'],
            'Team Leader': reg['Team Leader'],
            'Leader Email': reg['Leader Email'],
            'Leader Phone': reg['Leader Phone'],
            'College': reg['College'],
            'College Code': reg['College Code'],
            'Team Size': reg['Team Size'],
            'Payment Status': reg['Payment Status'],
            'Registration Date': reg['Registration Date'],
            'Theme': reg['Theme'],
            'Idea Title': reg['Idea Title'],
            'Payment Proof': reg['Payment Proof'],
        }
        
        # Add individual member details
        if reg.get('Detailed Members'):
            for i, member in enumerate(reg['Detailed Members'], 1):
                base_row[f'Member {i} Name'] = member['name']
                base_row[f'Member {i} Roll No'] = member['roll']
                base_row[f'Member {i} Email'] = member['email']
                base_row[f'Member {i} Phone'] = member['phone']
                base_row[f'Member {i} Role'] = 'Team Leader' if member['is_leader'] else 'Member'
        
        detailed_data.append(base_row)

    # Get all fieldnames from the first row (all possible columns)
    fieldnames = list(detailed_data[0].keys()) if detailed_data else []

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for row in detailed_data:
        writer.writerow(row)
        
    return response

@login_required(login_url='login')
def export_team_data_view(request):
    """
    Export team data grouped by college code with transaction IDs.
    This view executes the SQL query to aggregate team registrations by college.
    """
    registrations = list(TeamRegistration.objects.all().values())
    
    # Process data to match the SQL query logic
    team_data = []
    for reg in registrations:
        # Find the leader to get college information
        college_name = None
        college_code = None
        
        for i in range(1, 7):
            if reg.get(f'is_leader{i}'):
                college_name = reg.get(f'member{i}_college_name') or reg.get(f'member{i}_college')
                college_code = reg.get(f'member{i}_college_code')
                break
        
        # Fallback to first member or general fields if no leader found
        if not college_code:
            college_code = reg.get('member1_college_code') or reg.get('college_code', 'N/A')
        if not college_name:
            college_name = reg.get('member1_college_name') or reg.get('college_name') or reg.get('college', 'N/A')
        
        transaction_id = reg.get('transaction_id', 'N/A')
        
        team_data.append({
            'college_code': college_code,
            'college_name': college_name,
            'transaction_id': transaction_id
        })
    
    # Group by college_code
    from collections import defaultdict
    college_groups = defaultdict(lambda: {'college_names': set(), 'transaction_ids': [], 'count': 0})
    
    for team in team_data:
        code = team['college_code']
        college_groups[code]['college_names'].add(team['college_name'])
        college_groups[code]['transaction_ids'].append(team['transaction_id'])
        college_groups[code]['count'] += 1
    
    # Prepare data for Excel export
    export_data = []
    for college_code in sorted(college_groups.keys()):
        data = college_groups[college_code]
        export_data.append({
            'College Code': college_code,
            'College Names': ' | '.join(sorted(data['college_names'])),
            'No of Teams Registered': data['count'],
            'Transaction IDs': ', '.join(data['transaction_ids'])
        })
    
    # Create DataFrame
    df = pd.DataFrame(export_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Team Data by College')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Team Data by College']
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(length + 2, 80)
    
    output.seek(0)
    
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="team_data_by_college.xlsx"'
    return response
