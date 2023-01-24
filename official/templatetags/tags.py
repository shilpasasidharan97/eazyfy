from official.models import UserReply

from django import template


register = template.Library()


@register.simple_tag
def get_answer(question, user_request, option):
    if UserReply.objects.filter(user_request=user_request, question=question, option=option).exists():
        return "checked"
    else:
        return ""
