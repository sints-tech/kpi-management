from django import forms
from .models import (
    Story, DailyFeedReels, FeedReelsHistory, FYPPostValue, Campaign, CollabBrand,
    Profile, DashboardSettings, Report, AuditLog, SystemSettings, SocialMediaAccount, Company
)
from django.contrib.auth.models import User


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'title', 'platform', 'account_name', 'story_date',
            'content_file', 'content_image', 'content_url',
            'views', 'impressions', 'reach', 'engagement_rate',
            'link_clicks', 'swipe_up', 'reaction_rate', 'saves', 'shares', 'replays',
            'company', 'campaign', 'collab_brand', 'status', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'story_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'content_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,video/*'}),
            'content_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'content_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'views': forms.NumberInput(attrs={'class': 'form-control'}),
            'impressions': forms.NumberInput(attrs={'class': 'form-control'}),
            'reach': forms.NumberInput(attrs={'class': 'form-control'}),
            'engagement_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'link_clicks': forms.NumberInput(attrs={'class': 'form-control'}),
            'swipe_up': forms.NumberInput(attrs={'class': 'form-control'}),
            'reaction_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'saves': forms.NumberInput(attrs={'class': 'form-control'}),
            'shares': forms.NumberInput(attrs={'class': 'form-control'}),
            'replays': forms.NumberInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'collab_brand': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(is_active=True).order_by('company_type', 'name')
        self.fields['company'].required = False
        self.fields['campaign'].queryset = Campaign.objects.all().order_by('-start_date')
        self.fields['collab_brand'].queryset = CollabBrand.objects.all().order_by('-start_date')
        self.fields['campaign'].required = False
        self.fields['collab_brand'].required = False
        
        # Set optional fields that may not always be needed
        optional_fields = ['swipe_up', 'reaction_rate', 'saves', 'shares', 'replays', 
                          'content_file', 'content_image', 'content_url', 'notes', 'views', 'impressions', 
                          'reach', 'engagement_rate', 'link_clicks']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # Get social media accounts for account_name suggestions
        try:
            social_accounts = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
            account_choices = [('', 'Pilih Akun atau Ketik Manual')] + [(acc.account_name, f"{acc.get_platform_display()} - {acc.account_name}") for acc in social_accounts]
            self.fields['account_name'].widget = forms.Select(choices=account_choices, attrs={'class': 'form-select'})
            self.fields['account_name'].widget.attrs.update({'data-live-search': 'true'})
        except Exception:
            # If SocialMediaAccount doesn't exist, keep as TextInput
            pass


class DailyFeedReelsForm(forms.ModelForm):
    class Meta:
        model = DailyFeedReels
        fields = [
            'company', 'title', 'content_type', 'format_type', 'platform', 'account_name',
            'caption', 'content_url', 'content_file', 'thumbnail',
            'tags', 'hashtags', 'target_post_date',
            'likes', 'comments', 'shares', 'views', 'saves', 'engagement_rate',
            'campaign', 'collab_brand', 'status', 'publish_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'format_type': forms.Select(attrs={'class': 'form-select'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'content_url': forms.URLInput(attrs={'class': 'form-control'}),
            'content_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,video/*'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
            'hashtags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated hashtags'}),
            'target_post_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'likes': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.NumberInput(attrs={'class': 'form-control'}),
            'shares': forms.NumberInput(attrs={'class': 'form-control'}),
            'views': forms.NumberInput(attrs={'class': 'form-control'}),
            'saves': forms.NumberInput(attrs={'class': 'form-control'}),
            'engagement_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'collab_brand': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'publish_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(is_active=True).order_by('company_type', 'name')
        self.fields['company'].required = False
        self.fields['campaign'].queryset = Campaign.objects.all().order_by('-start_date')
        self.fields['collab_brand'].queryset = CollabBrand.objects.all().order_by('-start_date')
        self.fields['campaign'].required = False
        self.fields['collab_brand'].required = False
        self.fields['publish_date'].required = False
        
        # Set optional fields that may not always be needed
        optional_fields = ['likes', 'comments', 'shares', 'views', 'saves', 'engagement_rate',
                          'content_file', 'thumbnail', 'tags', 'hashtags', 'caption', 'content_url']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # Get social media accounts for account_name suggestions
        try:
            social_accounts = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
            account_choices = [('', 'Pilih Akun atau Ketik Manual')] + [(acc.account_name, f"{acc.get_platform_display()} - {acc.account_name}") for acc in social_accounts]
            self.fields['account_name'].widget = forms.Select(choices=account_choices, attrs={'class': 'form-select'})
            self.fields['account_name'].widget.attrs.update({'data-live-search': 'true'})
        except Exception:
            # If SocialMediaAccount doesn't exist, keep as TextInput
            pass


class FYPPostValueForm(forms.ModelForm):
    class Meta:
        model = FYPPostValue
        fields = [
            'post_title', 'platform', 'account_name', 'post_url', 'post_date',
            'fyp_views', 'total_views', 'fyp_percentage', 'reach', 'engagement_rate',
            'engagement_value', 'estimated_reach',
            'hashtags_used', 'audio_trending', 'niche', 'timing', 'best_practice_note',
            'notes'
        ]
        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'post_url': forms.URLInput(attrs={'class': 'form-control'}),
            'post_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fyp_views': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_views': forms.NumberInput(attrs={'class': 'form-control'}),
            'fyp_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'reach': forms.NumberInput(attrs={'class': 'form-control'}),
            'engagement_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'engagement_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_reach': forms.NumberInput(attrs={'class': 'form-control'}),
            'hashtags_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated hashtags'}),
            'audio_trending': forms.TextInput(attrs={'class': 'form-control'}),
            'niche': forms.TextInput(attrs={'class': 'form-control'}),
            'timing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Best practice timing'}),
            'best_practice_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set optional fields that may not always be needed
        optional_fields = ['fyp_views', 'total_views', 'fyp_percentage', 'reach', 'engagement_rate',
                          'engagement_value', 'estimated_reach', 'hashtags_used', 'audio_trending',
                          'niche', 'timing', 'best_practice_note', 'notes', 'post_url']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'company', 'name', 'description', 'objective', 'start_date', 'end_date',
            'budget', 'spent', 'target_platforms', 'target_audience', 'goals',
            'campaign_url', 'owner', 'status', 'notes'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objective': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'target_platforms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated platforms'}),
            'target_audience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'campaign_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(is_active=True).order_by('company_type', 'name')
        self.fields['company'].required = False
        self.fields['owner'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['owner'].required = False


class CollabBrandForm(forms.ModelForm):
    class Meta:
        model = CollabBrand
        fields = [
            'brand_name', 'contact_person', 'email', 'phone', 'company',
            'collaboration_type', 'start_date', 'end_date', 'contract_value',
            'payment_status', 'deliverables', 'deliverables_list',
            'contract_document', 'payment_reminder_date', 'renewal_reminder_date',
            'campaign', 'status', 'notes'
        ]
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'collaboration_type': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'deliverables': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contract_document': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'payment_reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'renewal_reminder_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # company adalah CharField, bukan ForeignKey, jadi tidak perlu queryset
        self.fields['campaign'].queryset = Campaign.objects.all().order_by('-start_date')
        self.fields['campaign'].required = False
        self.fields['payment_reminder_date'].required = False
        self.fields['renewal_reminder_date'].required = False


class ProfileForm(forms.ModelForm):
    # Fields untuk User model
    first_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'firstName'})
    )
    last_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lastName'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    organization = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'organization'})
    )
    phone_country = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'input-group-text', 'readonly': True, 'value': 'US (+1)'})
    )
    state = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'state', 'placeholder': 'California'})
    )
    zip_code = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'zipCode', 'placeholder': '231465', 'maxlength': '6'})
    )
    COUNTRY_CHOICES = [
        ('', 'Select'),
        ('Australia', 'Australia'),
        ('Bangladesh', 'Bangladesh'),
        ('Belarus', 'Belarus'),
        ('Brazil', 'Brazil'),
        ('Canada', 'Canada'),
        ('China', 'China'),
        ('France', 'France'),
        ('Germany', 'Germany'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Japan', 'Japan'),
        ('Korea', 'Korea, Republic of'),
        ('Mexico', 'Mexico'),
        ('Philippines', 'Philippines'),
        ('Russia', 'Russian Federation'),
        ('South Africa', 'South Africa'),
        ('Thailand', 'Thailand'),
        ('Turkey', 'Turkey'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States', 'United States'),
    ]

    LANGUAGE_CHOICES = [
        ('', 'Pilih Bahasa'),
        ('id', 'Bahasa Indonesia'),
        ('en', 'English'),
    ]

    TIMEZONE_CHOICES = [
        ('', 'Select Timezone'),
        ('-12', '(GMT-12:00) International Date Line West'),
        ('-11', '(GMT-11:00) Midway Island, Samoa'),
        ('-10', '(GMT-10:00) Hawaii'),
        ('-9', '(GMT-09:00) Alaska'),
        ('-8', '(GMT-08:00) Pacific Time (US & Canada)'),
        ('-8', '(GMT-08:00) Tijuana, Baja California'),
        ('-7', '(GMT-07:00) Arizona'),
        ('-7', '(GMT-07:00) Chihuahua, La Paz, Mazatlan'),
        ('-7', '(GMT-07:00) Mountain Time (US & Canada)'),
        ('-6', '(GMT-06:00) Central America'),
        ('-6', '(GMT-06:00) Central Time (US & Canada)'),
        ('-6', '(GMT-06:00) Guadalajara, Mexico City, Monterrey'),
        ('-6', '(GMT-06:00) Saskatchewan'),
        ('-5', '(GMT-05:00) Bogota, Lima, Quito, Rio Branco'),
        ('-5', '(GMT-05:00) Eastern Time (US & Canada)'),
        ('-5', '(GMT-05:00) Indiana (East)'),
        ('-4', '(GMT-04:00) Atlantic Time (Canada)'),
        ('-4', '(GMT-04:00) Caracas, La Paz'),
    ]

    CURRENCY_CHOICES = [
        ('', 'Select Currency'),
        ('usd', 'USD'),
        ('euro', 'Euro'),
        ('pound', 'Pound'),
        ('bitcoin', 'Bitcoin'),
    ]

    country = forms.ChoiceField(
        required=False,
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'select2 form-select', 'id': 'country'})
    )
    language = forms.ChoiceField(
        required=False,
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'select2 form-select', 'id': 'language'})
    )
    timezone = forms.ChoiceField(
        required=False,
        choices=TIMEZONE_CHOICES,
        widget=forms.Select(attrs={'class': 'select2 form-select', 'id': 'timeZones'})
    )
    currency = forms.ChoiceField(
        required=False,
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'select2 form-select', 'id': 'currency'})
    )

    class Meta:
        model = Profile
        fields = ['role', 'phone', 'address', 'bio', 'avatar', 'brand_name', 'logo', 'platform_linked', 'category', 'audience_segment', 'contact_info']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phoneNumber', 'placeholder': '202 555 0111'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'account-file-input', 'id': 'upload', 'style': 'display: none;', 'accept': 'image/png, image/jpeg, image/jpg, image/gif, image/webp'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=Profile.CATEGORY_CHOICES),
            'audience_segment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values dari User model jika instance ada
        if self.instance and self.instance.pk and self.instance.user:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

            # Set initial dari contact_info jika ada
            if self.instance.contact_info:
                contact_info = self.instance.contact_info if isinstance(self.instance.contact_info, dict) else {}
                self.fields['organization'].initial = contact_info.get('organization', '')
                self.fields['state'].initial = contact_info.get('state', '')
                self.fields['zip_code'].initial = contact_info.get('zip_code', '')
                self.fields['country'].initial = contact_info.get('country', '')
                self.fields['language'].initial = contact_info.get('language', '')
                self.fields['timezone'].initial = contact_info.get('timezone', '')
                self.fields['currency'].initial = contact_info.get('currency', '')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Validasi ukuran file (800KB = 800 * 1024 bytes)
            max_size = 800 * 1024
            if avatar.size > max_size:
                raise forms.ValidationError('Ukuran file terlalu besar. Maksimal 800KB.')
            
            # Validasi tipe file
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if avatar.content_type not in allowed_types:
                raise forms.ValidationError('Format file tidak didukung. Gunakan JPG, PNG, GIF, atau WEBP.')
        
        return avatar

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update User model
        if profile.user:
            user = profile.user
            if 'first_name' in self.cleaned_data:
                user.first_name = self.cleaned_data.get('first_name', '')
            if 'last_name' in self.cleaned_data:
                user.last_name = self.cleaned_data.get('last_name', '')
            if 'email' in self.cleaned_data:
                user.email = self.cleaned_data.get('email', '')
            if commit:
                user.save()

        # Update contact_info dengan data baru
        contact_info = profile.contact_info if isinstance(profile.contact_info, dict) else {}
        if 'organization' in self.cleaned_data:
            contact_info['organization'] = self.cleaned_data.get('organization', '')
        if 'state' in self.cleaned_data:
            contact_info['state'] = self.cleaned_data.get('state', '')
        if 'zip_code' in self.cleaned_data:
            contact_info['zip_code'] = self.cleaned_data.get('zip_code', '')
        if 'country' in self.cleaned_data:
            contact_info['country'] = self.cleaned_data.get('country', '')
        if 'language' in self.cleaned_data:
            contact_info['language'] = self.cleaned_data.get('language', '')
        if 'timezone' in self.cleaned_data:
            contact_info['timezone'] = self.cleaned_data.get('timezone', '')
        if 'currency' in self.cleaned_data:
            contact_info['currency'] = self.cleaned_data.get('currency', '')

        profile.contact_info = contact_info

        if commit:
            profile.save()
        return profile


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Kosongkan jika tidak ingin mengubah password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DashboardSettingsForm(forms.ModelForm):
    class Meta:
        model = DashboardSettings
        fields = [
            'role', 'show_total_campaign', 'show_total_story', 'show_total_fyp',
            'show_engagement_avg', 'show_revenue_kpi', 'show_user_activity',
            'show_notifications', 'can_view_dashboard', 'allowed_users'
        ]
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'show_total_campaign': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_total_story': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_total_fyp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_engagement_avg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_revenue_kpi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_user_activity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allowed_users': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'title', 'report_type', 'period', 'campaign_filter', 'brand_filter',
            'start_date', 'end_date', 'performance_type', 'auto_generate'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'campaign_filter': forms.Select(attrs={'class': 'form-select'}),
            'brand_filter': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'performance_type': forms.TextInput(attrs={'class': 'form-control'}),
            'auto_generate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campaign_filter'].queryset = Campaign.objects.all().order_by('-start_date')
        self.fields['brand_filter'].queryset = CollabBrand.objects.all().order_by('-start_date')
        self.fields['campaign_filter'].required = False
        self.fields['brand_filter'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['performance_type'].required = False


class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = [
            'name', 'label', 'setting_type', 'value', 'value_type',
            'description', 'is_active', 'is_public'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'contoh: site_name'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Situs'}),
            'setting_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'value_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value_type'].choices = [
            ('text', 'Text'),
            ('number', 'Number'),
            ('boolean', 'Boolean (true/false)'),
            ('json', 'JSON'),
            ('email', 'Email'),
            ('url', 'URL'),
        ]
        if self.instance and self.instance.pk:
            # Edit mode: name tidak bisa diubah
            self.fields['name'].widget.attrs['readonly'] = True


class SocialMediaAccountForm(forms.ModelForm):
    # Custom field untuk tags (convert dari list ke string dan sebaliknya)
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags (opsional)'}),
        help_text='Pisahkan dengan koma (contoh: marketing, social, influencer)'
    )

    class Meta:
        model = SocialMediaAccount
        fields = [
            'company', 'platform', 'account_name', 'account_id', 'display_name', 'profile_url',
            'owner', 'profile', 'status', 'is_verified', 'is_business_account',
            'input_method', 'auto_sync_enabled', 'sync_schedule',
            'followers_count', 'following_count', 'posts_count', 'engagement_rate',
            'access_token', 'refresh_token', 'api_key', 'api_secret',
            'notes', 'connected_at', 'last_synced_at'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username atau nama akun'}),
            'account_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID akun (opsional)'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama tampilan'}),
            'profile_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'profile': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_business_account': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'input_method': forms.Select(attrs={'class': 'form-select'}),
            'auto_sync_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sync_schedule': forms.Select(attrs={'class': 'form-select'}),
            'followers_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'following_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'posts_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'engagement_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'access_token': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Access token (untuk API sync)'}),
            'refresh_token': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Refresh token (untuk API sync)'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API Key (untuk API sync)'}),
            'api_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'API Secret (untuk API sync)', 'render_value': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'connected_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'last_synced_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(is_active=True).order_by('company_type', 'name')
        self.fields['company'].required = False
        self.fields['owner'].queryset = User.objects.filter(is_active=True).order_by('username')
        self.fields['owner'].required = False
        self.fields['profile'].queryset = Profile.objects.all().order_by('brand_name', 'user__username')
        self.fields['profile'].required = False
        self.fields['account_id'].required = False
        self.fields['display_name'].required = False
        self.fields['profile_url'].required = False
        self.fields['connected_at'].required = False
        self.fields['last_synced_at'].required = False
        self.fields['auto_sync_enabled'].required = False
        self.fields['sync_schedule'].required = False
        self.fields['sync_schedule'].choices = [
            ('', 'Pilih Jadwal'),
            ('hourly', 'Hourly (Setiap Jam)'),
            ('daily', 'Daily (Setiap Hari)'),
            ('weekly', 'Weekly (Setiap Minggu)'),
        ]
        self.fields['access_token'].required = False
        self.fields['refresh_token'].required = False
        self.fields['api_key'].required = False
        self.fields['api_secret'].required = False
        self.fields['notes'].required = False

        # Show/hide API fields berdasarkan input_method
        if 'input_method' in self.data:
            input_method = self.data.get('input_method', 'manual')
        elif self.instance and self.instance.pk:
            input_method = self.instance.input_method
        else:
            input_method = 'manual'

        if input_method == 'api':
            self.fields['access_token'].required = True
            self.fields['account_id'].required = True

        # Initialize tags field from list to comma-separated string
        if self.instance and self.instance.pk and hasattr(self.instance, 'tags'):
            if isinstance(self.instance.tags, list):
                self.fields['tags'].initial = ', '.join(self.instance.tags)
            elif self.instance.tags:
                self.fields['tags'].initial = str(self.instance.tags)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert tags from comma-separated string to list
        if 'tags' in self.cleaned_data:
            tags_str = self.cleaned_data.get('tags', '')
            if tags_str:
                tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                instance.tags = tags_list
            else:
                instance.tags = []

        if commit:
            instance.save()
        return instance

