from django.urls import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status

from apps.base.tests import BaseAPITest
from apps.products.models import Category, Product, KitAttribute, KitAttValue
from apps.stocks.models import StockMovement, StockMovementLine


class ProductAPITest(BaseAPITest):
    def setUp(self):
        super(ProductAPITest, self).setUp()
        self.computers_category = Category.objects.create(name='Computadores')
        self.processors_category = Category.objects.create(name='Processadores', saleable=False)
        self.hard_disks_category = Category.objects.create(name='Discos Rígidos', saleable=False)
        self.peripheral_category = Category.objects.create(name='Perifericos')

        self.pc_gamer = Product.objects.create(
            category=self.computers_category,
            name='PC Gamer',
            description='PC Gamer',
            type=Product.KIT
        )

        self.intel_pentium = Product.objects.create(
                category=self.processors_category,
                name='Processador Intel Pentium G4560',
                description='Processador Intel Pentium G4560 Kaby Lake, Cache 3MB, 3.5Ghz, LGA 1151, Intel HD '
                            'Graphics 610 BX80677G4560',
                type=Product.SIMPLE,
                unit_price=1870.47)

        self.amd_ryzen = Product.objects.create(
                category=self.processors_category,
                name='Processador AMD Ryzen 7 2700X',
                description='Processador AMD Ryzen 7 2700X c/ Wraith Prism Cooler, Octa Core, Cache 20MB, 3.7GHz (Max '
                            'Turbo 4.35GHz) AM4 - YD270XBGAFBOX',
                type=Product.SIMPLE,
                unit_price=445.76
            )

        self.hd_seagate = Product.objects.create(
                category=self.hard_disks_category,
                name='HD Seagate SATA 3,5´',
                description='HD Seagate SATA 3,5´ BarraCuda 1TB 7200RPM 64MB Cache SATA 6Gb/s - ST1000DM010',
                type=Product.SIMPLE,
                unit_price=445.76)

        self.hd_wd = Product.objects.create(
                category=self.hard_disks_category,
                name='HD WD SATA 3,5´',
                description='HD WD SATA 3,5´ RED NAS 1TB 5400RPM 64MB Cache SATA 6.0Gb/s - WD10EFRX',
                type=Product.SIMPLE,
                unit_price=266.55)

        self.mouse = Product.objects.create(
                category=self.peripheral_category,
                name='Mouse Microsoft',
                description='Mouse Microsoft',
                type=Product.SIMPLE,
                unit_price=100.10)

        self.stock_movement = StockMovement.objects.create(warehouse=self.warehouse, date=datetime.now())
        StockMovementLine.objects.create(stock=self.stock_movement, product=self.intel_pentium, quantity=10)
        StockMovementLine.objects.create(stock=self.stock_movement, product=self.hd_seagate, quantity=15)

        processor = KitAttribute.objects.create(
            kit=self.pc_gamer, name='Processador', category=self.processors_category)
        hard_disk = KitAttribute.objects.create(
            kit=self.pc_gamer, name='Disco Rígido', category=self.hard_disks_category)
        peripheral = KitAttribute.objects.create(
            kit=self.pc_gamer, name='Periférico', category=self.peripheral_category, required=False)

        KitAttValue.objects.create(attribute=processor, value=self.intel_pentium)
        KitAttValue.objects.create(attribute=processor, value=self.amd_ryzen)
        KitAttValue.objects.create(attribute=hard_disk, value=self.hd_seagate)
        KitAttValue.objects.create(attribute=hard_disk, value=self.hd_wd)
        KitAttValue.objects.create(attribute=peripheral, value=self.mouse)

    def test_make_sale_order_not_logged_in(self):
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk, 'kit': self.pc_gamer.pk}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_sale_order_not_logged_in(self):
        response = self.client.get(reverse('sale_order'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_make_sale_order_logged_in_with_a_valid_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        payload = {
            'sale_lines': [
                {'product': self.pc_gamer.pk, 'kit': self.pc_gamer.pk, 'attribute': 'Computador'}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Field product in "sale_lines" should be a Simple Product.')
        payload = {
            'sale_lines': [
                {'product': self.mouse.pk, 'attribute': 'Periférico'}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], '{} is not available'.format(self.mouse))
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk, 'kit': self.amd_ryzen.pk, 'attribute': 'Processador'}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Field kit in "sale_lines" should be a Kit Product.')
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Field product could not filled with not saleable product.')
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk, 'kit': self.pc_gamer.pk, 'attribute': 'Processador'}
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk, 'kit': self.pc_gamer.pk, 'attribute': 'Processador'},
                {'product': self.hd_seagate.pk, 'kit': self.pc_gamer.pk, 'attribute': 'Disco Rígido'},
                {'product': self.mouse.pk, 'kit': self.pc_gamer.pk, 'attribute': 'Periférico'},
            ]
        }
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        StockMovementLine.objects.create(stock=self.stock_movement, product=self.mouse, quantity=1)
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('sale_order'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_make_sale_order_logged_in_with_a_admin_user(self):
        payload = {
            'sale_lines': [
                {'product': self.intel_pentium.pk, 'kit': self.pc_gamer.pk}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        response = self.client.post(reverse('sale_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'User is not customer!')