from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from apps.invitation.models import Invitation
from common.constants import Invite_type, ApplicationMessages
from .models import User
from apps.company.models import Company
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import AcceptInvitationForm
from django.contrib.auth.hashers import make_password
from squad_spot.settings import HOST_URL, COMPANY_ADMIN_URL


class AcceptInvitationView(FormView):
    form_class = AcceptInvitationForm

    def get(self, request, uuid):
        valid_flag = True
        obj = Invitation.objects.filter(id=uuid)
        if obj:
            obj = obj.first()
        else:
            obj = Company.objects.filter(id=uuid).first()

        if (
            (
                obj.invite_type == Invite_type.INTERNAL
                or obj.invite_type == Invite_type.COMPANY
            )
            and (not obj.is_active)
        ) or (
            obj.invite_type == Invite_type.COMPANY_OWNER and (obj.is_active)
        ):
            valid_flag = False
            self.template_name = "unauthorized_access.html"
            return render(
                request,
                "unauthorized_access.html",
                {"error_message": ApplicationMessages.INVITATION_INVALID},
                status=401,
            )
        return render(
            request,
            "user/accept_invitation.html",
            {
                "form": self.form_class,
                "invitation": obj,
                "flag": valid_flag,
            },
            status=200,
        )

    def post(self, request, uuid):
        # Retrieve the invitation associated with the UUID
        company_name = ""
        obj = Invitation.objects.filter(id=uuid)
        if obj:
            obj = obj.first()
        else:
            obj = Company.objects.filter(id=uuid).first()

        if (
            obj.invite_type in [Invite_type.INTERNAL, Invite_type.COMPANY]
            and (not obj.is_active)
        ) or (
            obj.invite_type == Invite_type.COMPANY_OWNER and (obj.is_active)
        ):
            return render(
                request,
                "unauthorized_access.html",
                {"error_message": ApplicationMessages.INVITATION_INVALID},
                status=401,
            )

        # Create a new user with the provided email and password
        password = request.POST.get("password")
        encrpt_pswd = make_password(password)
        if obj.invite_type == Invite_type.COMPANY_OWNER:
            User.objects.create(
                full_name=obj.owner_name,
                email=obj.owner_email,
                company=obj,
                password=encrpt_pswd,
                is_staff=True,
                is_company_owner=True,
            )
            obj.is_active = True
            obj.invite_link = ""
            obj.save()
            company_name = obj.name.replace(" ", "-").lower()
        else:
            if obj.invite_type == Invite_type.COMPANY:
                com_obj = Company.objects.get(id=obj.company_id)
                company_name = com_obj.name.replace(" ", "-").lower()
            User.objects.create(
                full_name=obj.fullname,
                email=obj.email,
                role=obj.role,
                company=com_obj
                if obj.invite_type == Invite_type.COMPANY
                else None,
                password=encrpt_pswd,
                is_staff=True,
                is_company_owner=False,
            )
            obj.is_active = False
            obj.save()
        redirect_url = reverse("user:password_set_success")
        if company_name:
            redirect_url += f"?company_name={company_name}"

        return HttpResponseRedirect(redirect_url)  # Redirect to a success page


class PasswordSetSuccessView(TemplateView):
    template_name = "user/set_password_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.GET.get("company_name")
        if company_name is not None:
            login_url = f"http://{company_name}.{COMPANY_ADMIN_URL}"
        else:
            login_url = f"{HOST_URL}/ss-admin/"
        context["login_url"] = login_url
        return context
