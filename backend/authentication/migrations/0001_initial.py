import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('w_id', models.AutoField(primary_key=True, serialize=False)),
                ('workspace_id', models.CharField(max_length=20, unique=True)),
                ('workspace_name', models.CharField(max_length=20)),
                ('workspace_token', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('channel_id', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=200)),
                ('is_owner', models.BooleanField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='%(app_label)s_%(class)s_related', related_query_name='%(app_label)s_%(class)ss', to='auth.permission', verbose_name='user permissions')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='authentication.workspace')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.UniqueConstraint(fields=('user_id', 'workspace'), name='user_unique'),
        ),
    ]
