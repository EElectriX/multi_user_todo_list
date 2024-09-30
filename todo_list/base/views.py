from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
# LoginRequiredMixin it is using to not allow the user to perform curd operation if they are not logged in.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages 


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    redirect_authenticated_user = True
    # if user if authenticated 

    def get_success_url(self):
        return reverse_lazy('tasks')

class CustomLogoutView(LogoutView):

    def get_success_url(self):
        return reverse_lazy('login')

# class Register_page(FormView):
#     template_name='base/register.html'
#     form_class=UserCreationForm

#     #form_class = RegisterForm
#     redirect_authenticated_user = True
#     success_url=reverse_lazy('tasks')

#     def form_valid(self, form):
#         user=form.save()
#         if user is not None:
#             login(self.request,user)
#         return super(Register_page,self).form_valid(form)
    
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasks')
#         return super(Register_page,self).get(*args,**kwargs)
   

class Register_page(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, 'Registration failed. Username already exists.')
        return super(Register_page, self).form_valid(form)


    def form_invalid(self, form):
        # Add an error message to the form
        messages.error(self.request, 'Registration failed.check the password rules and try again.')
        return super(Register_page, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(Register_page, self).get(request, *args, **kwargs)
    


# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model=Task
    #object_list querry set name by default.
    context_object_name="tasks"
    #changing querry set 
    # template_name="base/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        # context["tasks"] = context["tasks"].filter(complex=False).count()
        context["count"] = context["tasks"].filter(complete=False).count()
        context["counting"] = context["tasks"].count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith=search_input)
        context["search_input"] = search_input
        return context
    #for different users can see only their profile. 
    
class TaskLDetail(LoginRequiredMixin,DetailView):
    model=Task
    #object querry set name by default.
    context_object_name="task"
    template_name="base/task.html"
 
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields= ['title','description','complete']
    #form_class=TaskForm
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    # different users only can create their specific data. 

    

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields= ['title','description','complete']
    #form_class=TaskForm
    success_url=reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name="task"
    #form_class=TaskForm
    success_url=reverse_lazy('tasks')
    template_name="base/task_confirm_delete.html" #also it is the by default name . 





