from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import requests
import uuid
import os
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .forms import TeamRegistrationForm
from .models import TeamRegistration
from django.db import IntegrityError

# Initialize Cloudinary
cloudinary.config( 
  cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'], 
  api_key = settings.CLOUDINARY_STORAGE['API_KEY'], 
  api_secret = settings.CLOUDINARY_STORAGE['API_SECRET'],
  secure = True
)

def upload_ppt_to_cloudinary(ppt_file, team_name):
    """Upload PPT file to Cloudinary"""
    try:
        unique_filename = f"{team_name.replace(' ', '_')}_{uuid.uuid4()}"
        print(f"Uploading PPT to Cloudinary: {unique_filename}")
        response = cloudinary.uploader.upload(
            ppt_file, 
            public_id=unique_filename,
            folder="ppt_submissions",
            resource_type="auto"
        )
        print(f"Cloudinary upload success. URL: {response.get('secure_url')}")
        return response.get('secure_url')
    except Exception as e:
        print(f"Error uploading PPT to Cloudinary: {str(e)}")
        return None

def register_team(request):
    """Handle team registration"""
    preserved_file_info = None
    if request.method == 'POST':
        # Debug CSRF token
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        print(f"=== CSRF DEBUG ===")
        print(f"CSRF token in POST: {csrf_token[:20] if csrf_token else 'MISSING'}...")
        print(f"CSRF cookie: {request.COOKIES.get('csrftoken', 'MISSING')[:20] if request.COOKIES.get('csrftoken') else 'MISSING'}...")
        print(f"==================")
        
        form = TeamRegistrationForm(request.POST, request.FILES)
        
        # Handle file persistence for validation errors
        preserved_file_info = None
        if request.method == 'POST' and request.FILES.get('payment_screenshot'):
            # Store file temporarily on server for persistence across validation errors
            uploaded_file = request.FILES['payment_screenshot']
            import tempfile
            import os
            
            # Create a temporary file to store the uploaded file
            temp_dir = tempfile.gettempdir()
            temp_filename = f"codestorm_payment_{uuid.uuid4()}_{uploaded_file.name}"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            try:
                # Write the uploaded file to temporary storage
                with open(temp_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Store file info in session for persistence across validation errors
                request.session['preserved_payment_screenshot'] = {
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'content_type': uploaded_file.content_type,
                    'temp_path': temp_path,
                    'uploaded': True
                }
                preserved_file_info = request.session['preserved_payment_screenshot']
                print(f"=== FILE SAVED TO TEMP: {temp_path} ===")
                
            except Exception as e:
                print(f"Error storing temporary file: {str(e)}")
                # Continue without file preservation if storage fails
                
        elif request.session.get('preserved_payment_screenshot'):
            preserved_file_info = request.session['preserved_payment_screenshot']
        
        # Debug: Print form errors if validation fails
        if not form.is_valid():
            print(f"=== FORM VALIDATION ERRORS ===")
            print(f"Form errors: {form.errors}")
            print(f"Non-field errors: {form.non_field_errors()}")
            for field, errors in form.errors.items():
                print(f"Field '{field}': {errors}")
            # Print some key form data for debugging
            print(f"Team size: {request.POST.get('team_size', 'NOT SET')}")
            print(f"Leader checkboxes: is_leader1={request.POST.get('is_leader1')}, is_leader2={request.POST.get('is_leader2')}, is_leader3={request.POST.get('is_leader3')}, is_leader4={request.POST.get('is_leader4')}")
            for i in range(1, 5):
                gender = request.POST.get(f'member{i}_gender', 'NOT SET')
                name = request.POST.get(f'member{i}_name', 'NOT SET')
                print(f"Member {i}: name={name[:20] if name != 'NOT SET' else 'NOT SET'}, gender={gender}")
            print(f"=============================")
            # Add error messages to be displayed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
        
        if form.is_valid():
            try:
                team_name = form.cleaned_data['team_name']
                team_size = int(form.cleaned_data.get('team_size', '4'))
                
                # Calculate fee with discount
                base_fee_per_person = 600
                discount_eligible = form.cleaned_data.get('_discount_eligible', False)
                discount_percentage = 0.10 if discount_eligible else 0
                
                total_base_fee = base_fee_per_person * team_size
                discount_amount = total_base_fee * discount_percentage
                total_fee = total_base_fee - discount_amount
                
                # Handle payment screenshot
                payment_screenshot_url = ''
                payment_screenshot_path = None
                # Use the already-saved temp file (written to disk when POST came in)
                if preserved_file_info and 'temp_path' in preserved_file_info:
                    payment_screenshot_path = preserved_file_info['temp_path']
                    print(f"Using preserved file at: {payment_screenshot_path}")
                
                # Find the team leader to get default values
                leader_data = None
                if form.cleaned_data.get('is_leader1'):
                    leader_data = {
                        'college_name': form.cleaned_data['member1_college_name'],
                        'course_name': form.cleaned_data['member1_course_name'],
                        'year': form.cleaned_data['member1_year']
                    }
                elif form.cleaned_data.get('is_leader2'):
                    leader_data = {
                        'college_name': form.cleaned_data['member2_college_name'],
                        'course_name': form.cleaned_data['member2_course_name'],
                        'year': form.cleaned_data['member2_year']
                    }
                elif form.cleaned_data.get('is_leader3'):
                    leader_data = {
                        'college_name': form.cleaned_data['member3_college_name'],
                        'course_name': form.cleaned_data['member3_course_name'],
                        'year': form.cleaned_data['member3_year']
                    }
                elif form.cleaned_data.get('is_leader4'):
                    leader_data = {
                        'college_name': form.cleaned_data['member4_college_name'],
                        'course_name': form.cleaned_data['member4_course_name'],
                        'year': form.cleaned_data['member4_year']
                    }
                elif form.cleaned_data.get('is_leader5') and form.cleaned_data.get('member5_name'):
                    leader_data = {
                        'college_name': form.cleaned_data.get('member5_college_name', ''),
                        'course_name': form.cleaned_data.get('member5_course_name', ''),
                        'year': form.cleaned_data.get('member5_year', '')
                    }
                elif form.cleaned_data.get('is_leader6') and form.cleaned_data.get('member6_name'):
                    leader_data = {
                        'college_name': form.cleaned_data.get('member6_college_name', ''),
                        'course_name': form.cleaned_data.get('member6_course_name', ''),
                        'year': form.cleaned_data.get('member6_year', '')
                    }
                
                # Helper function to get member data with leader defaults
                def get_member_data(member_num, prefix=''):
                    # For optional members (5 and 6), check if member exists
                    if member_num >= 5:
                        member_name = form.cleaned_data.get(f'{prefix}member{member_num}_name')
                        # If member name is not provided, return None for all fields
                        if not member_name:
                            return {
                                f'member{member_num}_college_name': None,
                                f'member{member_num}_college_code': None,
                                f'member{member_num}_course_name': None,
                                f'member{member_num}_year': None
                            }
                    
                    if leader_data:
                        college_key = f'{prefix}member{member_num}_college_name'
                        college_code_key = f'{prefix}member{member_num}_college_code'
                        course_key = f'{prefix}member{member_num}_course_name'
                        year_key = f'{prefix}member{member_num}_year'
                        
                        college_val = form.cleaned_data.get(college_key, '')
                        college_code_val = form.cleaned_data.get(college_code_key, '')
                        course_val = form.cleaned_data.get(course_key, '')
                        year_val = form.cleaned_data.get(year_key, '')
                        
                        # For optional members (5 and 6), if no values provided, use None
                        if member_num >= 5:
                            return {
                                f'member{member_num}_college_name': college_val if college_val else None,
                                f'member{member_num}_college_code': college_code_val if college_code_val else None,
                                f'member{member_num}_course_name': course_val if course_val else None,
                                f'member{member_num}_year': year_val if year_val else None
                            }
                        
                        return {
                            f'member{member_num}_college_name': college_val if college_val else leader_data['college_name'],
                            f'member{member_num}_college_code': college_code_val,
                            f'member{member_num}_course_name': course_val if course_val else leader_data['course_name'],
                            f'member{member_num}_year': year_val if year_val else leader_data['year']
                        }
                    else:
                        # If no leader found (shouldn't happen), use empty defaults
                        college_val = form.cleaned_data.get(f'{prefix}member{member_num}_college_name', '')
                        college_code_val = form.cleaned_data.get(f'{prefix}member{member_num}_college_code', '')
                        course_val = form.cleaned_data.get(f'{prefix}member{member_num}_course_name', '')
                        year_val = form.cleaned_data.get(f'{prefix}member{member_num}_year', '')
                        
                        # For optional members (5 and 6), if no values provided, use None
                        if member_num >= 5:
                            return {
                                f'member{member_num}_college_name': college_val if college_val else None,
                                f'member{member_num}_college_code': college_code_val if college_code_val else None,
                                f'member{member_num}_course_name': course_val if course_val else None,
                                f'member{member_num}_year': year_val if year_val else None
                            }
                        
                        return {
                            f'member{member_num}_college_name': college_val,
                            f'member{member_num}_college_code': college_code_val,
                            f'member{member_num}_course_name': course_val,
                            f'member{member_num}_year': year_val
                        }
                
                # Prepare data for Neon DB - match your table structure exactly
                registration_data = {
                    'team_name': team_name,
                    'team_size': form.cleaned_data.get('team_size', '4'),
                    'theme': form.cleaned_data['theme'],
                    'payment_screenshot': payment_screenshot_url,
                    'transaction_id': form.cleaned_data['transaction_id'],
                    'member1_name': form.cleaned_data['member1_name'],
                    'member1_email': form.cleaned_data['member1_email'],
                    'member1_phone': form.cleaned_data['member1_phone'],
                    'member1_roll': form.cleaned_data['member1_roll'],
                    'member1_gender': form.cleaned_data['member1_gender'],
                    'member1_college_name': form.cleaned_data['member1_college_name'],
                    'member1_college_code': form.cleaned_data['member1_college_code'],
                    'member1_course_name': form.cleaned_data['member1_course_name'],
                    'member1_year': form.cleaned_data['member1_year'],
                    'member1_tshirt_size': form.cleaned_data['member1_tshirt_size'],
                    'member1_food_preference': form.cleaned_data['member1_food_preference'],
                    'is_leader1': form.cleaned_data['is_leader1'],
                    'member2_name': form.cleaned_data['member2_name'],
                    'member2_email': form.cleaned_data['member2_email'],
                    'member2_phone': form.cleaned_data['member2_phone'],
                    'member2_roll': form.cleaned_data['member2_roll'],
                    'member2_gender': form.cleaned_data['member2_gender'],
                    'member2_college_code': form.cleaned_data['member2_college_code'],
                    'member2_tshirt_size': form.cleaned_data['member2_tshirt_size'],
                    'member2_food_preference': form.cleaned_data['member2_food_preference'],
                    **get_member_data(2),  # college_name, course_name, year with leader defaults
                    'is_leader2': form.cleaned_data['is_leader2'],
                    'member3_name': form.cleaned_data['member3_name'],
                    'member3_email': form.cleaned_data['member3_email'],
                    'member3_phone': form.cleaned_data['member3_phone'],
                    'member3_roll': form.cleaned_data['member3_roll'],
                    'member3_gender': form.cleaned_data['member3_gender'],
                    'member3_college_code': form.cleaned_data['member3_college_code'],
                    'member3_tshirt_size': form.cleaned_data['member3_tshirt_size'],
                    'member3_food_preference': form.cleaned_data['member3_food_preference'],
                    **get_member_data(3),  # college_name, course_name, year with leader defaults
                    'is_leader3': form.cleaned_data['is_leader3'],
                    'member4_name': form.cleaned_data['member4_name'],
                    'member4_email': form.cleaned_data['member4_email'],
                    'member4_phone': form.cleaned_data['member4_phone'],
                    'member4_roll': form.cleaned_data['member4_roll'],
                    'member4_gender': form.cleaned_data['member4_gender'],
                    'member4_college_code': form.cleaned_data['member4_college_code'],
                    'member4_tshirt_size': form.cleaned_data['member4_tshirt_size'],
                    'member4_food_preference': form.cleaned_data['member4_food_preference'],
                    **get_member_data(4),  # college_name, course_name, year with leader defaults
                    'is_leader4': form.cleaned_data['is_leader4'],
                    # Member 5 (Optional) - set all to None if member not provided
                    'member5_name': form.cleaned_data.get('member5_name') or None,
                    'member5_email': form.cleaned_data.get('member5_email') or None,
                    'member5_phone': form.cleaned_data.get('member5_phone') or None,
                    'member5_roll': form.cleaned_data.get('member5_roll') or None,
                    'member5_gender': form.cleaned_data.get('member5_gender') or None,
                    'member5_college_code': form.cleaned_data.get('member5_college_code') or None,
                    'member5_tshirt_size': form.cleaned_data.get('member5_tshirt_size') or None,
                    'member5_food_preference': form.cleaned_data.get('member5_food_preference') or None,
                    **get_member_data(5),  # college_name, course_name, year with leader defaults for optional member
                    'is_leader5': form.cleaned_data.get('is_leader5', False),
                    # Member 6 (Optional) - set all to None if member not provided
                    'member6_name': form.cleaned_data.get('member6_name') or None,
                    'member6_email': form.cleaned_data.get('member6_email') or None,
                    'member6_phone': form.cleaned_data.get('member6_phone') or None,
                    'member6_roll': form.cleaned_data.get('member6_roll') or None,
                    'member6_gender': form.cleaned_data.get('member6_gender') or None,
                    'member6_college_code': form.cleaned_data.get('member6_college_code') or None,
                    'member6_tshirt_size': form.cleaned_data.get('member6_tshirt_size') or None,
                    'member6_food_preference': form.cleaned_data.get('member6_food_preference') or None,
                    **get_member_data(6),  # college_name, course_name, year with leader defaults for optional member
                    'is_leader6': form.cleaned_data.get('is_leader6', False),
                }
                
                # Insert into Database
                try:
                    registration = TeamRegistration.objects.create(**registration_data)
                except IntegrityError:
                    raise Exception("conflict")
                
                print(f"=== CLOUDINARY UPLOAD DEBUG ===")
                print(f"payment_screenshot_path: {payment_screenshot_path}")
                print(f"preserved_file_info: {preserved_file_info}")
                import os
                if payment_screenshot_path:
                    print(f"File exists: {os.path.exists(payment_screenshot_path)}")
                    print(f"File size: {os.path.getsize(payment_screenshot_path) if os.path.exists(payment_screenshot_path) else 'N/A'}")
                print(f"===============================")
                # Only upload to Cloudinary after successful registration
                if payment_screenshot_path:
                    try:
                        # Upload payment screenshot to Cloudinary
                        unique_filename = f"{team_name.replace(' ', '_')}_payment_{uuid.uuid4()}"
                        response = cloudinary.uploader.upload(
                            payment_screenshot_path,
                            public_id=unique_filename,
                            folder="payment_screenshots",
                            resource_type="auto"
                        )
                        payment_screenshot_url = response.get('secure_url', '')
                        
                        # Update the registration record with the Cloudinary URL
                        registration.payment_screenshot = payment_screenshot_url
                        registration.save()
                        print(f"Payment screenshot uploaded to Cloudinary: {payment_screenshot_url}")
                        
                    except Exception as e:
                        print(f"Error uploading payment screenshot to Cloudinary: {str(e)}")
                        # Don't fail the registration if Cloudinary upload fails
                        # The registration is already successful at this point
                
                # Clear preserved file info after successful registration
                if 'preserved_payment_screenshot' in request.session:
                    preserved_data = request.session['preserved_payment_screenshot']
                    # Clean up temporary file if it exists
                    if 'temp_path' in preserved_data:
                        try:
                            import os
                            if os.path.exists(preserved_data['temp_path']):
                                os.remove(preserved_data['temp_path'])
                        except Exception as e:
                            print(f"Error cleaning up temporary file: {str(e)}")
                    
                    del request.session['preserved_payment_screenshot']
                
                return redirect('registration_success')
                
            except Exception as e:
                error_msg = str(e)
                print(f"Registration error: {error_msg}")
                print(f"Full error details: {repr(e)}")
                
                # Handle specific errors with helpful messages
                if 'CSRF' in error_msg.upper():
                    messages.error(request, 'Security verification failed. Please refresh the page (Ctrl+F5 or Cmd+Shift+R) and try submitting again.')
                elif 'cannot access local variable' in error_msg:
                    messages.error(request, 'Server configuration error. Please try again or contact support.')
                elif 'conflict' in error_msg.lower() or 'duplicate' in error_msg.lower():
                    if 'transaction_id' in error_msg.lower():
                        messages.error(request, 'This transaction ID has already been used. Please verify your transaction ID and try again.')
                    elif 'team_name' in error_msg.lower():
                        messages.error(request, 'A team with this name already exists. Please choose a different team name.')
                    else:
                        messages.error(request, 'A registration with this information already exists. Please check your details.')
                else:
                    messages.error(request, f'Error submitting registration: {error_msg}')
                
                # If PPT upload failed, we don't need to clean up since we didn't insert data
                
                # Create a new form instance to preserve other form data
                form = TeamRegistrationForm(request.POST, request.FILES)
                # Attach preserved file info to form for validation
                if preserved_file_info:
                    form.preserved_file_info = preserved_file_info
                
    else:
        form = TeamRegistrationForm()
        # Clear preserved file info when loading fresh form
        if 'preserved_payment_screenshot' in request.session:
            del request.session['preserved_payment_screenshot']
    
    # Default fee calculation for initial page load
    base_fee_per_person = 600
    default_team_size = 4
    default_total = base_fee_per_person * default_team_size
    
    context = {
        'form': form,
        'base_fee_per_person': base_fee_per_person,
        'default_total_fee': default_total,
        'discount_percentage': 10,
        'preserved_file_info': preserved_file_info,
    }
    
    return render(request, 'website/register.html', context)

def registration_success(request):
    """Show success page after registration"""
    return render(request, 'website/registration_success.html')

def home(request):
    """Home page view"""
    return render(request, 'website/home.html')