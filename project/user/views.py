from django.views import View, generic
from django.contrib.auth import views as auth_views, mixins

generic_form_template = 'page/user/form.html'

class LoginView(auth_views.LoginView):
    template_name = generic_form_template
    extra_context = {
        "form_title": "Iniciar sesión",
        "form_action": "Iniciar sesión",
    }
    def get_form(self, form_class = None):
        f = super().get_form(form_class)
        f.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        return f
    
class LogoutView(auth_views.LogoutView):
    template_name = generic_form_template

class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = generic_form_template
    extra_context = {
        "form_title": "Cambiar contraseña",
        "form_action": "Confirmar",
    }

class ProfileView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'page/user/profile.html'