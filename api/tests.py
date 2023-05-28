from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .constants import max_number_section

class TestCreateWallConfiguration(APITestCase):

    def test_create_conf_correct_input(self):
        sample_conf = {
            "conf": "10 20"
        }
        response = self.client.post(reverse('create_conf'), sample_conf)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_conf_invalid_input_char(self):
        sample_conf = {
            "conf": "10 p"
        }
        response = self.client.post(reverse('create_conf'), sample_conf)
        # print(response.status_code)
        # print(response.data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_conf_invalid_input_range(self):
        sample_conf = {
            "conf": "10 31 -1"
        }
        response = self.client.post(reverse('create_conf'), sample_conf)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_conf_invalid_input_max_number_section(self):
        pos_ = [(max_number_section + 1)*" 10"]
        pos_ = (' ').join(pos_)
        sample_conf = {
            "conf": {pos_}
        }
        response = self.client.post(reverse('create_conf'), sample_conf)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_conf_should_return(self):
        pos_ = [(max_number_section) * " 10"]
        pos_ = (' ').join(pos_)
        sample_conf = {
            "conf": {pos_}
        }
        response = self.client.post(reverse('create_conf'), sample_conf)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_conf_invalid_all_section_in_different_profile_(self):
        pos_ = [(max_number_section + 1) * " 10"]
        pos_ = ('\n').join(pos_)
        sample_conf = {
            "conf": {pos_}
        }
        response = self.client.post(reverse('create_conf'), sample_conf)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_conf_with_additional_spaces(self):
        sample_conf = {
            "conf": "10       10   21        22"
        }

        response = self.client.post(reverse('create_conf'), sample_conf)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    # GET

    def test_get_all_conf(self):
        response =self.client.get(reverse('create_conf'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class TestListWallConfiguration(APITestCase):
    def test_get_conf_valid_pk(self):
        sample_conf = {
            "conf": "10 20"
        }
        self.client.post(reverse('create_conf'), sample_conf)
        response = self.client.get(reverse('create_conf'))
        pk = int(response.data[0]['id'])

        res = self.client.get(reverse('get_conf', kwargs={"pk": pk}))
        self.assertEquals(res.status_code, status.HTTP_200_OK)


    def test_get_conf_invalid_pk(self):
        pk = 3232112
        res = self.client.get(reverse('get_conf', kwargs={"pk": pk}))
        self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_valid_pk(self):
        sample_conf = {
            "conf": "10 20"
        }
        self.client.post(reverse('create_conf'), sample_conf)
        response = self.client.get(reverse('create_conf'))
        pk = int(response.data[0]['id'])
        sample_conf = {
            "conf": "11 21"
        }
        response_put = self.client.put(reverse('get_conf', kwargs={"pk": pk}), data=sample_conf)
        self.assertEquals(response_put.status_code, status.HTTP_200_OK)

    def delte_valid_pk(self):
        sample_conf = {
            "conf": "10 20"
        }
        self.client.post(reverse('create_conf'), sample_conf)
        response = self.client.get(reverse('create_conf'))
        pk = int(response.data[0]['id'])

        response_delete = self.client.delete(reverse('get_conf', kwargs={"pk": pk}))
        self.assertEquals(response_delete.status_code, status.HTTP_204_NO_CONTENT)

class TestProfileDay(APITestCase):
    sample_conf = {
        "conf": "21 25 28\n17\n17 22 17 19 17"
    }

    def test_profile_day_invalid_profile_number(self):
        self.client.post(reverse('create_conf'), self.sample_conf)
        response = self.client.get(reverse('profile_day', kwargs={"profile": 4, "day": 1}))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_day_valid_profile_number(self):
        self.client.post(reverse('create_conf'), self.sample_conf)
        response = self.client.get(reverse('profile_day', kwargs={"profile": 1, "day":1}))
        day = response.data.get('day')
        ice_amount = response.data.get('ice_amount')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(day, 1)
        self.assertEquals(ice_amount, 585)



class TestProfileOverview(APITestCase):
    sample_conf = {
        "conf": "21 25 28\n17\n17 22 17 19 17"
    }
    def test_profile_overview(self):
        self.client.post(reverse('create_conf'), self.sample_conf)
        response = self.client.get(reverse("profile_overview", kwargs={"profile": 1, "day": 1}))
        day = response.data.get('day')
        cost = response.data.get('cost')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(day, 1)
        self.assertEquals(cost, 1111500)



class TestProfileOverviewDay(APITestCase):
    sample_conf = {
        "conf": "21 25 28\n17\n17 22 17 19 17"
    }
    def test_profile_overview_day(self):
        self.client.post(reverse("create_conf"), self.sample_conf)
        response = self.client.get(reverse('profile_overview_day', kwargs={"day": 1}))
        day = response.data.get("day")
        cost = response.data.get("cost")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(day, 1)
        self.assertEquals(cost, 3334500)




class TestWallOverview(APITestCase):
    sample_conf = {
        "conf": "21 25 28\n17\n17 22 17 19 17"
    }

    def test_wall_overview(self):
        self.client.post(reverse('create_conf'), self.sample_conf)
        response = self.client.get(reverse("wall_overview"))
        day = response.data.get('day')
        cost = response.data.get('cost')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(day, None)
        self.assertEquals(cost, 32233500)





