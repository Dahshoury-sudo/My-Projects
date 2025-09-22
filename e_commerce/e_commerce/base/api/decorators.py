## will rarely use it but it's just a good practise
## we often use @permission_classes() decorator

from django.shortcuts import redirect

def unauthorized_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('home')
        
    return wrapper_func