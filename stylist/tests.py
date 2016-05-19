from django.core.urlresolvers import reverse
from django.test import TestCase

from stylist.models import Item

class ForecastTestCase(TestCase):
    """Common superclass for forecast view tests."""

    def setUp(self):
        self.client.login(username='Paulina', password='pppppppp')
    
    def get_forecast(self, low, high):
        return self.client.post(reverse('stylist:forecast'),
                {'low': str(low), 'high': str(high)})


class ForecastViewTest(ForecastTestCase):
    fixtures = ['test_fixtures/users.json', 'test_fixtures/items.json']

    def test_no_top_or_bottom(self):
        """View should find no set if appropriate top or bottom unavailable."""
        # No top available
        response = self.get_forecast(70, 80)
        self.assertEqual(response.context['clothes'], ())
        
        # No bottom available
        response = self.get_forecast(55, 60)
        self.assertEqual(response.context['clothes'], ())
    
    def test_highest_score_set(self):
        """View should return highest scored set of available clothes."""
        response = self.get_forecast(40, 50)
        self.assertEqual(response.context['clothes'][0].id, 11)
        self.assertIn(response.context['clothes'][1].id, [1, 5])
        self.assertEqual(response.context['clothes'][2].id, 20)


class ForecastViewTestExtra(ForecastTestCase):
    fixtures = ['test_fixtures/users.json',
            'test_fixtures/items.json', 'test_fixtures/items_extra.json']

    def test_wear_outer_layer_if_high_temp_variation(self):
        """Set of clothes should contain outer layer if cold weather
        or diurnal temperature variation is high.
        """
        # Warm weather, low variation -> no outer layer
        response = self.get_forecast(70, 80)
        self.assertNotEqual(response.context['clothes'], ())
        self.assertIsNone(response.context['clothes'][2])
        
        # Warm weather, high variation -> outer layer
        response = self.get_forecast(70, 90)
        self.assertNotEqual(response.context['clothes'], ())
        self.assertIsNotNone(response.context['clothes'][2])

        # Cold weather, low variation -> outer layer
        response = self.get_forecast(40, 50)
        self.assertNotEqual(response.context['clothes'], ())
        self.assertIsNotNone(response.context['clothes'][2])

        # Cold weather, high variation -> outer layer
        response = self.get_forecast(30, 50)
        self.assertNotEqual(response.context['clothes'], ())
        self.assertIsNotNone(response.context['clothes'][2])
