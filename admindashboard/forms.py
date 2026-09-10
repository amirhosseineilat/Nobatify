from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class AdminLogingForm(AuthenticationForm):

	def confirm_login_allowed(self,user):

		if not user.is_admin:
			raise ValidationError(
				"only admin user can login"
				)