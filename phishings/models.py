import hashlib
from django.db import models


class Phishing(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=None, editable=False
    )
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.id = hashlib.sha256(self.url.encode("utf-8")).hexdigest()
        super(Phishing, self).save(*args, **kwargs)


class Form(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=None, editable=False
    )

    phishing = models.ForeignKey(
        Phishing, on_delete=models.CASCADE, related_name="forms"
    )

    meta_id = models.IntegerField()

    html_id = models.CharField(max_length=255, null=True)
    html_action = models.CharField(max_length=255, null=True)
    html_method = models.CharField(max_length=255, null=True)
    html_type = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        self.id = f"{self.phishing.id}-{self.meta_id}"
        super(Form, self).save(*args, **kwargs)


class Input(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=None, editable=False
    )

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="inputs")

    meta_id = models.IntegerField()

    html_id = models.CharField(max_length=255, null=True)
    html_name = models.CharField(max_length=255, null=True)
    html_placeholder = models.CharField(max_length=255, null=True)
    html_type = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        self.id = f"{self.form.id}-{self.meta_id}"
        super(Input, self).save(*args, **kwargs)


class Action(models.Model):
    phishing = models.ForeignKey(
        Phishing, on_delete=models.CASCADE, related_name="actions"
    )
    action = models.CharField(max_length=255)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
