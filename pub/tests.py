from django.test import TestCase

from pubmanager.settings import build_database_config


class DatabaseConfigTests(TestCase):
    def test_mysql_url_with_sslmode_query_parameter_is_supported(self):
        config = build_database_config(
            'mysql://user:pass@host.example.com:4000/pubmanager_db?sslmode=require'
        )

        self.assertEqual(config['default']['NAME'], 'pubmanager_db')
        self.assertEqual(config['default']['HOST'], 'host.example.com')
        self.assertEqual(config['default']['PORT'], 4000)
        self.assertIn('ssl', config['default']['OPTIONS'])
        self.assertNotIn('sslmode', config['default']['OPTIONS'])
