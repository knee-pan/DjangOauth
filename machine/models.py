from datetime import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.core.cache import cache
# Create your models here.


class MachineType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    general_width = models.PositiveIntegerField(default=120)
    general_height = models.PositiveIntegerField(default=68)

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "Machine Types"

    def __str__(self):
        return self.name


class Profile(models.Model):
    # Choices
    class DIMMING_TYPES(models.IntegerChoices):
        OFF = 0, "Off"
        CHECKERBOARD = 1, "Checkerboard"
        HOMOGENEUS = 2, "Homogeneous"

    # General
    name = models.CharField(
        max_length=50, unique=True, help_text="Profile name must be unique"
    )

    machine_type = models.ManyToManyField(MachineType, related_name="profiles")

    color = models.CharField(
        max_length=7,
        default="#ffffff",
        validators=[MinLengthValidator(7)],
        help_text="Profile color for resin",
    )

    confirmed = models.BooleanField(default=False)

    layer_thickness = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(5), MaxValueValidator(10000)],
        help_text="5 - 10000 micron",
    )

    xy_scale_factor = models.FloatField(
        default=1,
        validators=[MinValueValidator(-0.5), MaxValueValidator(1.2)],
        help_text="-0.5 - 1.2",
    )

    # Base Layers
    base_cure_time = models.PositiveIntegerField(
        default=9000,
        validators=[MinValueValidator(50), MaxValueValidator(40000)],
        help_text="50 - 40000 ms",
    )

    base_wait_before_cure = models.PositiveSmallIntegerField(
        default=500,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text="1 - 5000",
    )

    base_wait_on_top = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(25), MaxValueValidator(5000)],
        help_text="25 - 5000",
    )

    base_wait_after_cure = models.PositiveSmallIntegerField(
        default=150,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text="1 - 5000",
    )

    base_light_ratio = models.FloatField(
        default=1,
        validators=[MinValueValidator(0.1), MaxValueValidator(2)],
        help_text="0.1 - 2.0",
    )

    base_layer_count = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="1 - 100",
    )

    # NOTE: (Depricated) Windows Base Z Speed
    base_z_speed = models.PositiveSmallIntegerField(
        verbose_name="Windows Base Z Speed",
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        help_text="1 - 9",
    )

    # NOTE: (DEPRICATED)Linux Base Z Speed
    advanced_base_z_speed = models.PositiveSmallIntegerField(
        verbose_name="Linux Base Z Speed",
        default=310,
        validators=[MinValueValidator(150), MaxValueValidator(2000)],
        help_text="150 - 2000",
    )

    base_z_speed_step_1 = models.PositiveSmallIntegerField(
        verbose_name="Base Z Speed(Step 1)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    base_z_speed_step_2 = models.PositiveSmallIntegerField(
        verbose_name="Base Z Speed(Step 2)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    # NOTE: (Depricated) Windows/Linux Base Z peeling
    base_z_peeling = models.FloatField(
        verbose_name="Windows / Linux Base Z Peeling",
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10)],
        help_text="0.1 - 10.00",
    )

    base_z_peeling_step_1 = models.FloatField(
        verbose_name="Base Peeling(Step 1)",
        default=0.5,
        validators=[MinValueValidator(0.0025), MaxValueValidator(10)],
        help_text="0.0025 - 10.00",
    )

    base_z_peeling_step_2 = models.FloatField(
        verbose_name="Base Peeling(Step 2)",
        default=0.5,
        validators=[MinValueValidator(0.0025), MaxValueValidator(10)],
        help_text="0.0025 - 10.00",
    )

    # Normal Layer
    cure_time = models.PositiveIntegerField(
        default=1200,
        validators=[MinValueValidator(50), MaxValueValidator(20000)],
        help_text="50 - 20000",
    )

    wait_before_cure = models.PositiveSmallIntegerField(
        default=500,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text="1 - 5000",
    )

    wait_on_top = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(25), MaxValueValidator(5000)],
        help_text="25 - 5000",
    )

    wait_after_cure = models.PositiveSmallIntegerField(
        default=150,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text="1 - 5000",
    )

    light_ratio = models.FloatField(
        default=1,
        validators=[MinValueValidator(0.1), MaxValueValidator(2)],
        help_text="0.1 - 2.0",
    )

    # NOTE: (Depricated) windows z move speed
    z_speed = models.PositiveSmallIntegerField(
        verbose_name="Windows Z Speed",
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        help_text="1 - 9",
    )

    # NOTE: (Depricated) linux z move speed
    advanced_z_speed = models.PositiveSmallIntegerField(
        verbose_name="Linux Z Speed",
        default=310,
        validators=[MinValueValidator(150), MaxValueValidator(50000)],
        help_text="150 - 50000",
    )

    # NOTE: (Depricated) Windows / Linux Peeling
    z_peeling = models.FloatField(
        verbose_name="Peeling (For Linux Step 1)",
        default=1,
        validators=[MinValueValidator(0.1), MaxValueValidator(10)],
        help_text="0.1 - 10.00",
    )

    # Normal Layers
    z_speed_up_step_1 = models.PositiveSmallIntegerField(
        verbose_name="Z Speed Up (Step 1)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    z_speed_up_step_2 = models.PositiveSmallIntegerField(
        verbose_name="Z Speed Up (Step 2)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    z_speed_down_step_1 = models.PositiveSmallIntegerField(
        verbose_name="Z Speed Down (Step 1)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    z_speed_down_step_2 = models.PositiveSmallIntegerField(
        verbose_name="Z Speed Down (Step 2)",
        default=310,
        validators=[MinValueValidator(120), MaxValueValidator(20000)],
        help_text="120 - 20000",
    )

    z_peeling_step_1 = models.FloatField(
        verbose_name="Z Peeling (Step 1)",
        default=0.5,
        validators=[MinValueValidator(0.0025), MaxValueValidator(10)],
        help_text="0.0025 - 10.00",
    )

    z_peeling_step_2 = models.FloatField(
        verbose_name="Z Peeling (Step 2)",
        default=0.5,
        validators=[MinValueValidator(0.0025), MaxValueValidator(10)],
        help_text="0.0025 - 10.00",
    )

    resin_temp = models.PositiveSmallIntegerField(
        verbose_name="Resin Temp Min",
        default=36,
        validators=[MinValueValidator(20), MaxValueValidator(80)],
        help_text="20 - 80",
    )

    resin_temp_max = models.PositiveSmallIntegerField(
        verbose_name="Resin Temp Max",
        default=37,
        validators=[MinValueValidator(20), MaxValueValidator(80)],
        help_text="20 - 80",
    )

    # Dimming
    dimming_type = models.IntegerField(
        choices=DIMMING_TYPES.choices, default=DIMMING_TYPES.OFF
    )
    dimming_amount_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    wall_around_dimming = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    skip_dimming_for_early_layers = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.resin_temp >= self.resin_temp_max:
            raise ValidationError(
                {
                    "resin_temp": f"Must be lower than {self.resin_temp_max}",
                    "resin_temp_max": f"Must be bigger than {self.resin_temp}",
                }
            )


