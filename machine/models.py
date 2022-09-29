from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
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
