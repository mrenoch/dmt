from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    fullname = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=32)
    status = models.CharField(max_length=16, blank=True)
    grp = models.BooleanField(default=False)
    password = models.CharField(max_length=256, blank=True)
    type = models.TextField(blank=True)
    title = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    photo_url = models.TextField(blank=True)
    photo_width = models.IntegerField(null=True, blank=True)
    photo_height = models.IntegerField(null=True, blank=True)
    campus = models.TextField(blank=True)
    building = models.TextField(blank=True)
    room = models.TextField(blank=True)

    class Meta:
        db_table = u'users'

    def __unicode__(self):
        return self.fullname

    def get_absolute_url(self):
        return "/user/%s/" % self.username


class Project(models.Model):
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    pub_view = models.BooleanField(default=False)
    caretaker = models.ForeignKey(User, db_column='caretaker')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=16, blank=True)
    type = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=255, blank=True)
    restricted = models.CharField(max_length=10, blank=True)
    approach = models.CharField(max_length=50, blank=True)
    info_url = models.CharField(max_length=255, blank=True)
    entry_rel = models.BooleanField(default=False)
    eval_url = models.CharField(max_length=255, blank=True)
    projnum = models.IntegerField(null=True, blank=True)
    scale = models.CharField(max_length=20, blank=True)
    distrib = models.CharField(max_length=20, blank=True)
    poster = models.BooleanField(default=False)
    wiki_category = models.CharField(max_length=256, blank=True)

    class Meta:
        db_table = u'projects'
        ordering = ['name', ]

    def get_absolute_url(self):
        return "/project/%d/" % self.pid


class Document(models.Model):
    did = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Project, db_column='pid')
    filename = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=8, blank=True)
    url = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=16, blank=True)
    author = models.ForeignKey(User, db_column='author')
    last_mod = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'documents'


class Milestone(models.Model):
    mid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    target_date = models.DateField()
    project = models.ForeignKey(Project, db_column='pid')
    status = models.CharField(max_length=8)
    description = models.TextField(blank=True)

    class Meta:
        db_table = u'milestones'
        ordering = ['target_date', 'name', ]

    def get_absolute_url(self):
        return "/milestone/%d/" % self.mid

    def status_class(self):
        return self.status.lower()


class Item(models.Model):
    iid = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=12)
    owner = models.ForeignKey(User, db_column='owner',
                              related_name='owned_items')
    assigned_to = models.ForeignKey(User, db_column='assigned_to',
                                    related_name='assigned_items')
    title = models.CharField(max_length=255)
    milestone = models.ForeignKey(Milestone, db_column='mid')
    status = models.CharField(max_length=16)
    description = models.TextField(blank=True)
    priority = models.IntegerField(null=True, blank=True)
    r_status = models.CharField(max_length=16, blank=True)
    last_mod = models.DateTimeField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    estimated_time = models.TextField(blank=True)
    url = models.TextField(blank=True)

    class Meta:
        db_table = u'items'

    def get_absolute_url(self):
        return "/item/%d/" % self.iid

    def status_class(self):
        return self.status.lower()

    def is_bug(self):
        return self.type == "bug"


class Notify(models.Model):
    item = models.ForeignKey(Item, null=False, db_column='iid')
    username = models.ForeignKey(User, db_column='username')

    class Meta:
        db_table = u'notify'


class Client(models.Model):
    client_id = models.IntegerField(primary_key=True)
    lastname = models.CharField(max_length=64, blank=True)
    firstname = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=128, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    add_affiliation = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=128, blank=True)
    contact = models.ForeignKey(User, null=True, db_column='contact',
                                blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=16, blank=True)
    email_secondary = models.CharField(max_length=128, blank=True)
    phone_mobile = models.CharField(max_length=32, blank=True)
    phone_other = models.CharField(max_length=32, blank=True)
    website_url = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'clients'


class ItemClient(models.Model):
    item = models.ForeignKey(Item, db_column='iid')
    client = models.ForeignKey(Client)

    class Meta:
        db_table = u'item_clients'


class Node(models.Model):
    nid = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=256, blank=True)
    body = models.TextField(blank=True)
    author = models.ForeignKey(User, db_column='author')
    reply_to = models.IntegerField(null=True, blank=True)
    replies = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=8)
    overflow = models.BooleanField(default=False)
    added = models.DateTimeField()
    modified = models.DateTimeField()
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'nodes'


class WorksOn(models.Model):
    username = models.ForeignKey(User, db_column='username')
    project = models.ForeignKey(Project, db_column='pid')
    auth = models.CharField(max_length=16)

    class Meta:
        db_table = u'works_on'


class Events(models.Model):
    eid = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=32)
    event_date_time = models.DateTimeField(null=True, blank=True)
    item = models.ForeignKey(Item, db_column='item')

    class Meta:
        db_table = u'events'


class NotifyProject(models.Model):
    pid = models.ForeignKey(Project, db_column='pid')
    username = models.ForeignKey(User, db_column='username')

    class Meta:
        db_table = u'notify_project'


class InGroup(models.Model):
    grp = models.ForeignKey(User, db_column='grp',
                            related_name='group_members')
    username = models.ForeignKey(User, null=True,
                                 db_column='username', blank=True)

    class Meta:
        db_table = u'in_group'


class ProjectClient(models.Model):
    pid = models.ForeignKey(Project, db_column='pid')
    client = models.ForeignKey(Client)
    role = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'project_clients'


class ActualTime(models.Model):
    item = models.ForeignKey(Item, null=False, db_column='iid')
    resolver = models.ForeignKey(User, db_column='resolver')
    actual_time = models.TextField(blank=True)
    completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'actual_times'


class Attachment(models.Model):
    item = models.ForeignKey(Item, db_column='iid')
    filename = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=8, blank=True)
    url = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, db_column='author')
    last_mod = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'attachment'


class Comment(models.Model):
    cid = models.IntegerField(primary_key=True)
    comment = models.TextField()
    add_date_time = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=32)
    item = models.ForeignKey(Item, null=True, db_column='item', blank=True)
    event = models.ForeignKey(Events, null=True, db_column='event', blank=True)

    class Meta:
        db_table = u'comments'