class Projector(models.Model):
    model = models.CharField(max_length=19, unique=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model


class Machine(models.Model):
    class RESIN_TYPE(models.TextChoices):
        OPEN = "open", "Open Resin"
        CLOSED = "close", "Closed Resin"

    class SLICER_AUTOCENTER(models.IntegerChoices):
        CENTER_PIECES = 0, "Center Pieces"
        CENTER_ORIGIN = 1, "Center Origin"

    is_active = models.BooleanField(default=True, verbose_name="Active", help_text="Machine status")

    serial = models.CharField(max_length=15,unique=True,validators=[MinLengthValidator(12),RegexValidator(r"^[\d]*$", message="Only digit"),],)

    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="machines",) # limit_choices_to={"applications__name": "MegaPlatform"}
    machine_type = models.ForeignKey(MachineType,on_delete=models.SET_NULL,null=True,blank=True,related_name="machines",)
    mac = models.CharField(max_length=12,unique=True,validators=[MinLengthValidator(12), RegexValidator(r"^[A-F0-9]*$")],)

    teamviewer_id = models.CharField(max_length=12,null=True,blank=True,validators=[MinLengthValidator(10),RegexValidator(r"^[\d]*$", message="Only digit"),],)
    teamviewer_version = models.CharField(max_length=10, null=True, blank=True)

    profiles = models.ManyToManyField(Profile, related_name="machines")

    unconfirmed_profiles = models.ManyToManyField(Profile, blank=True) # , limit_choices_to={"confirmed": False}


    check_status = models.BooleanField(default=False,verbose_name="Check Status",help_text="! Machine will check status on every actions. Connection required.",)
    resin_type = models.CharField(max_length=5, choices=RESIN_TYPE.choices, default=RESIN_TYPE.OPEN)
    enable_stl_slc = models.BooleanField(default=False,verbose_name="STL Support",help_text="Machine can slice stl files.",)

    software_version = models.CharField(max_length=10, null=True, blank=True, verbose_name="Version (software)")
    ip = models.GenericIPAddressField(verbose_name="Ip Address",protocol="both",unpack_ipv4=True,blank=True,null=True,)

    real_plate_x = models.FloatField(default=120.0, help_text="(mm)")
    print_area_x = models.IntegerField(default=1920, verbose_name="Print Area(X)")
    print_area_y = models.IntegerField(default=1080, verbose_name="Print Area(Y)")
    z_distance = models.FloatField(default=114, help_text="Z Distance (mm)")
    led_current = models.PositiveSmallIntegerField(verbose_name="Projector Led Power",default=750,validators=[MinValueValidator(51), MaxValueValidator(1023)],help_text="51 - 1023",)
    projector_model = models.ForeignKey(Projector, on_delete=models.SET_NULL, null=True, blank=True)
    projector_serial = models.CharField(max_length=21,blank=True,validators=[MinLengthValidator(19),RegexValidator(r"^[a-zA-Z0-9]*$", "Only alphanumeric are allowed."),],)

    heating_time = models.PositiveSmallIntegerField(default=30,validators=[MinValueValidator(5), MaxValueValidator(60)],help_text="Heating (min)",)
    heater_close_time = models.PositiveSmallIntegerField(default=240, help_text="Heater Close (min)")
    bed_heater_temp_limit = models.PositiveIntegerField(default=65,validators=[MinValueValidator(40), MaxValueValidator(90)],help_text="Max temp limit for heater. (40-90)",)

    note = models.TextField(max_length=500, null=True, blank=True)

    client_sync = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    autocenter = models.IntegerField(choices=SLICER_AUTOCENTER.choices, default=SLICER_AUTOCENTER.CENTER_PIECES)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_full_change", "Can Change Machine Full Permission"),
        ]

    def __str__(self):
        return self.serial

    @property
    def active(self):
        return self.is_active and self.owner.active

    @property
    def _has_mask(self):
        return True if self.mask else False

    def update_sync(self):
        self.client_sync = timezone.now()
        self.save()

    def update_last_activity(self):
        self.last_activity = timezone.now()
        cache.clear()
        self.save()

    def update_software_version(self, version):
        if len(version) > 0:
            if self.software_version != version:
                self.software_version = version
                self.save()

    def save(self, *args, **kwargs):
        """
        Alternative way to checking self.pk we can check self._state of the model:
        - self._state.adding is True creating
        - self._state.adding is False updating
        """
        if self._state.adding:
            pass
            # Cache'i temizle, yeni makine oluşturuluyor
            # raise ValueError("Updating the value of creator isn't allowed")
        super().save(*args, **kwargs)


