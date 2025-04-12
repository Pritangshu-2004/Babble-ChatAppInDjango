from django.db import migrations, models
from django.db.models.functions import Lower

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=150,
                unique=True,
            ),
        ),
        migrations.RunSQL(
            sql=(
                "CREATE UNIQUE INDEX username_lower_idx "
                "ON accounts_user (LOWER(username));"
            ),
            reverse_sql="DROP INDEX username_lower_idx;",
        ),
    ]