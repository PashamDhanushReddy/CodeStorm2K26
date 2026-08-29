from django import forms
from django.core.validators import FileExtensionValidator

class TeamRegistrationForm(forms.Form):
    # Team details
    team_size = forms.ChoiceField(
        choices=[
            ('4', '4 Members'),
            ('5', '5 Members'),
            ('6', '6 Members')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    team_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Enter your team name'
        })
    )
    
    # Theme selection
    theme = forms.ChoiceField(
        choices=[
            ('Generative AI & LLM Applications', 'Generative AI & LLM Applications'),
            ('Robotics, Drones & Autonomous Systems', 'Robotics, Drones & Autonomous Systems'),
            ('Cybersecurity & Threat Intelligence', 'Cybersecurity & Threat Intelligence'),
            ('HealthTech, MedAI & Diagnostics', 'HealthTech, MedAI & Diagnostics'),
            ('FinTech, Blockchain & Digital Trust', 'FinTech, Blockchain & Digital Trust'),
            ('Smart Cities, IoT & Edge Computing', 'Smart Cities, IoT & Edge Computing'),
            ('Green Tech & Energy Optimization', 'Green Tech & Energy Optimization'),
            ('Agritech & Rural Innovation', 'Agritech & Rural Innovation'),
            ('Transportation & Logistics (AI-Driven)', 'Transportation & Logistics (AI-Driven)'),
            ('Open Innovation Challenge (Wildcard Track)', 'Open Innovation Challenge (Wildcard Track)')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control'
        })
    )
    
    # Payment screenshot upload
    payment_screenshot = forms.FileField(
        required=False,  # Will be validated conditionally in clean method
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])],
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'accept': '.jpg,.jpeg,.png,.pdf'
        })
    )
    
    # Transaction ID
    transaction_id = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Enter transaction ID from payment receipt'
        })
    )
    
    # Member 1 (Required)
    member1_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member1_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member1_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member1_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member1_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member1_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member1_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member1_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
            
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member1_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader1 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(1)'
        })
    )
    member1_tshirt_size = forms.ChoiceField(
        choices=[
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member1_food_preference = forms.ChoiceField(
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    # Member 2 (Required)
    member2_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member2_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member2_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member2_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member2_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member2_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member2_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member2_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member2_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader2 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(2)'
        })
    )
    member2_tshirt_size = forms.ChoiceField(
        choices=[
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member2_food_preference = forms.ChoiceField(
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    # Member 3 (Required)
    member3_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member3_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member3_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member3_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member3_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member3_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member3_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member3_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member3_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader3 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(3)'
        })
    )
    member3_tshirt_size = forms.ChoiceField(
        choices=[
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member3_food_preference = forms.ChoiceField(
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    # Member 4 (Required)
    member4_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member4_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member4_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member4_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member4_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member4_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member4_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member4_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member4_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(4)'
        })
    )
    member4_tshirt_size = forms.ChoiceField(
        choices=[
             ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member4_food_preference = forms.ChoiceField(
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    # Member 5 (Optional)
    member5_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member5_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member5_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member5_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member5_gender = forms.ChoiceField(
        required=False,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member5_college_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member5_course_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member5_year = forms.ChoiceField(
        required=False,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member5_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader5 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(5)'
        })
    )
    member5_tshirt_size = forms.ChoiceField(
        required=False,
        choices=[
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member5_food_preference = forms.ChoiceField(
        required=False,
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    
    # Member 6 (Optional)
    member6_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Full Name'
        })
    )
    member6_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Email Address'
        })
    )
    member6_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member6_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Roll Number'
        })
    )
    member6_gender = forms.ChoiceField(
        required=False,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member6_college_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Code'
        })
    )
    member6_course_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'Course Name (Eg.. BTECH-CSE)'
        })
    )
    member6_year = forms.ChoiceField(
        required=False,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member6_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 form-control',
            'placeholder': 'College Name'
        })
    )
    is_leader6 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(6)'
        })
    )
    member6_tshirt_size = forms.ChoiceField(
        required=False,
        choices=[
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('XXXL', 'XXXL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )
    member6_food_preference = forms.ChoiceField(
        required=False,
        choices=[
            ('Veg', 'Veg'),
            ('Non Veg', 'Non Veg')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 form-control',
        })
    )

    def clean_member1_email(self):
        email = self.cleaned_data.get('member1_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member2_email(self):
        email = self.cleaned_data.get('member2_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member3_email(self):
        email = self.cleaned_data.get('member3_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member4_email(self):
        email = self.cleaned_data.get('member4_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member5_email(self):
        email = self.cleaned_data.get('member5_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member6_email(self):
        email = self.cleaned_data.get('member6_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email

    def clean_member1_phone(self):
        phone = self.cleaned_data.get('member1_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member2_phone(self):
        phone = self.cleaned_data.get('member2_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member3_phone(self):
        phone = self.cleaned_data.get('member3_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member4_phone(self):
        phone = self.cleaned_data.get('member4_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member5_phone(self):
        phone = self.cleaned_data.get('member5_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member6_phone(self):
        phone = self.cleaned_data.get('member6_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone

    def clean_member1_college_code(self):
        college_code = self.cleaned_data.get('member1_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member1_college_name(self):
        college_name = self.cleaned_data.get('member1_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member1_course_name(self):
        course_name = self.cleaned_data.get('member1_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member2_college_code(self):
        college_code = self.cleaned_data.get('member2_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member2_college_name(self):
        college_name = self.cleaned_data.get('member2_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member2_course_name(self):
        course_name = self.cleaned_data.get('member2_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member3_college_code(self):
        college_code = self.cleaned_data.get('member3_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member3_college_name(self):
        college_name = self.cleaned_data.get('member3_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member3_course_name(self):
        course_name = self.cleaned_data.get('member3_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member4_college_code(self):
        college_code = self.cleaned_data.get('member4_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member4_college_name(self):
        college_name = self.cleaned_data.get('member4_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member4_course_name(self):
        course_name = self.cleaned_data.get('member4_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member5_college_code(self):
        college_code = self.cleaned_data.get('member5_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member5_college_name(self):
        college_name = self.cleaned_data.get('member5_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member5_course_name(self):
        course_name = self.cleaned_data.get('member5_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member6_college_code(self):
        college_code = self.cleaned_data.get('member6_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member6_college_name(self):
        college_name = self.cleaned_data.get('member6_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member6_course_name(self):
        course_name = self.cleaned_data.get('member6_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_payment_screenshot(self):
        """Custom validation for payment screenshot to handle preserved files"""
        payment_screenshot = self.cleaned_data.get('payment_screenshot')
        
        # If no new file is uploaded, check if we have a preserved file
        if not payment_screenshot and hasattr(self, 'preserved_file_info'):
            # Return a dummy value to indicate preserved file exists
            return 'PRESERVED_FILE_EXISTS'
        
        return payment_screenshot

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that exactly one leader is selected
        leader_fields = ['is_leader1', 'is_leader2', 'is_leader3', 'is_leader4', 'is_leader5', 'is_leader6']
        leader_count = sum(1 for field in leader_fields if cleaned_data.get(field))
        
        if leader_count != 1:
            raise forms.ValidationError('Exactly one team member must be designated as the leader.')
        
        # Validate optional members
        if cleaned_data.get('is_leader5') and not cleaned_data.get('member5_name'):
            raise forms.ValidationError('Member 5 cannot be leader if not provided.')
        
        if cleaned_data.get('is_leader6') and not cleaned_data.get('member6_name'):
            raise forms.ValidationError('Member 6 cannot be leader if not provided.')
        
        # Validate that at least one female member is in the team
        team_size_str = cleaned_data.get('team_size', '4')
        try:
            team_size = int(team_size_str)
        except (ValueError, TypeError):
            team_size = 4
        
        # Validate payment screenshot - either new file or preserved file
        payment_screenshot = cleaned_data.get('payment_screenshot')
        has_preserved_file = hasattr(self, 'preserved_file_info')
        
        if not payment_screenshot and not has_preserved_file:
            raise forms.ValidationError('Payment screenshot is required. Please upload a screenshot of your payment confirmation.')
        
        female_count = 0
        
        for i in range(1, team_size + 1):
            gender = cleaned_data.get(f'member{i}_gender', '')
            member_name = cleaned_data.get(f'member{i}_name', '')
            # Only count if member exists and is female
            # Check both with and without stripping whitespace
            if member_name and str(gender).strip() == 'Female':
                female_count += 1
        
        if female_count == 0:
            raise forms.ValidationError('At least one team member must be female.')
        
        # Validate inter-college discount eligibility
        team_size_str = cleaned_data.get('team_size', '4')
        try:
            team_size = int(team_size_str)
        except (ValueError, TypeError):
            team_size = 4
        
        # Collect all college codes
        college_codes = set()
        for i in range(1, team_size + 1):
            member_name = cleaned_data.get(f'member{i}_name', '')
            if member_name:
                college_code = cleaned_data.get(f'member{i}_college_code', '').strip().upper()
                if college_code:
                    college_codes.add(college_code)
        
        # Check if team is eligible for discount (has both NRCM and non-NRCM members)
        has_nrcm = 'NRCM' in college_codes
        has_non_nrcm = len(college_codes) > 1 and any(code != 'NRCM' for code in college_codes)
        
        # Store discount eligibility in cleaned_data for use in views
        cleaned_data['_discount_eligible'] = has_nrcm and has_non_nrcm
        
        return cleaned_data