class PrintLog(models.Model):
    PRINT_STATUS = (
        ("successful", "Successful"),
        ("unsuccessful", "Unsuccessful"),
        ("cancelled", "Cancelled"),
        ("faulty", "Faulty"),
    )

    START_TYPE = (
        ("normal", "NoHeating"),
        ("quickstart", "Quickstart"),
        ("overtime", "Overtime"),
        ("overtemp", "Overtemp"),
    )

    id = models.BigAutoField(primary_key=True)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="print_logs")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=True, blank=True, null=True)
    model_name = models.CharField(max_length=100)
    profile_name = models.CharField(max_length=50, null=True, blank=True)
    software_version = models.CharField(max_length=10, null=True, blank=True)
    layer_count = models.PositiveSmallIntegerField()
    layer_thickness = models.PositiveIntegerField()
    finished_layers = models.PositiveIntegerField()
    print_status = models.CharField(max_length=12, choices=PRINT_STATUS, default="faulty")
    start_type = models.CharField(max_length=10, choices=START_TYPE, default="normal", null=True, blank=True)
    start_temp = models.FloatField(null=True, blank=True)
    total_solid_area = models.FloatField()
    exposure = models.FloatField()
    print_start = models.DateTimeField()
    print_real_start = models.DateTimeField(null=True, blank=True)
    print_stop = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Print Logs"

    def __str__(self):
        return str(self.id)

    @property
    def printing_time(self):
        if self.print_stop:

            print_start = (
                self.print_real_start if self.print_real_start else self.print_start
            )

            print_time = self.print_stop - print_start

            return int(print_time.seconds / 60)
        return 0