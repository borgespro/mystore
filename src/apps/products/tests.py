from rest_framework import status
from rest_framework.reverse import reverse

from apps.base.tests import BaseAPITest
from .models import Category, Product, KitAttribute, KitAttValue


class CategoryAPITest(BaseAPITest):
    default_categories = [
        Category(name='Computadores'),
        Category(name='Discos Rígidos', saleable=False),
        Category(name='Processadores', saleable=False),
        Category(name='Periféricos')
    ]

    default_categories_count = len(default_categories)
    default_saleable_categories_count = len(list(filter(lambda category: category.saleable, default_categories)))

    def setUp(self):
        super(CategoryAPITest, self).setUp()
        Category.objects.bulk_create(self.default_categories)

    def test_list_all_categories(self):
        response = self.client.get(reverse('category_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], self.default_categories_count)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])

    def test_list_saleable_categories(self):
        response = self.client.get(reverse('saleable_category_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], self.default_saleable_categories_count)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])


class ProductAPITest(BaseAPITest):
    def setUp(self):
        super(ProductAPITest, self).setUp()
        self.computers_category = Category.objects.create(name='Computadores')
        self.empty_category = Category.objects.create(name='Categoria Vázia')

        self.products = [
            Product(
                category=self.computers_category,
                name='PC Básico',
                description='PC Básico',
                type=Product.KIT),
            Product(
                category=self.computers_category,
                name='PC Gamer',
                description='PC Gamer',
                type=Product.KIT),
            Product(
                category=self.computers_category,
                name='Macbook Pro',
                description='Macbook Pro',
                type=Product.SIMPLE,
                unit_price=5000.00)
        ]

        Product.objects.bulk_create(self.products)

    def test_list_all_products(self):
        response = self.client.get(reverse('product_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(self.products))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])

    def test_detail_product(self):
        product = Product.objects.filter(type=Product.SIMPLE).first()
        response = self.client.get(reverse('product_detail', kwargs={'pk': product.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], product.id)
        self.assertEqual(data['category'], product.category.name)
        self.assertEqual(data['name'], product.name)
        self.assertEqual(data['description'], product.description)
        self.assertEqual(data['type'], Product.SIMPLE)
        self.assertEqual(data['unit_price'], str(product.unit_price))
        self.assertNotIn('kit_attributes', data)
        pk = 9999999
        response = self.client.get(reverse('product_detail', kwargs={'pk': pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_kits(self):
        response = self.client.get(reverse('kit_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(list(filter(lambda product: product.type == Product.KIT, self.products))))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])

    def test_detail_kit(self):
        kit = Product.objects.filter(type=Product.KIT).first()
        response = self.client.get(reverse('kit_detail', kwargs={'pk': kit.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['id'], kit.id)
        self.assertEqual(data['category'], kit.category.name)
        self.assertEqual(data['name'], kit.name)
        self.assertNotIn('type', data)
        self.assertNotIn('unit_price', data)
        self.assertIn('kit_attributes', data)
        pk = Product.objects.filter(type=Product.SIMPLE).first().pk
        response = self.client.get(reverse('kit_detail', kwargs={'pk': pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_kit_with_attributes(self):
        kit = Product.objects.filter(type=Product.KIT).first()
        hard_disk_att = KitAttribute.objects.create(
            kit=kit, category=Category.objects.create(name='Discos Rígidos', saleable=False), name='Disco Rígido')
        processor_att = KitAttribute.objects.create(
            kit=kit, category=Category.objects.create(name='Processadores', saleable=False), name='Processador')
        response = self.client.get(reverse('kit_detail', kwargs={'pk': kit.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIn('kit_attributes', data)
        self.assertEqual(len(data['kit_attributes']), 2)
        KitAttValue.objects.create(
            attribute=hard_disk_att,
            value=Product.objects.create(
                category=self.computers_category,
                name='SanDisk 128 gb SSD',
                description='SanDisk 128 gb SSD',
                type=Product.SIMPLE)
        )
        response = self.client.get(
            reverse('attribute_value_list', kwargs={'attribute_id': hard_disk_att.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)
        response = self.client.get(
            reverse('attribute_value_list', kwargs={'attribute_id': processor_att.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['results']), 0)
        response = self.client.get(reverse('attribute_value_list', kwargs={'attribute_id': 9999999}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products_filtered_by_category(self):
        response_for_empty_category = self.client.get(
            reverse('product_list'), {'category': self.empty_category.pk}, format='json')
        self.assertEqual(response_for_empty_category.status_code, status.HTTP_200_OK)
        data = response_for_empty_category.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        response_for_computers_category = self.client.get(
            reverse('product_list'), {'category': self.computers_category.pk}, format='json')
        self.assertEqual(response_for_empty_category.status_code, status.HTTP_200_OK)
        data = response_for_computers_category.data
        total_products_computer_category = \
            len(list(filter(lambda product: product.category == self.computers_category, self.products)))
        self.assertEqual(data['count'], total_products_computer_category)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])

    def test_list_kits_filtered_by_category(self):
        response_for_empty_category = self.client.get(
            reverse('kit_list'), {'category': self.empty_category.pk}, format='json')
        self.assertEqual(response_for_empty_category.status_code, status.HTTP_200_OK)
        data = response_for_empty_category.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        response_for_computers_category = self.client.get(
            reverse('kit_list'), {'category': self.computers_category.pk}, format='json')
        self.assertEqual(response_for_empty_category.status_code, status.HTTP_200_OK)
        data = response_for_computers_category.data
        total_kits_computer_category = len(list(filter(
            lambda product: product.category == self.computers_category and product.type == Product.KIT, self.products))
        )
        self.assertEqual(data['count'], total_kits_computer_category)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])

