from django.db import models


class Box(models.Model):
    box_id = models.IntegerField(primary_key=True, serialize=False, verbose_name='BOX_ID')
    box_num = models.TextField()
    box_dest = models.TextField()
    contents = models.TextField()
    box_warnings = models.TextField()
    box_qr_val = models.TextField()

    def __str__(self):
        return self.box_num
