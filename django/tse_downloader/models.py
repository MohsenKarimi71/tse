from django.db import models
from django.utils import timezone
import jdatetime


def persian_to_gregorian_datetime(persian_datetime):
    """
    تبدیل تاریخ و زمان شمسی به میلادی (پشتیبانی از ثانیه)
    input format:
         دیده بان بازار : 1403/10/2 - زمان آخرین معامله : 15:51:54 
    """
    parts = persian_datetime.split(' - ')   # جدا کردن تاریخ و زمان
    date_part = parts[0].split(' : ')[1]
    time_part = parts[1].split(': ')[1]  
    year, month, day = map(int, date_part.split('/'))  # تبدیل تاریخ به اعداد
    hour, minute, second = map(int, time_part.split(':'))  # تبدیل زمان به اعداد
    persian_date = jdatetime.datetime(year, month, day, hour, minute, second)
    return persian_date.togregorian()


def gregorian_to_persian_datetime(gregorian_datetime):
    """
    تبدیل تاریخ و زمان میلادی به شمسی (پشتیبانی از ثانیه)
    ورودی: یک شیء datetime به فرمت میلادی
    خروجی: یک رشته تاریخ و زمان شمسی به فرمت `YYYY-MM-DD HH:MM:SS`
    """
    persian_date = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
    return persian_date.strftime('%Y-%m-%d %H:%M:%S')


# Create your models here.
class AbstractStockClass(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    # تعریف گروه‌های مختلف بورسی
    AUTOMOTIVE = 'ATMTV'
    BASIC_METALS = 'BSCMTLS'
    CHEMICALS = 'CHMCLS'
    PETROLEUM_PRODUCTS = 'PTRLMPRDCTS'
    PAPER_PRODUCTS = 'PPRPRDCTS'
    PHARMACEUTICALS = 'PHRMCTCLS'
    CEMENT = 'CEMENT'
    TELECOMMUNICATION = 'TLCMNCTN'
    BANKS = 'BANKS'
    PETROCHEMICALS = 'PTRCHMCLS'
    AGRICULTURE = 'AGRCLTR'
    TRANSPORTATION = 'TRNSPRTTN'
    MACHINERY = 'MCHNRY'
    BUILDING_MATERIALS = 'BLDNGMTRLS'
    NONFERROUS_METALS = 'NNFRSMTLS'
    OIL_GAS = 'OILGAS'
    CERAMICS_GLASS = 'CRMCSGLS'
    SANDOGH = 'SNDGH'
    OTHER = 'OTHER'

    GROUP_CHOICES = [
        (AUTOMOTIVE, 'صنعت خودرو و ساخت قطعات'),
        (BASIC_METALS, 'صنعت فلزات اساسی'),
        (CHEMICALS, 'صنعت شیمیایی'),
        (PETROLEUM_PRODUCTS, 'صنعت فرآورده‌های نفتی، کک و سوخت هسته‌ای'),
        (PAPER_PRODUCTS, 'صنعت محصولات کاغذی'),
        (PHARMACEUTICALS, 'صنعت دارویی'),
        (CEMENT, 'صنعت سیمان، آهک و گچ'),
        (TELECOMMUNICATION, 'صنعت مخابرات'),
        (BANKS, 'صنعت بانک‌ها و موسسات اعتباری'),
        (PETROCHEMICALS, 'صنعت پتروشیمی'),
        (AGRICULTURE, 'صنعت کشاورزی'),
        (TRANSPORTATION, 'صنعت حمل و نقل'),
        (MACHINERY, 'صنعت ماشین‌آلات و تجهیزات'),
        (BUILDING_MATERIALS, 'صنعت ساختمان و مصالح ساختمانی'),
        (NONFERROUS_METALS, 'صنعت فلزات غیرآهنی'),
        (OIL_GAS, 'صنعت نفت و گاز'),
        (CERAMICS_GLASS, 'صنعت سرامیک و شیشه'),
        (SANDOGH, 'صندوق ها'),
        (OTHER, 'دیگر گروه ها')
    ]

    group = models.CharField(
        max_length=11,
        choices=GROUP_CHOICES,
        default=OTHER,
    )

    def __str__(self):
        return f'{self.name} - {self.get_group_display()}'

    class Meta:
        abstract = True


class Stock(AbstractStockClass):
    is_in_option_chain = models.BooleanField(default=False)


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)  # ارتباط با سهام خاص
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت سهام
    timestamp = models.DateTimeField(default=timezone.now)  # تاریخ و زمان ثبت قیمت

    def save(self, *args, **kwargs):
        if isinstance(self.timestamp, str):  # اگر تاریخ شمسی باشد
            self.timestamp = persian_to_gregorian_datetime(self.timestamp)  # تبدیل به میلادی
        super().save(*args, **kwargs)

    def get_persian_timestamp(self):
        return gregorian_to_persian_datetime(self.timestamp)  # تبدیل میلادی به شمسی هنگام نمایش

    class Meta:
        # اطمینان از اینکه برای هر سهام در هر زمان تنها یک قیمت ذخیره شده باشد
        unique_together = ('stock', 'timestamp')

    def __str__(self):
        return f"Price of {self.stock.name} at {self.get_persian_timestamp()}: {self.price}"


class Option(models.Model):
    stock = models.ForeignKey(to=Stock, on_delete=models.CASCADE)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت اعمال
    expiration_date = models.DateField(auto_now=False, auto_now_add=False)

    SELL_OPTION = "SELL"
    BUY_OPTION = "BUY"
    CONTRACT_CHOICES = [
        (SELL_OPTION, 'اختیار فروش'),
        (BUY_OPTION, 'اختیار خرید')
    ]
    contract_type = models.CharField(
        max_length=4,
        choices=CONTRACT_CHOICES
    )


class OptionPrice(models.Model):
    option = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت پریمیوم
    timestamp = models.DateTimeField(default=timezone.now)  # تاریخ و زمان ثبت قیمت

    def save(self, *args, **kwargs):
        if isinstance(self.timestamp, str):  # اگر تاریخ شمسی باشد
            self.timestamp = persian_to_gregorian_datetime(self.timestamp)  # تبدیل به میلادی
        super().save(*args, **kwargs)

    def get_persian_timestamp(self):
        return gregorian_to_persian_datetime(self.timestamp)  # تبدیل میلادی به شمسی هنگام نمایش