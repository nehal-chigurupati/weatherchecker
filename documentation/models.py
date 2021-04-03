from django.db import models

class project(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    directory = models.CharField(max_length=1000, default="NOT PROVIDED")

    def __str__(self):
        return self.name

class interface(models.Model):
    name = models.CharField(max_length=30)
    implementing_class = models.CharField(max_length=30)
    project = models.ForeignKey(project, related_name='interfaces', on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=10000)
    directory = models.CharField(max_length=1000, default="NOT PROVIDED")

    def __str__(self):
        return self.name


class method(models.Model):
    name = models.CharField(max_length=30)
    header = models.CharField(max_length=100)
    returns = models.CharField(max_length=200)
    updates = models.CharField(max_length=200)
    prints = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=10000)
    interface = models.ForeignKey(interface, related_name='methods', on_delete=models.CASCADE, blank=True, null=True)
    builder_handle = models.CharField(max_length=200)
    isCodeWritten = models.BooleanField(default=False)
    isCodeTested = models.BooleanField(default=False)
    isCodeUsable = models.BooleanField(default=False)
    directory = models.CharField(max_length=1000, default='NOT PROVIDED')

    def __str__(self):
        return self.name
