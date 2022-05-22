# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from constants import MAX_DIGITS, MAX_LENGTH, DECIMAL_PLACES

class Category(models.Model):
    """
    Category Model used to store Category data.

    Attributes
    ----------
    name : str
        name of the category

    Methods
    -------
    str():
        Prints the attributes.
    """
    name = models.CharField(max_length=MAX_LENGTH, null=False)
    def __str__(self) -> str:
        return f"name: {self.name}"


class Groups(models.Model):
    """
    Groups Model used to store Groups data.

    Attributes
    ----------
    name : str
        name of the group
    members : ManyToMany
        
    Methods
    -------
    str():
        Prints the attributes.
    """
    name = models.CharField(max_length=MAX_LENGTH, null=False)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    
    def __str__(self) -> str:
        return f"name: {self.name}, members: {self.members}"


class Expenses(models.Model):
    """
    Expenses Model used to store Expenses data.

    Attributes
    ----------
    description : str
        description of expense
    total_amount : float
        amount of expense
    group - Foreign Key to group 

    category : Foreign Key to category 
        
    Methods
    -------
    str():
        Prints the attributes.
    """
    description = models.CharField(max_length=MAX_LENGTH)
    total_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    group = models.ForeignKey(Groups, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"description: {self.description}, total_amount: {self.total_amount}, group: {self.group}, category: {self.category}"

class UserExpense(models.Model):
    """
    Expenses Model used to store Expenses data.

    Attributes
    ----------
    amount_lent : float
        amount lent by the user
    amount_owed : float
        amount lent by the user
    expense - Foreign Key to expense 

    user : Foreign Key to user 
        
    Methods
    -------
    str():
        Prints the attributes.
    """
    expense = models.ForeignKey(Expenses, default=1, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount_owed = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    amount_lent = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)

    def __str__(self) -> str:
        return f"user: {self.user}, amount_owed: {self.amount_owed}, amount_lent: {self.amount_lent}"
