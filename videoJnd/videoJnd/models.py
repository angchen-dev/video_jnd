from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.timezone import now
import jsonfield
from videoJnd.src.GetConfig import get_config

class Experiment(models.Model):
    euid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=False, editable=True)
    name = models.CharField(max_length=20, default="", editable=True)
    description = models.TextField(max_length=4096, default="", editable=True)
    has_created_videos = models.BooleanField(default=False, editable=False)
    configuration = jsonfield.JSONField(default=get_config())
    pub_date = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)

    def __str__(self):
        return self.name

class InterfaceText(models.Model):
    title = models.CharField(max_length=20, default="InterfaceText", editable=False)
    question = models.TextField(max_length=4096, default="", null=False, blank=False)
    text_end_exp = RichTextField(default="", null=False, blank=False)
    text_end_hit = RichTextField(default="", null=False, blank=False)
    timeout_msg = models.TextField(max_length=4096, default="", null=False, blank=False)
    btn_text_end_hit = models.TextField(max_length=4096, default="", null=False, blank=False)

class Instruction(models.Model):
    title = models.CharField(max_length=20, default="Instruction", editable=False)
    description = RichTextField()

class ConsentForm(models.Model):
    title = models.CharField(max_length=20, default="Consent Form", editable=False)
    description = RichTextField()

class VideoObj(models.Model):
    vuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    source_video = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    codec = models.CharField(max_length=10, default="", editable=False)
    frame_rate = models.IntegerField(default=0, editable=False)
    crf = models.CharField(max_length=10, default="", editable=False)
    rating = models.IntegerField(default=0, editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    qp_count = models.IntegerField(default=0, editable=False)
    qp = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    result_orig = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    result_code = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    participant_result = models.TextField(max_length=4096, editable=False, null=False, blank=False)
    is_finished = models.BooleanField(default=False, editable=False)
    cur_participant = models.CharField(max_length=20, editable=False, null=True, blank=True)
    cur_participant_uid = models.CharField(max_length=50, editable=False, null=True, blank=True)

    # only for displaying the time when the user start the experiment
    participant_start_date = models.CharField(max_length=20, editable=False, null=True, blank=True) 
    
    def __str__(self):
        return self.source_video

class Participant(models.Model):
    puid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    email = models.EmailField(max_length=30, editable=False, default="", null=True, blank=True)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=False, blank=True, null=True)
    videos = models.TextField(max_length=4096, default="", editable=False)
    ongoing = models.BooleanField(default=False, editable=False)

class RatingHistory(models.Model):
    puid = models.UUIDField(editable=False, null=True, blank=True)
    pname = models.CharField(max_length=20, editable=False, null=False, blank=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vuid = models.UUIDField(editable=False, null=True, blank=True)
    side = models.CharField(max_length=10, editable=False, null=False, blank=False)
    qp = models.CharField(max_length=10, editable=False, null=False, blank=False)
    decision = models.CharField(max_length=10, editable=False, null=False, blank=False)
    result_orig = models.CharField(max_length=10, editable=False, null=False, blank=False)
    update_time = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)

class EtJndHit(models.Model):
    huid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=True)
    image_url = models.TextField(max_length=4096, default="")
    image_gts = models.TextField(max_length=4096, default="")
    test_gt = models.TextField(max_length=4096, default="")
    def __str__(self):
        return self.name

class EtJndResult(models.Model):
    hit_id = models.CharField(max_length=64, default="", editable=True)
    assignment_id = models.CharField(max_length=64, default="django_task", editable=True)
    worker_id = models.CharField(max_length=64, default="", editable=True)
    result = models.TextField(default="")
    status = models.CharField(max_length=20, default="Submitted", editable=True)
    accept_time = models.CharField(max_length=20, default="", editable=True)
    submit_time = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)

class EtJndParticipant(models.Model):
    wuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cur_hit = models.CharField(max_length=20, default="", editable=True)
    left_hits = jsonfield.JSONField()
    join_date = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)
    finish_all_hits = models.BooleanField(default=False, editable=False)

