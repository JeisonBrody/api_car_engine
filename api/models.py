from django.db import models
from datetime import datetime


class photos(models.Model):
    name = models.CharField(max_length=255, default='')
    photo = models.ImageField(upload_to='archive/photo', verbose_name='Изображение')
    model_recognition = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class company(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название компании")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Компании"
        verbose_name = "Компании"


class car_model(models.Model):
    company_id = models.ForeignKey(company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Название модели")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Модели'
        verbose_name = "Модели"


class engines(models.Model):
    title = models.CharField(max_length=100, default='', verbose_name="Название двигателя", unique=True)
    engine_capacity = models.CharField(max_length=15, default='', verbose_name='Объем двигателя')

    def __str__(self):
        return self.title + " " + self.engine_capacity

    class Meta:
        verbose_name_plural = "Двигатели"
        verbose_name = "Двигатели"



class generations(models.Model):
    car_model_id = models.ForeignKey(car_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    engine = models.ManyToManyField(engines)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Поколения'
        verbose_name = "Поколения"


class engine_params(models.Model):
    oil = (
        (92, 'АИ-92'),
        (95, 'АИ-95'),
        (98, 'АИ-98'),
        (100, 'АИ-100'),
        (0, 'Дизель')
    )

    id = models.OneToOneField(engines, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=25, verbose_name='Наименование двигателя')
    year_of_issue = models.CharField(max_length=30, default='', verbose_name="Годы выпуска")
    supply_system = models.CharField(max_length=30, default='', verbose_name="Система питания")
    engine_vol = models.FloatField(default=0, verbose_name="Объем двигателя")  # объем двигателя
    engine_pow = models.CharField(max_length=30, default='', verbose_name="Мощность двс")  # мощность двигателя
    torque = models.CharField(max_length=30, default='', verbose_name="Крутящий момент")  # крутящий момент
    cylinder_block = models.CharField(max_length=30, default='', verbose_name="Блок Цилиндров")
    block_head = models.CharField(max_length=30, default='', verbose_name="Головка Блока")
    stroke = models.FloatField(default=0, verbose_name='Ход поршня')  # ход поршня
    diameter_cyl = models.FloatField(default=0, verbose_name="Диаметр цилиндра")  # диаметр цилиндра
    gas = models.CharField(max_length=30, default='', choices=oil, verbose_name="Бензин")
    fuel_consumption = models.JSONField(default=dict(city=None, highway=None, mixed=None), verbose_name="Расход бензина")  # расход
    oil_in_engine = models.CharField(max_length=30, default='', verbose_name="Масло в двигателе")  # масло в двигатель
    oil_vol = models.FloatField(default=0, verbose_name="Количество масла в двс")  # количество масла в двигателе
    # compression = models.CharField(max_length=30, default='')   # степень сжатия

    defect = models.TextField(blank=True, verbose_name="Известные неисправности")   # известные неисправности и ремонт
    modification = models.TextField(blank=True, verbose_name="Модификации")  # модификации двигателя
    problem = models.TextField(blank=True, verbose_name="Проблемы")    # проблемы и недостатки
    tuning = models.TextField(blank=True, verbose_name="Тюнинг")   # тюнинг

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Информация о двигателе'
        verbose_name = "Информация о двигателе"
