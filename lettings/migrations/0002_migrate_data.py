from django.db import migrations

def migrate_lettings_data(apps, schema_editor):
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')
    
    for address in OldAddress.objects.all():
        NewAddress.objects.create(
            id=address.id,
            number=address.number,
            street=address.street,
            city=address.city,
            zip_code=address.zip_code,
            country_iso_code=address.country_iso_code,
        )
    
    for letting in OldLetting.objects.all():
        NewLetting.objects.create(
            id=letting.id,
            title=letting.title,
            address_id=letting.address_id,
        )

class Migration(migrations.Migration):
    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_lettings_data),
    ]
