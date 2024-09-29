from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    #user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    """
on_delete=models.CASCADE: This specifies the behavior when the related object (in this case, the User) is deleted. CASCADE means that when the 
related User object is deleted, all related objects with this ForeignKey will also be deleted.

on_delete=models.SET_NULL: Specifies that when the related User object is deleted, this Foreign Key field will be set to NULL instead of deleting the object. 
This is useful when you want to keep the records in the current model but remove the link to the deleted User.

null=True: This allows the Foreign Key field to accept NULL values in the database,
 meaning it's not mandatory for every record to have a related User.

blank=True: This allows the field to be left blank in forms, 
making it optional when inputting data through a form.

    """
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=200,null=True,blank=True)
    complete=models.BooleanField(default=False)
    create=models.DateTimeField(auto_now_add=True)
    #auto matically add the time . 
    def __str__(self):
        return self.title
    # class Meta:
        
    #     ordering=['complete']
"""
Whenever an Article object is printed or listed in Django Admin, it will display the value 
of its title field instead of something generic like <Article object (1)>.

class Meta:: This is a nested class inside a Django model that holds various options for the model, like ordering, verbose names, permissions, etc.

ordering = ['complete']: This option tells Django how to order the query results by default when retrieving objects from the database.

The value inside the list ('complete') refers to a field in your model named complete.

The query results will be sorted in ascending order of the complete field by default. If you want the results to be sorted in descending order, 
you would prefix the field name with a hyphen (ordering = ['-complete']).
"""
    

