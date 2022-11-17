# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Items(models.Model):
    i_id = models.IntegerField(primary_key=True)
    i_name = models.CharField(max_length=50, blank=True, null=True)
    i_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


class Items1(models.Model):
    i_id = models.IntegerField(primary_key=True)
    i_name = models.CharField(max_length=50)
    i_price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'items1'


class Stocks(models.Model):
    w_id = models.IntegerField(primary_key=True)
    i_id = models.IntegerField()
    s_qty = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'
        unique_together = (('w_id', 'i_id'),)


class Stocks1(models.Model):
    w = models.OneToOneField('Warehouses1', models.DO_NOTHING, primary_key=True)
    i = models.ForeignKey(Items1, models.DO_NOTHING)
    s_qty = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks1'
        unique_together = (('w', 'i'),)


class Warehouses(models.Model):
    w_id = models.IntegerField(primary_key=True)
    w_name = models.CharField(max_length=50, blank=True, null=True)
    w_street_1 = models.CharField(max_length=50, blank=True, null=True)
    w_street_2 = models.CharField(max_length=50, blank=True, null=True)
    w_city = models.CharField(max_length=50, blank=True, null=True)
    w_state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouses'


class Warehouses1(models.Model):
    w_id = models.IntegerField(primary_key=True)
    w_name = models.CharField(max_length=50, blank=True, null=True)
    w_street_1 = models.CharField(max_length=50, blank=True, null=True)
    w_street_2 = models.CharField(max_length=50, blank=True, null=True)
    w_city = models.CharField(max_length=50, blank=True, null=True)
    w_state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouses1'